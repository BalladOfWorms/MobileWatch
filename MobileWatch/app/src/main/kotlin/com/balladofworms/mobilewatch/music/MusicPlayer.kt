package com.balladofworms.mobilewatch.music

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioTrack
import android.media.MediaMetadata
import android.media.MediaPlayer
import android.media.session.MediaSession
import android.media.session.PlaybackState
import android.net.Uri
import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.util.concurrent.Executors

// The music player. One instance for the whole app (an object), so music keeps playing while you
// move around MobileWatch, and the header button can show that something is playing.
//
// .bgw files are decoded here (BgwStream) and fed to an AudioTrack, which loops them exactly the
// way the game does: intro once, then the loop section seamlessly, for as long as repeat is on.
// Every other format (MP3, FLAC, WAV, OGG, M4A...) goes through Android's own MediaPlayer.

object MusicPlayer {
    // ── state the UI watches ─────────────────────────────────────────
    var tracks by mutableStateOf<List<MusicTrack>>(emptyList())
        private set
    var scanning by mutableStateOf(false)
        private set
    var current by mutableStateOf<MusicTrack?>(null)
        private set
    var playing by mutableStateOf(false)           // sound coming out (not paused)
        private set
    var loading by mutableStateOf(false)
        private set
    var repeat by mutableStateOf(true)             // true = loop forever, as in game
        private set
    var shuffle by mutableStateOf(false)
        private set
    var favourites by mutableStateOf<Set<String>>(emptySet())
        private set
    var message by mutableStateOf<String?>(null)
    var folders by mutableStateOf<List<Uri>>(emptyList())
        private set
    var playlists by mutableStateOf<Map<String, List<String>>>(emptyMap())
        private set
    /** The playlist being shown, or null for the whole library. */
    var activePlaylist by mutableStateOf<String?>(null)
    var hasFolder by mutableStateOf(false)
        private set

    private lateinit var app: Context
    private val main = Handler(Looper.getMainLooper())
    private val worker = Executors.newSingleThreadExecutor()     // folder scans
    private val loader = Executors.newSingleThreadExecutor()     // opening tracks (never waits on a scan)
    private var backend: Backend? = null
    private var queue: List<MusicTrack> = emptyList()
    private val history = ArrayList<MusicTrack>()
    private var loadToken = 0
    private var started = false

    // The media session: what the notification, the lock screen, Bluetooth and headset buttons
    // talk to. Its callbacks just call the player.
    private var session: MediaSession? = null
    val sessionToken: MediaSession.Token? get() = session?.sessionToken
    private var publishedUri: String? = null

