package com.balladofworms.mobilewatch

import android.content.Context
import android.graphics.BitmapFactory
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

object IconConfig {
    // Item icons are the 32x32 images out of the client's item DATs, named by ITEM ID:
    //   assets/itemicons/28503.png     (bundled)
    //   <BASE_URL>28503.png            (hosted, same repo pattern as the zone maps)
    //
    // WHERE TO PUT THEM -- either works, and both can be used at once (a bundled subset,
    // say gear only, with the rest hosted). The app checks assets, then the device cache,
    // then the URL, and works out on its own which of the two you did; there is nothing
    // to switch on.
    //   1) Bundled: drop <id>.png into  app/src/main/assets/itemicons/  and rebuild.
    //   2) Hosted:  push them to an  icons/  folder beside  maps/  in the public repo.
    const val BASE_URL = "https://raw.githubusercontent.com/BalladOfWorms/MobileWatch/main/icons/"

    const val ASSET_DIR = "itemicons"

    // png first -- that is what the extractor writes. The others cost nothing until a png misses.
    val EXTENSIONS = listOf("png", "webp", "jpg")
}

/**
 * WHY THIS IS SHAPED THE WAY IT IS
 *
 * The item list is a LazyColumn that can hold hundreds of rows, so an icon lookup has to be
 * cheap on the second, third and hundredth time it is asked for, and it must not fire an HTTP
 * request per row on a phone with no icons installed. Four things handle that:
 *
 *  1. AN LRU IN MEMORY. Decoded icons are ~4 KB each; the last few hundred are kept, so
 *     scrolling back up is instant and costs no IO at all.
 *
 *  2. A MISS SET. An id that is absent locally AND remotely is remembered for the session, so
 *     a list full of icon-less items asks once each rather than on every recomposition.
 *
 *  3. THE APP DECIDES FOR ITSELF WHETHER ICONS EXIST. `available` flips true as soon as any
 *     icon loads, from assets or the host, and rows only reserve a tile once it has. Until
 *     then the lists look exactly as they did before. Nothing probes the filesystem to find
 *     this out -- see the note by readLocal about why listing the assets folder is banned.
 *
 *  4. A NETWORK LATCH. A transport failure (aeroplane mode, dead wifi) parks the network for a
 *     minute instead of paying an 8s connect timeout per row, and a long run of clean 404s with
 *     no hits parks it for the session.
 */
object ItemIcons {
    private const val MEM_MAX = 400
    private const val NET_PAUSE_MS = 60_000L
    private const val MISS_LIMIT = 40          // clean 404s, with no hit at all, before we stop asking
    private const val PREFS = "mobilewatch"
    private const val KEY_REMOTE_OK = "itemIconsRemote"

    private val memCache = object : LinkedHashMap<Int, ImageBitmap>(64, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<Int, ImageBitmap>): Boolean =
            size > MEM_MAX
    }
    private val missing = HashSet<Int>()

    /** Flips to true the moment any icon loads, from assets or the host. Composables read
     *  it to decide whether to reserve a tile, so it is Compose state rather than a plain
     *  flag -- rows recompose themselves when it changes. */
    var available by mutableStateOf(false)
        private set
    @Volatile private var remoteOk: Boolean? = null
    @Volatile private var netPausedUntil = 0L   // transport is down -- retry after a minute
    @Volatile private var remoteOff = false     // nothing is published -- stop asking this session
    @Volatile private var remoteMisses = 0

    /** Already decoded? Lets a row draw its icon on the first frame instead of flickering in. */
    fun peek(id: Int): ImageBitmap? = synchronized(memCache) { memCache[id] }

    /**
     * assets -> device cache -> host. Blocking; call it off the main thread.
     * `probe` forces the network attempt even before we know any icons exist -- the detail
     * screen passes true, which is how a hosted set gets discovered.
     */
    fun load(context: Context, id: Int, probe: Boolean = false): ImageBitmap? {
        if (id <= 0) return null
        peek(id)?.let { return it }
        synchronized(missing) { if (id in missing) return null }

        readLocal(context, id)?.let { return store(id, it) }

        var unreachable = false
        if (probe || remoteOk(context)) {
            downloadIcon(context, id)?.let { return store(id, it) }
            unreachable = System.currentTimeMillis() < netPausedUntil
        }
        // Only a confirmed absence is recorded. If the network was simply unreachable the id
        // stays open so it resolves the next time the row scrolls past.
        if (!unreachable) synchronized(missing) { missing.add(id) }
        return null
    }

    private fun store(id: Int, img: ImageBitmap): ImageBitmap {
        synchronized(memCache) { memCache[id] = img }
        if (!available) available = true
        return img
    }

    // -- local ----------------------------------------------------------------
    private fun cacheDir(c: Context) = File(c.cacheDir, IconConfig.ASSET_DIR).apply { mkdirs() }

    private fun readLocal(context: Context, id: Int): ImageBitmap? {
        for (ext in IconConfig.EXTENSIONS) {
            val name = "$id.$ext"
            runCatching { context.assets.open("${IconConfig.ASSET_DIR}/$name").use { it.readBytes() } }
                .getOrNull()?.let { b ->
                    BitmapFactory.decodeByteArray(b, 0, b.size)?.let { return it.asImageBitmap() }
                }
            val f = File(cacheDir(context), name)
            if (f.exists() && f.length() > 0L)
                BitmapFactory.decodeFile(f.path)?.let { return it.asImageBitmap() }
        }
        return null
    }

    // NOTE: do NOT ask AssetManager to list the icons folder to find out whether icons are
    // bundled. With ~24,000 files in it that call takes seconds, and anything calling it
    // during composition freezes the UI -- it was blocking typing in the search box. The
    // presence of icons is learned from the first successful load instead, which costs
    // nothing extra because that load was going to happen anyway.

    // -- hosted ---------------------------------------------------------------
    private fun remoteOk(context: Context): Boolean {
        remoteOk?.let { return it }
        val v = runCatching {
            context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getBoolean(KEY_REMOTE_OK, false)
        }.getOrDefault(false)
        remoteOk = v
        return v
    }

    private fun markRemoteOk(context: Context) {
        if (remoteOk == true) return
        remoteOk = true
        remoteMisses = 0
        runCatching {
            context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
                .edit().putBoolean(KEY_REMOTE_OK, true).apply()
        }
    }

    private class Unreachable : IOException()

    private fun downloadIcon(context: Context, id: Int): ImageBitmap? {
        if (remoteOff || System.currentTimeMillis() < netPausedUntil) return null
        for (ext in IconConfig.EXTENSIONS) {
            val name = "$id.$ext"
            val bytes = try {
                download(IconConfig.BASE_URL + name)
            } catch (e: Unreachable) {
                netPausedUntil = System.currentTimeMillis() + NET_PAUSE_MS
                return null
            } ?: continue
            if (bytes.isEmpty()) continue
            runCatching { File(cacheDir(context), name).writeBytes(bytes) }
            BitmapFactory.decodeByteArray(bytes, 0, bytes.size)?.let {
                markRemoteOk(context)
                return it.asImageBitmap()
            }
        }
        // A run of clean 404s with nothing ever found means the icons simply are not published.
        // Stop asking for the rest of the session rather than trickling requests out per row.
        if (remoteOk != true && ++remoteMisses >= MISS_LIMIT) remoteOff = true
        return null
    }

    /** null = a clean "not there". Throws Unreachable when the network itself is down. */
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
}
