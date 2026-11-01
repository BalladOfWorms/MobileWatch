package com.balladofworms.mobilewatch.music

import android.media.MediaDescription
import android.media.browse.MediaBrowser
import android.os.Bundle
import android.service.media.MediaBrowserService
import java.util.concurrent.Executors

// What Android Auto (and other media browsers) see of the player.
//
// Android Auto only shows apps that offer a media browser: this service. It hands Auto the same
// media session the lock screen uses -- so the car shows the track, its info and artwork, and
// its buttons work -- plus a library to pick music from:
//
//   Favourites / each playlist / All tracks / one folder per expansion
//
// Picking a track plays it with the rest of that list as the queue.

class MusicBrowserService : MediaBrowserService() {
    private val worker = Executors.newSingleThreadExecutor()

    override fun onCreate() {
        super.onCreate()
        // Auto can start this before the app has ever been opened this session.
        MusicPlayer.init(applicationContext)
        MusicPlayer.sessionToken?.let { sessionToken = it }
    }

    override fun onGetRoot(clientPackageName: String, clientUid: Int, rootHints: Bundle?): BrowserRoot =
        BrowserRoot(ROOT, null)

    override fun onLoadChildren(parentId: String, result: Result<MutableList<MediaBrowser.MediaItem>>) {
        // The library may still be loading from its cache; answer when it's ready.
        result.detach()
        worker.execute {
            val items = runCatching { children(parentId) }.getOrDefault(mutableListOf())
            result.sendResult(items)
        }
    }

    private fun children(parentId: String): MutableList<MediaBrowser.MediaItem> {
        val tracks = MusicPlayer.libraryForBrowsing(applicationContext)
        val out = mutableListOf<MediaBrowser.MediaItem>()
        when {
            parentId == ROOT -> {
                if (MusicPlayer.favourites.isNotEmpty()) out += folder(FAVS, "Favourites", "${MusicPlayer.favourites.size} tracks")
                MusicPlayer.playlists.forEach { (name, keys) -> out += folder("$PLAYLIST$name", name, "${keys.size} tracks") }
                out += folder(ALL, "All tracks", "${tracks.size} tracks")
                tracks.map { it.expansion.ifBlank { OTHER } }.distinct().sorted().forEach { exp ->
                    out += folder("$EXPANSION$exp", exp, null)
                }
            }
            else -> MusicPlayer.listFor(parentId, tracks).forEach { t -> out += playable(parentId, t) }
        }
        return out
    }

    private fun folder(id: String, title: String, sub: String?) = MediaBrowser.MediaItem(
        MediaDescription.Builder().setMediaId(id).setTitle(title).setSubtitle(sub)
            .setIconBitmap(MusicPlayer.artwork).build(),
        MediaBrowser.MediaItem.FLAG_BROWSABLE)

    private fun playable(parentId: String, t: MusicTrack) = MediaBrowser.MediaItem(
        MediaDescription.Builder()
            .setMediaId(MusicPlayer.mediaId(parentId, t))
            .setTitle(t.title)
            .setSubtitle(listOf(t.expansion, t.composer).filter { it.isNotBlank() }.joinToString(" \u00b7 "))
            .build(),
        MediaBrowser.MediaItem.FLAG_PLAYABLE)

    companion object {
        const val ROOT = "root"
        const val ALL = "all"
        const val FAVS = "favs"
        const val PLAYLIST = "pl:"
        const val EXPANSION = "exp:"
        const val OTHER = "Other music"
    }
}
