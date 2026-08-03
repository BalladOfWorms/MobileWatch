package com.balladofworms.mobilewatch

import android.content.Context
import android.graphics.BitmapFactory
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.asAndroidBitmap
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

object MapConfig {
    // Zone maps use the standard FFXI map-pack naming that OmniWatch / OT use:
    //   "<zoneID-in-hex>_<mapIndex>.<ext>"   e.g.  0a_0.png , 0a_1.png , 118_0.gif
    // The hex is tried both zero-padded ("0a_0") and bare ("a_0"); map index starts at 0.
    //
    // WHERE TO PUT MAPS — two options (both work; app checks assets first, then cache, then URL):
    //   1) Bundled: drop the pack's files into  app/src/main/assets/maps/  and rebuild.
    //      Simplest for testing; they ship inside the APK (watch total size for a full pack).
    //   2) Hosted: put the files at BASE_URL (a GitHub repo's raw URL works). No rebuild needed,
    //      keeps the APK small; downloaded maps are cached on device after first view.
    const val BASE_URL = "https://raw.githubusercontent.com/BalladOfWorms/MobileWatch/main/maps/"

    // gif first (many packs are gif), same order OmniWatch probes.
    val EXTENSIONS = listOf("gif", "png", "jpg", "jpeg", "webp")

    // Hex name styles, in probe order: zero-padded lower/upper, then bare lower/upper.
    val FORMATS = listOf("%02x_%d", "%02X_%d", "%x_%d", "%X_%d")
}

/**
 * WHY THIS IS SHAPED THE WAY IT IS (rewritten rev 397)
 *
 * A zone's page count is not known up front, so the loader walks index 0, 1, 2 ...
 * until one misses. The old version paid for that miss OVER THE NETWORK every single
 * time a zone was opened: 4 name styles x 5 extensions = 20 HTTP requests to GitHub
 * raw, all 404, with an 8s connect timeout each -- and it did that even when every
 * real page was already sitting in the disk cache. Worse, it tried assets -> disk ->
 * NETWORK for name style 1 before it ever looked at disk for name style 2, so a zone
 * whose files use the 4th style fired 15 pointless requests per cached page on top of
 * that. Four cached pages cost 80 wasted requests per view.
 *
 * Three changes fix it, and the first is the one that matters:
 *
 *  1. A MANIFEST. After a successful probe the resolved filenames are written to
 *     cacheDir/maps/.idx_<zoneId>. Every later view reads that list and loads exactly
 *     those files from assets or disk -- ZERO network, zero probing. An EMPTY manifest
 *     records "this zone has no maps" so a mapless zone stops re-probing too; that
 *     negative is trusted for a week in case maps get added. If a listed file has gone
 *     missing the manifest is deleted and the zone re-probes, so a cleared cache heals.
 *
 *  2. LOCAL BEFORE NETWORK, ACROSS ALL NAME STYLES. Every style/extension pair is
 *     checked against assets and disk before any of them touches the network.
 *
 *  3. STICKY STYLE. Pages within one zone always share a naming style, so once page 0
 *     resolves, later pages try that exact combination first and the terminating miss
 *     costs ONE request instead of twenty.
 *
 * Plus: a transport failure (aeroplane mode, dead wifi) aborts the whole probe at once
 * instead of burning 20 x 8s of connect timeouts, and no manifest is written from a
 * probe that was cut short that way.
 */
object MapLoader {
    private const val MAX_INDEX = 40
    private const val NEG_TTL_MS = 7L * 24 * 60 * 60 * 1000   // re-probe a mapless zone weekly

    /** Thrown when the network itself is unreachable, as opposed to a clean 404. */
    private class Unreachable : IOException()

