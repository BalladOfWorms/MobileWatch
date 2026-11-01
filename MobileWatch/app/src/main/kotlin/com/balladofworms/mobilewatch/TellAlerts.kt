package com.balladofworms.mobilewatch

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder

/**
 * Tell alerts: a notification on the phone when someone sends you a tell in game. Disconnect
 * alerts ride along: OmniWatch puts an "alert" line in the chat feed when a character drops
 * out of the game without logging out, and that becomes a notification too.
 *
 * While it's on, a small service keeps one request parked at OmniWatch (it answers the moment a
 * line arrives, or after 25 s with nothing), so a tell shows up within a second or two without the
 * phone asking over and over. It shows the quiet "Listening for tells" notification Android
 * requires for that. Tells from blocked names, and the ones you send, never alert; neither does a
 * tell while you're looking at the Tell tab.
 */
object TellAlerts {
    private const val P_ON = "tell_alerts"
    private const val P_DC = "dc_alerts"
    const val EXTRA_OPEN_TELLS = "open_tells"

    @Volatile var appVisible = false        // MainActivity is on screen
    @Volatile var tellTabOpen = false       // the Chat tab is showing tells

    fun isOn(ctx: Context): Boolean = prefs(ctx).getBoolean(P_ON, false)
    fun isDcOn(ctx: Context): Boolean = prefs(ctx).getBoolean(P_DC, false)
    /** Either kind of alert wanted: the service runs for both. */
    fun anyOn(ctx: Context): Boolean = isOn(ctx) || isDcOn(ctx)

    fun setOn(ctx: Context, on: Boolean) {
        prefs(ctx).edit().putBoolean(P_ON, on).apply()
        restart(ctx)
    }

    fun setDcOn(ctx: Context, on: Boolean) {
        prefs(ctx).edit().putBoolean(P_DC, on).apply()
        restart(ctx)
    }

    private fun restart(ctx: Context) {
        if (anyOn(ctx)) start(ctx) else ctx.stopService(Intent(ctx, TellAlertService::class.java))
    }

    /** Start listening if alerts are on and OmniWatch is paired. Safe to call any time the app is
     *  in front (Android only lets a foreground service start from there). */
    fun start(ctx: Context) {
        if (!anyOn(ctx) || CharLink.load(prefs(ctx)) == null) return
        runCatching { ctx.startForegroundService(Intent(ctx, TellAlertService::class.java)) }
    }

    fun stop(ctx: Context) { ctx.stopService(Intent(ctx, TellAlertService::class.java)) }

    internal fun prefs(ctx: Context) =
        ctx.getSharedPreferences("mobilewatch", Context.MODE_PRIVATE)

    /** The message part of an incoming tell ("Friendguy>> you up?" -> "you up?"). */
    fun body(text: String): String = text.replaceFirst(Regex("^[A-Za-z]{3,15}>>\\s?"), "")
}