    fun init(ctx: Context) {
        if (started) return
        started = true
        app = ctx.applicationContext
        val p = app.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE)
        repeat = p.getBoolean("music_repeat", true)
        shuffle = p.getBoolean("music_shuffle", false)
        favourites = MusicLibrary.favourites(app)
        playlists = MusicLibrary.playlists(app)
        folders = MusicLibrary.treeUris(app)
        hasFolder = folders.isNotEmpty()
        // Pause when headphones are unplugged, like any music app.
        androidx.core.content.ContextCompat.registerReceiver(app, object : BroadcastReceiver() {
            override fun onReceive(c: Context?, i: Intent?) { if (playing) togglePause() }
        }, IntentFilter(AudioManager.ACTION_AUDIO_BECOMING_NOISY),
            androidx.core.content.ContextCompat.RECEIVER_NOT_EXPORTED)
        worker.execute {
            val cached = MusicLibrary.visible(app, MusicLibrary.cached(app))
            main.post { if (tracks.isEmpty()) { tracks = cached; adoptFavourites() } }
        }
        session = MediaSession(app, "MobileWatch").apply {
            setCallback(object : MediaSession.Callback() {
                override fun onPlay() { if (!playing) togglePause() }
                override fun onPause() { if (playing) togglePause() }
                override fun onSkipToNext() = next()
                override fun onSkipToPrevious() = previous()
                override fun onSeekTo(pos: Long) = seekTo(pos)
                override fun onStop() = stop()
            })
        }
    }

    // ── zone music: a short taste of a zone's theme on its page ──────
    //
    // Opening a zone in the Zones tab plays the start of that zone's music from your library,
    // fading in, then out after a few seconds. It never interrupts: nothing happens if music
    // is already playing (this player or any other app), or if it's switched off in Settings.
    // It shows no notification and doesn't touch the now-playing bar.
    private var preview: Backend? = null
    const val CANT_PLAY = "This file can't be played -- it may be damaged or in an unknown format."
    private var previewToken = 0

    fun zoneMusicOn(): Boolean =
        app.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE).getBoolean("zone_music", true)

    fun setZoneMusicOn(on: Boolean) {
        app.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE).edit().putBoolean("zone_music", on).apply()
        if (!on) endPreview()
    }

    /** The library track that's this zone's music, or null (see ZoneMusic for the matching). */
    fun zoneTrack(zoneName: String, region: String, type: String = ""): MusicTrack? =
        ZoneMusic.pick(tracks, zoneName, region, type)

    fun previewZone(zoneName: String, region: String, type: String = "") {
        if (!started || !zoneMusicOn()) return
        val am = app.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        if (playing || loading || am.isMusicActive) return
        val t = zoneTrack(zoneName, region, type)?.takeIf { it.playable } ?: return
        endPreview(fade = false)
        val token = ++previewToken
        loader.execute {
            val b: Backend? = runCatching {
                if (t.bgw != null) {
                    val data = app.contentResolver.openInputStream(Uri.parse(t.uri))!!.use { it.readBytes() }
                    BgwBackend(data, t.bgw, false, 0L) { }
                } else MediaBackend(app, Uri.parse(t.uri), false, 0L) { }
            }.getOrNull()
            main.post {
                if (token != previewToken || playing || b == null) { b?.release(); return@post }
                preview = b
                b.setVolume(0f)
                b.start()
                ramp(b, token, 0f, 1f, 1200) {                 // fade in
                    main.postDelayed({
                        if (token == previewToken) ramp(b, token, 1f, 0f, 3500) { endPreview(fade = false) }
                    }, 9000)                                    // ...hold, then fade out
                }
            }
        }
    }

    /** Stop the zone music (leaving the zone page): a quick fade, then silence. */
    fun endPreview(fade: Boolean = true) {
        val b = preview ?: return
        val token = ++previewToken
        if (fade) ramp(b, token, 0.6f, 0f, 400) { if (preview === b) { b.release(); preview = null } }
        else { b.release(); preview = null }
    }

    private fun ramp(b: Backend, token: Int, from: Float, to: Float, ms: Long, then: () -> Unit) {
        val steps = maxOf(1, (ms / 50).toInt())
        var i = 0
        val r = object : Runnable {
            override fun run() {
                if (preview !== b || (token != previewToken && to != 0f)) return
                i++
                val f = i.toFloat() / steps
                // Ease the level so the fade sounds even to the ear.
                val v = from + (to - from) * f
                b.setVolume(v * v)
                if (i < steps) main.postDelayed(this, 50) else then()
            }
        }
        main.post(r)
    }

    // ── notification / lock screen ───────────────────────────────────
    private val ACTIONS = PlaybackState.ACTION_PLAY or PlaybackState.ACTION_PAUSE or
        PlaybackState.ACTION_PLAY_PAUSE or PlaybackState.ACTION_SKIP_TO_NEXT or
        PlaybackState.ACTION_SKIP_TO_PREVIOUS or PlaybackState.ACTION_SEEK_TO or PlaybackState.ACTION_STOP

    private fun pushState() {
        val s = session ?: return
        val st = when { current == null -> PlaybackState.STATE_STOPPED
                        loading -> PlaybackState.STATE_BUFFERING
                        playing -> PlaybackState.STATE_PLAYING
                        else -> PlaybackState.STATE_PAUSED }
        s.setPlaybackState(PlaybackState.Builder().setActions(ACTIONS)
            .setState(st, positionMs(), if (playing) 1f else 0f).build())
    }

    /** Tell the session and the notification what's happening now. */
    private fun publish() {
        val s = session ?: return
        val t = current
        if (t != null && t.uri != publishedUri) {
            s.setMetadata(MediaMetadata.Builder()
                .putString(MediaMetadata.METADATA_KEY_TITLE, t.title)
                .putString(MediaMetadata.METADATA_KEY_ARTIST, t.composer.ifBlank { t.expansion })
                .putString(MediaMetadata.METADATA_KEY_ALBUM, t.expansion)
                .putLong(MediaMetadata.METADATA_KEY_DURATION, durationMs())
                .build())
            publishedUri = t.uri
        }
        pushState()
        s.isActive = t != null
        val svc = MusicService.instance
        if (svc != null) svc.refresh()
        else if (t != null && (playing || loading)) MusicService.start(app)
        main.removeCallbacks(stateTicker)
        if (playing) main.postDelayed(stateTicker, 3000)
    }

    // While playing, re-send the position now and then: a looping track jumps back to its loop
    // point, which the lock screen's seek bar can't know about otherwise.
    private val stateTicker = object : Runnable {
        override fun run() { if (playing) { pushState(); main.postDelayed(this, 3000) } }
    }

    // ── library ──────────────────────────────────────────────────────
    /** Add a folder; the folders already added stay. */
    fun addFolder(uri: Uri) {
        MusicLibrary.addTree(app, uri)
        folders = MusicLibrary.treeUris(app)
        hasFolder = folders.isNotEmpty()
        rescan()
    }

    /** Take a folder out of the library (nothing on the phone is deleted). */
    fun removeFolder(uri: Uri) {
        MusicLibrary.removeTree(app, uri)
        folders = MusicLibrary.treeUris(app)
        hasFolder = folders.isNotEmpty()
        val pre = "$uri/document/"
        if (current?.uri?.startsWith(pre) == true) stop()
        tracks = tracks.filterNot { it.uri.startsWith(pre) }
        message = "Removed ${MusicLibrary.treeLabel(uri)} from the library"
    }

    /** Take tracks off the list (their files are untouched; adding their folder again brings
     *  them back). */
    fun removeTracks(list: List<MusicTrack>) {
        val uris = list.map { it.uri }.toSet()
        MusicLibrary.removeTracks(app, uris)
        if (current?.uri?.let { it in uris } == true) stop()
        tracks = tracks.filterNot { it.uri in uris }
        message = "Removed ${list.size} track${if (list.size == 1) "" else "s"} from the list"
    }

    /** Favourites saved before several folders were possible were keyed by the path inside the
     *  one folder; match them up to the same tracks' new keys. */
    private fun adoptFavourites() {
        val keys = tracks.map { MusicLibrary.favKey(it) }
        val known = keys.toSet()
        val stale = favourites.filter { it !in known }
        if (stale.isEmpty()) return
        val moved = stale.mapNotNull { old -> keys.firstOrNull { it.endsWith("/$old") || it.endsWith(old) }?.let { old to it } }
        if (moved.isEmpty()) return
        favourites = favourites - moved.map { it.first }.toSet() + moved.map { it.second }.toSet()
        MusicLibrary.saveFavourites(app, favourites)
    }

    fun rescan() {
        if (scanning) return
        scanning = true
        worker.execute {
            val found = runCatching { MusicLibrary.scan(app) }.getOrDefault(emptyList())
            val shown = MusicLibrary.visible(app, found)
            main.post {
                tracks = shown
                adoptFavourites()
                scanning = false
                message = if (shown.isEmpty()) "No music found" else "Found ${shown.size} tracks"
            }
        }
    }

    fun isFav(t: MusicTrack) = MusicLibrary.favKey(t) in favourites

    // ── playlists ────────────────────────────────────────────────────
    private fun putPlaylists(p: Map<String, List<String>>) {
        playlists = p
        MusicLibrary.savePlaylists(app, p)
    }

    /** The tracks of a playlist, in its order (ones no longer in the library are skipped). */
    fun playlistTracks(name: String): List<MusicTrack> {
        val byKey = tracks.associateBy { MusicLibrary.favKey(it) }
        return playlists[name].orEmpty().mapNotNull { byKey[it] }
    }

    fun createPlaylist(name: String, start: List<MusicTrack> = emptyList()): Boolean {
        val n = name.trim()
        if (n.isEmpty() || n in playlists) return false
        putPlaylists(playlists + (n to start.map { MusicLibrary.favKey(it) }.distinct()))
        message = "Created \"$n\""
        return true
    }

    fun addToPlaylist(name: String, list: List<MusicTrack>) {
        val cur = playlists[name] ?: return
        val add = list.map { MusicLibrary.favKey(it) }.filter { it !in cur }
        putPlaylists(playlists + (name to cur + add))
        message = "Added ${add.size} to \"$name\""
    }

    fun removeFromPlaylist(name: String, list: List<MusicTrack>) {
        val cur = playlists[name] ?: return
        val drop = list.map { MusicLibrary.favKey(it) }.toSet()
        putPlaylists(playlists + (name to cur.filterNot { it in drop }))
    }

    fun renamePlaylist(old: String, new: String): Boolean {
        val n = new.trim()
        if (n.isEmpty() || (n != old && n in playlists)) return false
        val rebuilt = LinkedHashMap<String, List<String>>()
        playlists.forEach { (k, v) -> rebuilt[if (k == old) n else k] = v }
        putPlaylists(rebuilt)
        if (activePlaylist == old) activePlaylist = n
        return true
    }

    fun deletePlaylist(name: String) {
        putPlaylists(playlists - name)
        if (activePlaylist == name) activePlaylist = null
    }

    /** Favourite (or un-favourite) several tracks at once. */
    fun setFavs(list: List<MusicTrack>, on: Boolean) {
        val keys = list.map { MusicLibrary.favKey(it) }.toSet()
        favourites = if (on) favourites + keys else favourites - keys
        MusicLibrary.saveFavourites(app, favourites)
    }

    fun toggleFav(t: MusicTrack) {
        val k = MusicLibrary.favKey(t)
        favourites = if (k in favourites) favourites - k else favourites + k
        MusicLibrary.saveFavourites(app, favourites)
    }

    // ── playback ─────────────────────────────────────────────────────
    /** Play [t]; [order] is the list as shown, which next/previous walk. */
    fun play(t: MusicTrack, order: List<MusicTrack> = queue) {
        if (!t.playable) { message = CANT_PLAY; return }
        queue = order
        current?.let { if (it !== t) history.add(it) }
        start(t, 0L)
    }

    private fun start(t: MusicTrack, fromMs: Long, autoPlay: Boolean = true) {
        endPreview(fade = false)
        release()
        current = t
        loading = true
        playing = false
        val token = ++loadToken
        publish()
        val looping = repeat
        loader.execute {
            val b: Backend? = runCatching {
                if (t.bgw != null) {
                    val data = app.contentResolver.openInputStream(Uri.parse(t.uri))!!.use { it.readBytes() }
                    BgwBackend(data, t.bgw, looping, fromMs) { main.post { if (token == loadToken) onEnded() } }
                } else {
                    MediaBackend(app, Uri.parse(t.uri), looping, fromMs) { main.post { if (token == loadToken) onEnded() } }
                }
            }.onFailure { e -> main.post { if (token == loadToken) message = "Can't play ${t.fileName}: ${e.message}" } }
                .getOrNull()
            main.post {
                if (token != loadToken) { b?.release(); return@post }
                loading = false
                backend = b
                if (b != null && autoPlay) { requestFocus(); b.start(); playing = true }
                publish()
            }
        }
    }

    private fun onEnded() {
        playing = false
        next()
    }

    fun togglePause() {
        val b = backend ?: run { current?.let { start(it, 0L) }; return }
        if (playing) { b.pause(); playing = false }
        else { requestFocus(); if (b.begun) b.resume() else b.start(); playing = true }
        publish()
    }

    fun next() {
        val pool = queue.ifEmpty { tracks }.filter { it.playable }
        if (pool.isEmpty()) return
        val cur = current
        val at = pool.indexOfFirst { it.uri == cur?.uri }          // by file: a rescan makes new objects
        val nxt = if (shuffle && pool.size > 1) pool.filter { it.uri != cur?.uri }.random()
                  else pool[(at + 1).mod(pool.size)]
        cur?.let { history.add(it) }
        start(nxt, 0L)
    }

    fun previous() {
        // A few seconds in, "previous" restarts the track, like most players.
        if (positionMs() > 3000) { seekTo(0L); return }
        val pool = queue.ifEmpty { tracks }.filter { it.playable }
        if (pool.isEmpty()) return
        val at = pool.indexOfFirst { it.uri == current?.uri }
        val prev = if (shuffle && history.isNotEmpty()) history.removeAt(history.size - 1)
                   else pool[(if (at < 0) 0 else at - 1).mod(pool.size)]
        start(prev, 0L)
    }

    fun stop() {
        release()
        playing = false
        loading = false
        current = null              // closes the notification and the now-playing bar
        loadToken++
        abandonFocus()
        publish()
    }

    fun seekTo(ms: Long) {
        val t = current ?: return
        val b = backend
        if (b is MediaBackend) { b.seekTo(ms); pushState(); return }
        start(t, ms.coerceAtLeast(0), autoPlay = playing)
    }

    fun changeRepeat(on: Boolean) {
        repeat = on
        app.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE).edit().putBoolean("music_repeat", on).apply()
        val b = backend ?: return
        if (b is MediaBackend) b.setLooping(on)
        else if (playing) current?.let { start(it, positionMs()) }   // restart in the new mode, same spot
    }

    fun changeShuffle(on: Boolean) {
        shuffle = on
        app.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE).edit().putBoolean("music_shuffle", on).apply()
    }

    fun positionMs(): Long = backend?.positionMs() ?: 0L
    fun durationMs(): Long = current?.let { (it.seconds * 1000).toLong() } ?: 0L

    private fun release() {
        backend?.release()
        backend = null
    }

    // ── audio focus: step aside for calls, navigation, other music ───
    private var focusRequest: AudioFocusRequest? = null

    private fun requestFocus() {
        val am = app.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        val req = focusRequest ?: AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN)
            .setAudioAttributes(ATTRS)
            .setOnAudioFocusChangeListener { change ->
                if (change == AudioManager.AUDIOFOCUS_LOSS || change == AudioManager.AUDIOFOCUS_LOSS_TRANSIENT) {
                    if (playing) togglePause()
                }
            }.build().also { focusRequest = it }
        am.requestAudioFocus(req)
    }

    private fun abandonFocus() {
        val am = app.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        focusRequest?.let { am.abandonAudioFocusRequest(it) }
    }

    internal val ATTRS: AudioAttributes = AudioAttributes.Builder()
        .setUsage(AudioAttributes.USAGE_MEDIA)
        .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
        .build()
}

