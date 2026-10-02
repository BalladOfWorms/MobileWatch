package com.balladofworms.mobilewatch.music

import android.content.Context
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.provider.DocumentsContract
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

// The music library: one folder the user picks with Android's own folder picker (Storage Access
// Framework -- no storage permission needed), scanned for FFXI's .bgw files and for ordinary
// audio files (MP3, FLAC, WAV, OGG, M4A...), e.g. tracks exported from OmniPlayer on the PC.

class MusicTrack(
    val uri: String,
    val fileName: String,
    val folder: String,              // path of the folder inside the picked tree, "/"-separated
    val size: Long,
    val bgw: BgwInfo?,               // header of a .bgw file; null for other formats
    val tagTitle: String? = null,    // other formats: their own tags
    val tagArtist: String? = null,
    val tagAlbum: String? = null,
    val durationMs: Long = 0
) {
    val isBgw get() = bgw != null
    var cat: CatalogEntry? = null

    val number: Int? = Regex("(\\d+)").find(fileName.substringBeforeLast('.'))?.value?.toIntOrNull()
    val fingerprint: String? get() = bgw?.fingerprint

    /** "023 Ronfaure.mp3" -> "Ronfaure"; "music023.bgw" -> "music023". */
    private val stemName: String get() {
        val stem = fileName.substringBeforeLast('.')
        return if (!isBgw) stem.replace(Regex("^\\d+\\s+"), "") else stem
    }

    val title: String get() = cat?.title ?: tagTitle?.takeIf { it.isNotBlank() } ?: stemName
    val expansion: String get() = cat?.expansion ?: ""
    val composer: String get() = cat?.composer ?: tagArtist ?: ""
    val heard: String get() = cat?.heard ?: ""

    val seconds: Double get() = bgw?.seconds ?: (durationMs / 1000.0)
    val loops: Boolean get() = bgw?.loopStart != null

    fun toJson(): JSONObject = JSONObject().apply {
        put("u", uri); put("f", fileName); put("d", folder); put("s", size)
        if (bgw != null) put("h", bgw.headerHex)
        tagTitle?.let { put("tt", it) }; tagArtist?.let { put("ta", it) }; tagAlbum?.let { put("tb", it) }
        put("ms", durationMs)
    }

    companion object {
        fun fromJson(o: JSONObject): MusicTrack? {
            val hex = o.optString("h", "")
            val bgw = if (hex.isNotEmpty()) BgwInfo.parse(hexBytes(hex)) ?: return null else null
            return MusicTrack(
                o.getString("u"), o.getString("f"), o.optString("d"), o.optLong("s"), bgw,
                o.optString("tt").ifBlank { null }, o.optString("ta").ifBlank { null },
                o.optString("tb").ifBlank { null }, o.optLong("ms")
            )
        }

        private fun hexBytes(h: String) = ByteArray(h.length / 2) { h.substring(it * 2, it * 2 + 2).toInt(16).toByte() }
    }
}

private val BgwInfo.headerHex: String get() = header.joinToString("") { "%02x".format(it.toInt() and 0xFF) }

object MusicLibrary {
    val AUDIO_EXT = setOf("mp3", "flac", "wav", "ogg", "oga", "opus", "m4a", "aac")