    /** Keep decoded maps for the last few zones in memory so re-viewing is instant. */
    private val memCache = object : LinkedHashMap<Int, List<ImageBitmap>>(8, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<Int, List<ImageBitmap>>): Boolean = size > 4
    }

    private fun cacheDir(c: Context) = File(c.cacheDir, "maps").apply { mkdirs() }
    private fun manifest(c: Context, zoneId: Int) = File(cacheDir(c), ".idx_$zoneId")

    /** All maps for a zone by its ID. */
    fun loadAll(context: Context, zoneId: Int): List<ImageBitmap> {
        synchronized(memCache) { memCache[zoneId]?.let { return it } }

        readManifest(context, zoneId)?.let { cached ->
            if (cached.isNotEmpty()) synchronized(memCache) { memCache[zoneId] = cached }
            return cached
        }

        val images = ArrayList<ImageBitmap>()
        val files = ArrayList<String>()
        val seen = HashSet<Long>()
        var style: Pair<String, String>? = null
        var probeCompleted = true
        var i = 0
        while (i <= MAX_INDEX) {
            val hit = try {
                probe(context, zoneId, i, style)
            } catch (e: Unreachable) {
                probeCompleted = false
                null
            } ?: break
            style = hit.style
            if (seen.add(imageHash(hit.image))) {
                images.add(hit.image)
                files.add(hit.file)
            }
            i++
        }

        // Only record the result if the probe actually finished. A probe cut short by a dead
        // connection must not be frozen into a manifest claiming the zone has no maps.
        if (probeCompleted) writeManifest(context, zoneId, files)
        if (images.isNotEmpty()) synchronized(memCache) { memCache[zoneId] = images }
        return images
    }

    /** Drops the manifest so the next view re-probes. Nothing calls this yet; a Settings
     *  "refresh maps" action would. */
    fun forget(context: Context, zoneId: Int) {
        runCatching { manifest(context, zoneId).delete() }
        synchronized(memCache) { memCache.remove(zoneId) }
    }

    // -- manifest -------------------------------------------------------------
    private fun readManifest(context: Context, zoneId: Int): List<ImageBitmap>? {
        val f = manifest(context, zoneId)
        if (!f.exists()) return null
        val names = runCatching { f.readLines().filter { it.isNotBlank() } }.getOrNull() ?: return null
        if (names.isEmpty()) {
            // Recorded negative: no maps for this zone. Re-check occasionally in case maps
            // were added to the repo since.
            return if (System.currentTimeMillis() - f.lastModified() < NEG_TTL_MS) emptyList()
            else { f.delete(); null }
        }
        val out = ArrayList<ImageBitmap>(names.size)
        for (n in names) {
            val img = readLocal(context, n)
            if (img == null) { f.delete(); return null }   // stale -- fall through to a re-probe
            out.add(img)
        }
        return out
    }

    private fun writeManifest(context: Context, zoneId: Int, files: List<String>) {
        runCatching { manifest(context, zoneId).writeText(files.joinToString("\n")) }
    }

    // -- probing --------------------------------------------------------------
    private class Hit(val image: ImageBitmap, val file: String, val style: Pair<String, String>)

    private fun combos(style: Pair<String, String>?): List<Pair<String, String>> {
        val out = LinkedHashSet<Pair<String, String>>()
        if (style != null) out.add(style)                  // the one that worked last page
        for (fmt in MapConfig.FORMATS) for (ext in MapConfig.EXTENSIONS) out.add(fmt to ext)
        return out.toList()
    }

    private fun probe(context: Context, zoneId: Int, idx: Int, style: Pair<String, String>?): Hit? {
        val all = combos(style)

        // 1) everything local, every naming style, before the network is touched at all
        for ((fmt, ext) in all) {
            val file = fmt.format(zoneId, idx) + "." + ext
            readLocal(context, file)?.let { return Hit(it, file, fmt to ext) }
        }

        // 2) network. Once a style is known it is the only one worth asking for -- pages in
        //    one zone never change naming mid-zone -- which is what makes the terminating
        //    miss cost one request instead of twenty.
        val net = if (style != null) listOf(style) else all
        for ((fmt, ext) in net) {
            val file = fmt.format(zoneId, idx) + "." + ext
            val bytes = download(MapConfig.BASE_URL + file) ?: continue
            if (bytes.isEmpty()) continue
            runCatching { File(cacheDir(context), file).writeBytes(bytes) }
            BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
                ?.let { return Hit(it.asImageBitmap(), file, fmt to ext) }
        }
        return null
    }

    /** assets/maps/<file>, then the disk cache. Never network. */
    private fun readLocal(context: Context, file: String): ImageBitmap? {
        runCatching { context.assets.open("maps/$file").use { it.readBytes() } }.getOrNull()?.let { b ->
            BitmapFactory.decodeByteArray(b, 0, b.size)?.let { return it.asImageBitmap() }
        }
        val f = File(cacheDir(context), file)
        if (f.exists() && f.length() > 0L) {
            BitmapFactory.decodeFile(f.path)?.let { return it.asImageBitmap() }
        }
        return null
    }

    /** null = a clean "not there". Throws Unreachable if the network itself is down, so the
     *  caller can stop instead of waiting out one connect timeout per remaining combination. */
    private fun download(urlStr: String): ByteArray? {
        val conn = (URL(urlStr).openConnection() as HttpURLConnection).apply {
            connectTimeout = 8000; readTimeout = 15000; instanceFollowRedirects = true
        }
        return try {
            val code = conn.responseCode          // throws if it cannot reach the host
            if (code != 200) null else conn.inputStream.use { it.readBytes() }
        } catch (e: Exception) {
            throw Unreachable()
        } finally {
            conn.disconnect()
        }
    }

    /** Cheap fingerprint (dimensions + a sampled grid) to detect duplicate map pages.
     *  One getPixels() per sampled row rather than 256 individual getPixel() calls. */
    private fun imageHash(img: ImageBitmap): Long {
        val bmp = img.asAndroidBitmap()
        var h = 1125899906842597L
        h = h * 31 + bmp.width
        h = h * 31 + bmp.height
        val w = bmp.width
        val hgt = bmp.height
        if (w <= 0 || hgt <= 0) return h
        val row = IntArray(w)
        val stepX = maxOf(1, w / 16)
        val stepY = maxOf(1, hgt / 16)
        var y = 0
        while (y < hgt) {
            bmp.getPixels(row, 0, w, 0, y, w, 1)
            var x = 0
            while (x < w) { h = h * 31 + row[x]; x += stepX }
            y += stepY
        }
        return h
    }
}