private interface Backend {
    val begun: Boolean               // start() has been called
    fun setVolume(v: Float)
    fun start()
    fun pause()
    fun resume()
    fun positionMs(): Long
    fun release()
}

/**
 * A .bgw track through an AudioTrack. A writer thread decodes ahead and writes; when it reaches
 * the end with repeat on, it jumps the decoder back to the loop start and keeps writing, so the
 * join is seamless. Where playback "is" comes from the AudioTrack's own head position, mapped
 * back onto the track through the jumps recorded as they were written.
 */
private class BgwBackend(
    data: ByteArray, private val info: BgwInfo, private val looping: Boolean,
    startMs: Long, private val onEnd: () -> Unit
) : Backend {
    private val stream = openBgw(data, info)
    private val rate = info.sampleRate
    private val track: AudioTrack
    private val segments = ArrayList<LongArray>()      // [frames written before it, track frame]
    @Volatile private var running = true
    @Volatile private var paused = false
    @Volatile private var written = 0L
    private val thread: Thread

    init {
        val min = AudioTrack.getMinBufferSize(rate, AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT)
        track = AudioTrack.Builder()
            .setAudioAttributes(MusicPlayer.ATTRS)
            .setAudioFormat(AudioFormat.Builder()
                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                .setSampleRate(rate)
                .setChannelMask(AudioFormat.CHANNEL_OUT_STEREO).build())
            .setBufferSizeInBytes(maxOf(min * 4, rate * 4 / 2))       // about half a second
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
        val startFrame = (startMs * rate / 1000).coerceIn(0, info.totalSamples)
        stream.seek(startFrame)
        segments.add(longArrayOf(0, startFrame))
        thread = Thread({ writeLoop() }, "bgw-writer")
    }

    override var begun = false
    override fun start() { begun = true; track.play(); thread.start() }
    override fun setVolume(v: Float) { runCatching { track.setVolume(v) } }
    override fun pause() { paused = true; track.pause() }
    override fun resume() { paused = false; track.play() }

    override fun positionMs(): Long {
        val head = track.playbackHeadPosition.toLong() and 0xFFFFFFFFL
        val seg = synchronized(segments) { segments.lastOrNull { it[0] <= head } } ?: return 0
        return (seg[1] + (head - seg[0])) * 1000 / rate
    }

    override fun release() {
        running = false
        runCatching { track.pause(); track.flush() }
        runCatching { thread.join(500) }
        runCatching { track.release() }
    }

    private fun write(buf: ShortArray, frames: Int) {
        var off = 0
        val len = frames * 2
        while (off < len && running) {
            if (paused) { Thread.sleep(20); continue }
            val r = track.write(buf, off, len - off)
            if (r < 0) return
            off += r
        }
        written += frames
    }

    private fun writeLoop() {
        val chunk = 4096
        val buf = ShortArray(chunk * 2)
        var ended = false
        while (running) {
            if (paused) { Thread.sleep(20); continue }
            val n = stream.read(buf, chunk)
            if (n > 0) write(buf, n)
            if (n < chunk) {
                val ls = info.loopStart
                if (looping && ls != null) {
                    stream.seek(ls)
                    synchronized(segments) { segments.add(longArrayOf(written, ls)) }
                } else { ended = true; break }
            }
        }
        if (ended && running) {
            // Let what's buffered finish playing, then report the end.
            while (running && (track.playbackHeadPosition.toLong() and 0xFFFFFFFFL) < written) Thread.sleep(30)
            if (running) onEnd()
        }
    }
}

/** Every other format, through MediaPlayer (repeat = loop the whole file). */
private class MediaBackend(
    ctx: Context, uri: Uri, looping: Boolean, startMs: Long, onEnd: () -> Unit
) : Backend {
    private val mp = MediaPlayer().apply {
        setAudioAttributes(MusicPlayer.ATTRS)
        setDataSource(ctx, uri)
        isLooping = looping
        setOnCompletionListener { if (!isLooping) onEnd() }
        prepare()
        if (startMs > 0) seekTo(startMs.toInt())
    }

    override var begun = false
    override fun start() { begun = true; mp.start() }
    override fun setVolume(v: Float) { runCatching { mp.setVolume(v, v) } }
    override fun pause() = mp.pause()
    override fun resume() = mp.start()
    override fun positionMs(): Long = runCatching { mp.currentPosition.toLong() }.getOrDefault(0L)
    override fun release() { runCatching { mp.stop() }; mp.release() }
    fun seekTo(ms: Long) = mp.seekTo(ms.toInt())
    fun setLooping(on: Boolean) { mp.isLooping = on }
}