    private fun prefs(ctx: Context) = ctx.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE)
    private fun cacheFile(ctx: Context) = File(ctx.filesDir, "music_library.json")

    fun treeUri(ctx: Context): Uri? = prefs(ctx).getString("music_tree", null)?.let(Uri::parse)

    fun setTree(ctx: Context, uri: Uri) {
        runCatching {
            ctx.contentResolver.takePersistableUriPermission(uri,
                android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        prefs(ctx).edit().putString("music_tree", uri.toString()).apply()
        cacheFile(ctx).delete()
    }

    fun favourites(ctx: Context): MutableSet<String> =
        prefs(ctx).getStringSet("music_favs", emptySet())!!.toMutableSet()

    fun saveFavourites(ctx: Context, favs: Set<String>) {
        prefs(ctx).edit().putStringSet("music_favs", favs.toSet()).apply()
    }

    /** Favourites key a track by folder + file name, so they survive a re-scan. */
    fun favKey(t: MusicTrack) = "${t.folder}/${t.fileName}"

    private fun fingerprints(ctx: Context): MutableMap<String, String> {
        val out = HashMap<String, String>()
        runCatching {
            val o = JSONObject(prefs(ctx).getString("music_fp", "{}")!!)
            for (k in o.keys()) out[k] = o.getString(k)
        }
        return out
    }

    private fun saveFingerprints(ctx: Context, fp: Map<String, String>) {
        prefs(ctx).edit().putString("music_fp", JSONObject(fp).toString()).apply()
    }

    /** Last scan, from the cache file (instant); empty if none. */
    fun cached(ctx: Context): List<MusicTrack> {
        val f = cacheFile(ctx)
        if (!f.exists()) return emptyList()
        val tracks = runCatching {
            val a = JSONArray(f.readText())
            List(a.length()) { MusicTrack.fromJson(a.getJSONObject(it)) }.filterNotNull()
        }.getOrDefault(emptyList())
        recognise(ctx, tracks)
        return tracks
    }

    /** Walk the picked folder (and every folder inside it). Slow-ish: run off the main thread. */
    fun scan(ctx: Context): List<MusicTrack> {
        val tree = treeUri(ctx) ?: return emptyList()
        val cr = ctx.contentResolver
        val out = ArrayList<MusicTrack>()
        val rootId = DocumentsContract.getTreeDocumentId(tree)
        val queue = ArrayDeque<Pair<String, String>>()       // (documentId, folder path)
        queue.add(rootId to "")
        val cols = arrayOf(DocumentsContract.Document.COLUMN_DOCUMENT_ID,
            DocumentsContract.Document.COLUMN_DISPLAY_NAME,
            DocumentsContract.Document.COLUMN_MIME_TYPE,
            DocumentsContract.Document.COLUMN_SIZE)
        while (queue.isNotEmpty()) {
            val (docId, path) = queue.removeFirst()
            val children = DocumentsContract.buildChildDocumentsUriUsingTree(tree, docId)
            runCatching {
                cr.query(children, cols, null, null, null)?.use { c ->
                    while (c.moveToNext()) {
                        val id = c.getString(0)
                        val name = c.getString(1) ?: continue
                        val mime = c.getString(2) ?: ""
                        val size = if (c.isNull(3)) 0L else c.getLong(3)
                        if (mime == DocumentsContract.Document.MIME_TYPE_DIR) {
                            queue.add(id to (if (path.isEmpty()) name else "$path/$name"))
                            continue
                        }
                        val ext = name.substringAfterLast('.', "").lowercase()
                        val uri = DocumentsContract.buildDocumentUriUsingTree(tree, id)
                        if (ext == "bgw") {
                            val head = runCatching {
                                cr.openInputStream(uri)?.use { s ->
                                    val b = ByteArray(BgwInfo.HEADER_BYTES)
                                    var got = 0
                                    while (got < b.size) { val r = s.read(b, got, b.size - got); if (r < 0) break; got += r }
                                    b
                                }
                            }.getOrNull() ?: continue
                            val info = BgwInfo.parse(head) ?: continue
                            if (info.playable) out.add(MusicTrack(uri.toString(), name, path, size, info))
                        } else if (ext in AUDIO_EXT) {
                            var title: String? = null; var artist: String? = null
                            var album: String? = null; var ms = 0L
                            runCatching {
                                val r = MediaMetadataRetriever()
                                try {
                                    r.setDataSource(ctx, uri)
                                    title = r.extractMetadata(MediaMetadataRetriever.METADATA_KEY_TITLE)
                                    artist = r.extractMetadata(MediaMetadataRetriever.METADATA_KEY_ARTIST)
                                    album = r.extractMetadata(MediaMetadataRetriever.METADATA_KEY_ALBUM)
                                    ms = r.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull() ?: 0L
                                } finally { r.release() }
                            }
                            out.add(MusicTrack(uri.toString(), name, path, size, null, title, artist, album, ms))
                        }
                    }
                }
            }
        }
        recognise(ctx, out)
        runCatching { cacheFile(ctx).writeText(JSONArray(out.map { it.toJson() }).toString()) }
        return out
    }

    private fun recognise(ctx: Context, tracks: List<MusicTrack>) {
        val fp = fingerprints(ctx)
        val before = fp.size
        MusicCatalog.get(ctx).assign(tracks, fp)
        if (fp.size != before) saveFingerprints(ctx, fp)
    }
}
