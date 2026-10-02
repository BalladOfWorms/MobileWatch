package com.balladofworms.mobilewatch.music

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.drawable.Icon
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import com.balladofworms.mobilewatch.MainActivity
import com.balladofworms.mobilewatch.R

// Keeps the music going with the screen off or the app in the background, and shows the
// player's controls in the notification shade and on the lock screen (previous, play/pause,
// next, close, plus the seek bar Android draws from the media session).
//
// It runs only while there is a track: it is in the foreground (the ongoing notification, so
// Android won't stop it) while music plays; when paused the notification stays but can be
// swiped away; closing it, or the app being swiped away, stops the music.

class MusicService : Service() {
    private var wake: PowerManager.WakeLock? = null
    private var logo: Bitmap? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        instance = this
        val nm = getSystemService(NotificationManager::class.java)
        if (nm.getNotificationChannel(CHANNEL) == null) {
            nm.createNotificationChannel(NotificationChannel(CHANNEL, "Music", NotificationManager.IMPORTANCE_LOW).apply {
                description = "Music player controls"
                setShowBadge(false)
            })
        }
        // Keeps the CPU awake for the decoder while music plays with the screen off.
        wake = (getSystemService(Context.POWER_SERVICE) as PowerManager)
            .newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MobileWatch:music").apply { setReferenceCounted(false) }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // A start from the app (startForegroundService, no action) must reach startForeground
        // within seconds, whatever happens next. Taps on the notification's buttons arrive as
        // plain starts and need no such promise.
        if (intent?.action == null) goForeground(build())
        when (intent?.action) {
            ACT_TOGGLE -> MusicPlayer.togglePause()
            ACT_NEXT -> MusicPlayer.next()
            ACT_PREV -> MusicPlayer.previous()
            ACT_STOP -> MusicPlayer.stop()
        }
        refresh()
        return START_NOT_STICKY
    }

    /** Bring the notification up to date with the player (called on every state change). */
    fun refresh() {
        val nm = getSystemService(NotificationManager::class.java)
        if (MusicPlayer.current == null) {
            wake?.let { if (it.isHeld) it.release() }
            stopForeground(STOP_FOREGROUND_REMOVE)
            nm.cancel(NOTE_ID)
            stopSelf()
            return
        }
        val n = build()
        if (MusicPlayer.playing || MusicPlayer.loading) {
            goForeground(n)
            wake?.acquire(6 * 60 * 60 * 1000L)          // safety cap; released on pause/stop
        } else {
            wake?.let { if (it.isHeld) it.release() }
            stopForeground(STOP_FOREGROUND_DETACH)      // paused: keep it, but let it be swiped away
            nm.notify(NOTE_ID, n)
        }
    }

    private fun goForeground(n: Notification) {
        // Android can refuse a foreground start while the app is in the background (12+);
        // the notification is then simply posted as it is.
        runCatching {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q)
                startForeground(NOTE_ID, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK)
            else startForeground(NOTE_ID, n)
        }.onFailure { getSystemService(NotificationManager::class.java).notify(NOTE_ID, n) }
    }

    private fun pi(action: String, code: Int): PendingIntent =
        PendingIntent.getService(this, code, Intent(this, MusicService::class.java).setAction(action),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)

    private fun action(icon: Int, label: String, act: String, code: Int) =
        Notification.Action.Builder(Icon.createWithResource(this, icon), label, pi(act, code)).build()

    private fun build(): Notification {
        val t = MusicPlayer.current
        val open = PendingIntent.getActivity(this, 0,
            Intent(this, MainActivity::class.java)
                .setAction(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
                .putExtra(EXTRA_OPEN_MUSIC, true)
                .addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_REORDER_TO_FRONT),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
        val playing = MusicPlayer.playing || MusicPlayer.loading
        val b = Notification.Builder(this, CHANNEL)
            .setSmallIcon(R.drawable.ic_music_note)
            .setContentTitle(t?.title ?: "MobileWatch")
            .setContentText(listOfNotNull(t?.expansion, t?.composer).filter { it.isNotBlank() }
                .joinToString("  \u00b7  ").ifBlank { t?.fileName ?: "" })
            .setContentIntent(open)
            .setDeleteIntent(pi(ACT_STOP, 4))
            .setOngoing(playing)
            .setShowWhen(false)
            .setVisibility(Notification.VISIBILITY_PUBLIC)
            .addAction(action(R.drawable.ic_music_prev, "Previous", ACT_PREV, 1))
            .addAction(if (playing) action(R.drawable.ic_music_pause, "Pause", ACT_TOGGLE, 2)
                       else action(R.drawable.ic_music_play, "Play", ACT_TOGGLE, 2))
            .addAction(action(R.drawable.ic_music_next, "Next", ACT_NEXT, 3))
            .addAction(action(R.drawable.ic_music_close, "Close", ACT_STOP, 5))
            .setStyle(Notification.MediaStyle()
                .setMediaSession(MusicPlayer.sessionToken)
                .setShowActionsInCompactView(0, 1, 2))
        largeIcon()?.let { b.setLargeIcon(it) }
        return b.build()
    }

    private fun largeIcon(): Bitmap? {
        if (logo == null) logo = runCatching {
            val o = BitmapFactory.Options().apply { inJustDecodeBounds = true }
            BitmapFactory.decodeResource(resources, R.drawable.mobilewatch_logo, o)
            var s = 1
            while (o.outWidth / (s * 2) >= 256) s *= 2
            BitmapFactory.decodeResource(resources, R.drawable.mobilewatch_logo,
                BitmapFactory.Options().apply { inSampleSize = s })
        }.getOrNull()
        return logo
    }

    // Swiping MobileWatch away in Recents ends the music, as leaving the app does.
    override fun onTaskRemoved(rootIntent: Intent?) {
        MusicPlayer.stop()
        stopSelf()
    }

    override fun onDestroy() {
        wake?.let { if (it.isHeld) it.release() }
        instance = null
        super.onDestroy()
    }

    companion object {
        const val CHANNEL = "music"
        const val NOTE_ID = 4711
        const val EXTRA_OPEN_MUSIC = "open_music"
        private const val ACT_TOGGLE = "com.balladofworms.mobilewatch.music.TOGGLE"
        private const val ACT_NEXT = "com.balladofworms.mobilewatch.music.NEXT"
        private const val ACT_PREV = "com.balladofworms.mobilewatch.music.PREV"
        private const val ACT_STOP = "com.balladofworms.mobilewatch.music.STOP"

        @Volatile var instance: MusicService? = null
            private set

        /** Start the service (when playback begins from the app). */
        fun start(ctx: Context) {
            runCatching { ctx.startForegroundService(Intent(ctx, MusicService::class.java)) }
        }
    }
}