class TellAlertService : Service() {
    @Volatile private var running = false
    private var worker: Thread? = null
    private val recent = HashMap<String, ArrayDeque<String>>()   // sender -> last few tells

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        val nm = getSystemService(NotificationManager::class.java)
        if (nm.getNotificationChannel(CH_TELLS) == null)
            nm.createNotificationChannel(NotificationChannel(CH_TELLS, "Tells", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "A tell sent to you in game"
            })
        if (nm.getNotificationChannel(CH_ALERTS) == null)
            nm.createNotificationChannel(NotificationChannel(CH_ALERTS, "Disconnects", NotificationManager.IMPORTANCE_HIGH).apply {
                description = "A character dropped out of the game"
            })
        if (nm.getNotificationChannel(CH_WATCH) == null)
            nm.createNotificationChannel(NotificationChannel(CH_WATCH, "Listening for tells", NotificationManager.IMPORTANCE_MIN).apply {
                description = "Shown while MobileWatch listens to OmniWatch for tells"
                setShowBadge(false)
            })
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        goForeground(listening())
        if (!running) {
            running = true
            worker = Thread({ loop() }, "tell-alerts").apply { isDaemon = true; start() }
        }
        return START_STICKY
    }

    override fun onDestroy() {
        running = false
        worker?.interrupt()
        super.onDestroy()
    }

    private fun goForeground(text: String) {
        val n = Notification.Builder(this, CH_WATCH)
            .setSmallIcon(R.drawable.ic_notify_mw)
            .setContentTitle("MobileWatch")
            .setContentText(text)
            .setContentIntent(openApp(0, false))
            .setOngoing(true)
            .setShowWhen(false)
            .build()
        runCatching {
            if (Build.VERSION.SDK_INT >= 34)
                startForeground(NOTE_WATCH, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_REMOTE_MESSAGING)
            else startForeground(NOTE_WATCH, n)
        }.onFailure { getSystemService(NotificationManager::class.java).notify(NOTE_WATCH, n) }
    }

    private fun listening(): String = when {
        TellAlerts.isOn(this) && TellAlerts.isDcOn(this) -> "Listening for tells and disconnects"
        TellAlerts.isDcOn(this) -> "Watching for disconnects"
        else -> "Listening for tells"
    }

    private fun openTells(code: Int): PendingIntent = openApp(code, true)

    private fun openApp(code: Int, tells: Boolean): PendingIntent =
        PendingIntent.getActivity(this, code,
            Intent(this, MainActivity::class.java)
                .setAction(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
                .putExtra(TellAlerts.EXTRA_OPEN_TELLS, tells)
                .addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_REORDER_TO_FRONT),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)

    private fun loop() {
        val prefs = TellAlerts.prefs(this)
        var boot = 0L
        var since = 0
        var started = System.currentTimeMillis() / 1000
        var down = false
        while (running) {
            val link = CharLink.load(prefs)
            if (link == null || !TellAlerts.anyOn(this)) { stopSelf(); return }
            val r = CharLink.chat(link, since, boot, waitSec = if (boot == 0L) 0 else 25)
            val b = r.value
            if (b == null) {
                if (r.fail == CharLink.Fail.BadCode) { stopSelf(); return }
                if (!down) { down = true; goForeground("Waiting for OmniWatch") }
                if (!sleep(15_000)) return
                continue
            }
            if (down) { down = false; goForeground(listening()) }
            if (b.boot != boot) {
                // First contact, or OmniWatch restarted: only tells newer than this service.
                val fresh = boot != 0L
                boot = b.boot
                if (!fresh) { since = b.seq; started = System.currentTimeMillis() / 1000; continue }
            }
            since = b.seq
            val blocked = b.blocked ?: prefs.getString("chat_blocked", "")!!.split('\n').filter { it.isNotBlank() }.toSet()
            for (l in b.lines) {
                if (l.ch == "alert") {
                    if (TellAlerts.isDcOn(this) && l.t >= started - 5) postAlert(l.text)
                    continue
                }
                if (!TellAlerts.isOn(this)) continue
                val from = l.from ?: continue
                if (l.ch != "tell" || l.self || l.t < started - 5) continue
                if (from.lowercase() in blocked) continue
                if (TellAlerts.appVisible && TellAlerts.tellTabOpen) continue
                post(from, TellAlerts.body(l.text))
            }
        }
    }

    private fun sleep(ms: Long): Boolean = try { Thread.sleep(ms); running } catch (e: InterruptedException) { false }

    private fun post(from: String, text: String) {
        val lines = recent.getOrPut(from.lowercase()) { ArrayDeque() }
        lines.addLast(text); while (lines.size > 5) lines.removeFirst()
        val style = Notification.InboxStyle().setBigContentTitle(from)
        lines.forEach { style.addLine(it) }
        val id = 2000 + (from.lowercase().hashCode() and 0x3FF)
        val n = Notification.Builder(this, CH_TELLS)
            .setSmallIcon(R.drawable.ic_notify_mw)
            .setColor(0xFFC0169E.toInt())     // the logo's magenta, behind the icon
            .setContentTitle(from)
            .setContentText(text)
            .setStyle(style)
            .setCategory(Notification.CATEGORY_MESSAGE)
            .setContentIntent(openTells(id))
            .setAutoCancel(true)
            .build()
        runCatching { getSystemService(NotificationManager::class.java).notify(id, n) }
    }

    private fun postAlert(text: String) {
        val id = 3000 + (text.hashCode() and 0x3FF)
        val n = Notification.Builder(this, CH_ALERTS)
            .setSmallIcon(R.drawable.ic_notify_mw)
            .setColor(0xFFC0169E.toInt())
            .setContentTitle(text)
            .setContentText("OmniWatch stopped hearing from the game.")
            .setCategory(Notification.CATEGORY_STATUS)
            .setContentIntent(openApp(id, false))
            .setAutoCancel(true)
            .build()
        runCatching { getSystemService(NotificationManager::class.java).notify(id, n) }
    }

    companion object {
        private const val CH_ALERTS = "dc_alerts"
        private const val CH_TELLS = "tells"
        private const val CH_WATCH = "tell_watch"
        private const val NOTE_WATCH = 1999
    }
}
