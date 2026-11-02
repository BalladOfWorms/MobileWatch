package com.balladofworms.mobilewatch

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

/**
 * The link to OmniWatch on the PC, for the Character tab.
 *
 * OmniWatch keeps a gear snapshot per character (everything that character owns that can be
 * equipped, with augments, plus job levels and what was last worn on each job) and serves it
 * from a small web server inside the overlay. The phone reaches it on the PC's address -- same
 * Wi-Fi, or over Tailscale -- and every request carries the pairing code OmniWatch shows in
 * Settings > MobileWatch (just above Exit).
 *
 * Each snapshot fetched is kept in the app's own storage, so the tab still shows your gear when
 * the PC is off; the next successful fetch replaces it.
 */
object CharLink {
    const val DEFAULT_PORT = 47321
    private const val P_ADDR = "charlink_addr"
    private const val P_CODE = "charlink_code"
    private const val P_SEL = "charlink_sel"

    data class Link(val address: String, val code: String)

    sealed class Fail {
        object BadCode : Fail()
        object Unreachable : Fail()
        object NoSnapshot : Fail()
    }

    class Result<T>(val value: T?, val fail: Fail?)

    fun load(prefs: SharedPreferences): Link? {
        val a = prefs.getString(P_ADDR, null) ?: return null
        val c = prefs.getString(P_CODE, null) ?: return null
        return if (a.isBlank() || c.isBlank()) null else Link(a, c)
    }

    fun save(prefs: SharedPreferences, link: Link) {
        prefs.edit().putString(P_ADDR, link.address).putString(P_CODE, link.code).apply()
    }

    fun clear(prefs: SharedPreferences) {
        prefs.edit().remove(P_ADDR).remove(P_CODE).apply()
    }

    fun savedCharacter(prefs: SharedPreferences): String? = prefs.getString(P_SEL, null)
    fun saveCharacter(prefs: SharedPreferences, name: String) { prefs.edit().putString(P_SEL, name).apply() }

    /** "192.168.50.20", "http://192.168.50.20:47321/" and "100.82.241.13:47321" all become
     *  host:port. The port is added when it was left off. */
    fun normalizeAddress(raw: String): String {
        var a = raw.trim().removePrefix("http://").removePrefix("https://").trimEnd('/')
        a = a.substringBefore('/')
        if (a.isEmpty()) return ""
        val hasPort = a.substringAfterLast(':', "").let { it.isNotEmpty() && it.all(Char::isDigit) }
        return if (hasPort) a else "$a:$DEFAULT_PORT"
    }

    /** What people type: "x2zy-4n3u", "X2ZY 4N3U". The PC compares letters and digits only. */
    fun normalizeCode(raw: String): String = raw.filter { it.isLetterOrDigit() }.uppercase()

    private fun open(link: Link, path: String, etag: String? = null, readMs: Int = 10000): HttpURLConnection =
        (URL("http://${link.address}$path").openConnection() as HttpURLConnection).apply {
            connectTimeout = 4000
            readTimeout = readMs
            useCaches = false
            setRequestProperty("X-OmniWatch-Code", link.code)
            if (etag != null) setRequestProperty("If-None-Match", etag)
        }

    /** The characters OmniWatch has a gear snapshot for. Call off the main thread. */
    fun hello(link: Link): Result<List<String>> = try {
        val c = open(link, "/mw/v1/hello")
        try {
            when (c.responseCode) {
                200 -> {
                    val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                    val arr = o.optJSONArray("characters")
                    val names = ArrayList<String>()
                    if (arr != null) for (i in 0 until arr.length())
                        arr.optJSONObject(i)?.optString("name")?.takeIf { it.isNotBlank() }?.let { names.add(it) }
                    Result(names, null)
                }
                401 -> Result(null, Fail.BadCode)
                else -> Result(null, Fail.Unreachable)
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        Result(null, Fail.Unreachable)
    }

    /**
     * Fetch one character's snapshot, sending the "updated" stamp of the copy we already hold so an
     * unchanged snapshot costs nothing. Returns the new snapshot, or the cached one when nothing
     * changed. Saves a new one to the cache. Call off the main thread.
     */
    fun fetchGear(ctx: Context, link: Link, name: String): Result<GearSnapshot> {
        val cached = cached(ctx, name)
        return try {
            val path = "/mw/v1/gear/" + URLEncoder.encode(name, "UTF-8")
            val c = open(link, path, cached?.let { "\"${it.updated}\"" })
            try {
                when (c.responseCode) {
                    200 -> {
                        val text = c.inputStream.bufferedReader().use { it.readText() }
                        val snap = parse(text)
                        if (snap == null) Result(cached, Fail.Unreachable) else {
                            writeCache(ctx, name, text)
                            Result(snap, null)
                        }
                    }
                    304 -> Result(cached, null)
                    401 -> Result(cached, Fail.BadCode)
                    404 -> Result(cached, Fail.NoSnapshot)
                    else -> Result(cached, Fail.Unreachable)
                }
            } finally { c.disconnect() }
        } catch (e: Exception) {
            Result(cached, Fail.Unreachable)
        }
    }

    /** Chat lines after [since] from OmniWatch's run [boot]; a different run sends everything.
     *  Call off the main thread. */
    /** Lines after [since]. With [waitSec], OmniWatch holds the request until a line arrives or
     *  that long passes, which is how tell alerts listen without asking every few seconds. */
    fun chat(link: Link, since: Int, boot: Long, waitSec: Int = 0): Result<ChatBatch> = try {
        val c = open(link, "/mw/v1/chat?since=$since&boot=$boot" + if (waitSec > 0) "&wait=$waitSec" else "",
            readMs = 10000 + waitSec * 1000)
        try {
            when (c.responseCode) {
                200 -> {
                    val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                    val arr = o.optJSONArray("lines")
                    val lines = ArrayList<ChatLine>()
                    if (arr != null) for (i in 0 until arr.length()) arr.optJSONObject(i)?.let { l ->
                        lines.add(ChatLine(
                            seq = l.optInt("seq"), ch = l.optString("ch"), t = l.optLong("t"),
                            text = l.optString("text"), self = l.optBoolean("self"),
                            from = l.optString("from").ifBlank { null }, to = l.optString("to").ifBlank { null }))
                    }
                    val bl = o.optJSONArray("blocked")?.let { a -> (0 until a.length()).map { a.optString(it).lowercase() }.filter { it.isNotBlank() }.toSet() }
                    Result(ChatBatch(o.optLong("boot"), o.optInt("seq"), lines, bl), null)
                }
                401 -> Result(null, Fail.BadCode)
                else -> Result(null, Fail.Unreachable)
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        Result(null, Fail.Unreachable)
    }

    /** Say [text] in game on [ch] ("tell", "shout", "say", "yell", "ls1", "ls2"). Returns null when OmniWatch
     *  took it, else what went wrong in words. Call off the main thread. */
    fun sendChat(link: Link, ch: String, to: String, text: String): String? = try {
        val body = JSONObject().apply { put("ch", ch); put("to", to); put("text", text) }.toString().toByteArray()
        val c = open(link, "/mw/v1/chat/send").apply {
            requestMethod = "POST"; doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setFixedLengthStreamingMode(body.size)
        }
        try {
            c.outputStream.use { it.write(body) }
            when (c.responseCode) {
                200 -> null
                401 -> "OmniWatch didn't accept the code."
                else -> when (runCatching { JSONObject(c.errorStream.bufferedReader().use { it.readText() }).optString("error") }.getOrNull()) {
                    "no_target" -> "Who's the tell for?"
                    "empty" -> "Nothing to send."
                    else -> "OmniWatch couldn't send that."
                }
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        "Can't reach OmniWatch."
    }

    /** Change OmniWatch's chat blacklist (shared with its chat panel). Returns the whole list as
     *  OmniWatch now has it (lowercase), or null when it couldn't be reached. */
    fun setBlocked(link: Link, add: Collection<String>, remove: Collection<String>): Set<String>? = try {
        val body = JSONObject().apply {
            put("add", org.json.JSONArray(add.toList())); put("remove", org.json.JSONArray(remove.toList()))
        }.toString().toByteArray()
        val c = open(link, "/mw/v1/blocked").apply {
            requestMethod = "POST"; doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setFixedLengthStreamingMode(body.size)
        }
        try {
            c.outputStream.use { it.write(body) }
            if (c.responseCode != 200) null else {
                val a = JSONObject(c.inputStream.bufferedReader().use { it.readText() }).optJSONArray("blocked")
                a?.let { (0 until it.length()).map { i -> it.optString(i).lowercase() }.filter { n -> n.isNotBlank() }.toSet() } ?: emptySet()
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        null
    }

    /** The Marketplace as OmniWatch has it. null when it couldn't be reached. */
    fun market(link: Link): Market? = try {
        val c = open(link, "/mw/v1/market")
        try {
            if (c.responseCode != 200) null else {
                val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                fun objs(a: org.json.JSONArray?) = a?.let { (0 until it.length()).mapNotNull { i -> it.optJSONObject(i) } }.orEmpty()
                fun items(a: org.json.JSONArray?, priceKey: String) = objs(a).map { j ->
                    MarketItem(j.optInt("id"), j.optString("name"), j.optInt("count", 1),
                        j.optInt("stack", 1), j.optLong(priceKey), j.optInt("slot"))
                }
                val sales = objs(o.optJSONArray("sales")).map { j ->
                    MarketSale(j.optInt("slot"), j.optString("status"), j.optString("name"), j.optInt("id"),
                        j.optInt("count", 1), j.optLong("price"),
                        if (j.isNull("left")) null else j.optLong("left"))
                }
                val buy = objs(o.optJSONArray("buy")).map { j ->
                    BuyRow(j.optInt("id"), j.optString("name"), j.optInt("level"), j.optInt("stack") == 1,
                        j.optInt("ssize", 1), if (j.has("avail")) j.optInt("avail") else null)
                }
                val queue = objs(o.optJSONArray("queue")).map { j ->
                    BuyQueued(j.optInt("id"), j.optString("name"), j.optInt("qty"), j.optLong("start"),
                        j.optLong("max"), j.optLong("inc"), j.optInt("stack") == 1, j.optString("status"))
                }
                val box = o.optJSONObject("dbox")?.let { d ->
                    fun slots(k: String) = objs(d.optJSONArray(k)).map { j ->
                        BoxSlot(j.optInt("slot"), j.optInt("id"), j.optLong("count"), j.optString("name"),
                            j.optString("who"), j.optBoolean("gil"))
                    }
                    DeliveryBox(d.optString("open"), d.optBoolean("busy"), d.optString("box", "in"),
                        d.optString("note"), slots("in"), slots("out"), items(d.optJSONArray("inv"), "price"))
                }
                val log = o.optJSONArray("log")?.let { a -> (0 until a.length()).map { a.optString(it) } }.orEmpty()
                Market(o.optString("character"), if (o.isNull("gil") || !o.has("gil")) null else o.optLong("gil"),
                    sales, items(o.optJSONArray("ah_inv"), "price"), items(o.optJSONArray("bazaar"), "bazaar"),
                    items(o.optJSONArray("bazaar_inv"), "bazaar"), o.optString("search"), buy, queue,
                    o.optBoolean("running"), box, log, o.optInt("log_seq"))
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        null
    }

    /** Ask OmniWatch to refresh, list, cancel or price ([body] has "action"). null when it took it,
     *  else what went wrong in words. Call off the main thread. */
    fun marketAct(link: Link, body: JSONObject): String? = try {
        val bytes = body.toString().toByteArray()
        val c = open(link, "/mw/v1/market").apply {
            requestMethod = "POST"; doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setFixedLengthStreamingMode(bytes.size)
        }
        try {
            c.outputStream.use { it.write(bytes) }
            when (c.responseCode) {
                200 -> null
                401 -> "OmniWatch didn't accept the code."
                else -> "OmniWatch couldn't do that."
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        "Can't reach OmniWatch."
    }

    /** Sync jobs: [action] "start" or "cancel", or null just to read where it is. null when
     *  OmniWatch couldn't be reached. Call off the main thread. */
    fun jobSync(link: Link, action: String?): JobSync? = try {
        val c = open(link, "/mw/v1/jobsync")
        if (action != null) {
            val body = JSONObject().apply { put("action", action) }.toString().toByteArray()
            c.requestMethod = "POST"; c.doOutput = true
            c.setRequestProperty("Content-Type", "application/json")
            c.setFixedLengthStreamingMode(body.size)
            c.outputStream.use { it.write(body) }
        }
        try {
            if (c.responseCode != 200) null else {
                val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                fun list(k: String) = o.optJSONArray(k)?.let { a -> (0 until a.length()).map { a.optString(it) } }.orEmpty()
                JobSync(o.optString("state"), o.optInt("done"), o.optInt("total"), o.optString("job"),
                    o.optString("error"), list("skipped"), list("saved"))
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        null
    }

    /** Send the phone's quest ticks (section -> lowercase names) and get OmniWatch's back. Both sides
     *  end up with every tick either had. null when OmniWatch couldn't be reached or was busy. */
    fun syncQuests(link: Link, ticks: Map<String, Set<String>>): QuestSync? = try {
        val t = JSONObject()
        ticks.forEach { (k, v) -> t.put(k, org.json.JSONArray(v.toList())) }
        val body = JSONObject().apply { put("ticks", t) }.toString().toByteArray()
        val c = open(link, "/mw/v1/quests").apply {
            requestMethod = "POST"; doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setFixedLengthStreamingMode(body.size)
        }
        try {
            c.outputStream.use { it.write(body) }
            if (c.responseCode != 200) null else {
                val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                val out = HashMap<String, Set<String>>()
                o.optJSONObject("ticks")?.let { m -> m.keys().forEach { k ->
                    val a = m.optJSONArray(k) ?: return@forEach
                    out[k] = (0 until a.length()).map { a.optString(it).lowercase() }.filter { it.isNotBlank() }.toSet()
                } }
                QuestSync(o.optString("character"), out, o.optInt("added"), o.optInt("unmatched"))
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        null
    }

    /** Missions and mounts: send the phone's ticks (checklist key -> ids) and get OmniWatch's back,
     *  including the mounts it has seen you own. null when it couldn't be reached or was busy. */
    fun syncChecklist(link: Link, cats: Map<String, Set<String>>): QuestSync? = try {
        val t = JSONObject()
        cats.forEach { (k, v) -> t.put(k, org.json.JSONArray(v.toList())) }
        val body = JSONObject().apply { put("cats", t) }.toString().toByteArray()
        val c = open(link, "/mw/v1/checklist").apply {
            requestMethod = "POST"; doOutput = true
            setRequestProperty("Content-Type", "application/json")
            setFixedLengthStreamingMode(body.size)
        }
        try {
            c.outputStream.use { it.write(body) }
            if (c.responseCode != 200) null else {
                val o = JSONObject(c.inputStream.bufferedReader().use { it.readText() })
                val out = HashMap<String, Set<String>>()
                o.optJSONObject("cats")?.let { m -> m.keys().forEach { k ->
                    val a = m.optJSONArray(k) ?: return@forEach
                    out[k] = (0 until a.length()).map { a.optString(it).lowercase() }.filter { it.isNotBlank() }.toSet()
                } }
                QuestSync(o.optString("character"), out, o.optInt("added"), o.optInt("unmatched"))
            }
        } finally { c.disconnect() }
    } catch (e: Exception) {
        null
    }

    private fun cacheDir(ctx: Context) = File(ctx.filesDir, "charlink").apply { mkdirs() }
    private fun safe(name: String) = name.filter { it.isLetterOrDigit() }

    private fun writeCache(ctx: Context, name: String, text: String) {
        runCatching {
            val f = File(cacheDir(ctx), safe(name) + ".json")
            val tmp = File(f.path + ".tmp")
            tmp.writeText(text)
            if (!tmp.renameTo(f)) { f.delete(); tmp.renameTo(f) }
        }
    }

    fun cached(ctx: Context, name: String): GearSnapshot? = runCatching {
        val f = File(cacheDir(ctx), safe(name) + ".json")
        if (f.isFile) parse(f.readText()) else null
    }.getOrNull()

    /** Characters we have a saved snapshot for, for when the PC can't be reached. */
    fun cachedCharacters(ctx: Context): List<String> =
        cacheDir(ctx).listFiles()?.filter { it.name.endsWith(".json") }
            ?.mapNotNull { f -> runCatching { JSONObject(f.readText()).optString("character") }.getOrNull()
                ?.takeIf { it.isNotBlank() } }?.sorted() ?: emptyList()

    fun forget(ctx: Context) { runCatching { cacheDir(ctx).deleteRecursively() } }

    fun parse(text: String): GearSnapshot? = runCatching {
        val o = JSONObject(text)
        fun owned(j: JSONObject): OwnedItem {
            val a = j.optJSONArray("augs")
            val augs = if (a == null) emptyList() else (0 until a.length()).map { a.optString(it) }.filter { it.isNotBlank() }
            return OwnedItem(j.optInt("id"), j.optInt("bag"), j.optInt("idx"), augs)
        }
        val levels = LinkedHashMap<String, Int>()
        o.optJSONObject("job_levels")?.let { jl -> jl.keys().forEach { k -> levels[k.uppercase()] = jl.optInt(k) } }
        val bags = HashMap<Int, String>()
        o.optJSONObject("bags")?.let { b -> b.keys().forEach { k -> k.toIntOrNull()?.let { bags[it] = b.optString(k) } } }
        val items = ArrayList<OwnedItem>()
        o.optJSONArray("items")?.let { arr -> for (i in 0 until arr.length()) arr.optJSONObject(i)?.let { items.add(owned(it)) } }
        val jobGear = HashMap<String, Map<String, OwnedItem>>()
        o.optJSONObject("job_gear")?.let { jg ->
            jg.keys().forEach { job ->
                val slots = HashMap<String, OwnedItem>()
                jg.optJSONObject(job)?.let { s -> s.keys().forEach { slot -> s.optJSONObject(slot)?.let { slots[slot] = owned(it) } } }
                jobGear[job.uppercase()] = slots
            }
        }
        val jobStats = HashMap<String, JobStats>()
        o.optJSONObject("job_stats")?.let { js ->
            js.keys().forEach { job ->
                val e = js.optJSONObject(job) ?: return@forEach
                val st = HashMap<String, Double>()
                e.optJSONObject("stats")?.let { m -> m.keys().forEach { k -> st[k] = m.optDouble(k, 0.0) } }
                val worn = HashMap<String, OwnedItem>()
                e.optJSONObject("worn")?.let { w -> w.keys().forEach { slot -> w.optJSONObject(slot)?.let { worn[slot] = owned(it) } } }
                jobStats[job.uppercase()] = JobStats(e.optString("sub").uppercase(), st, worn)
            }
        }
        val inv = ArrayList<InvItem>()
        o.optJSONArray("inventory")?.let { a -> for (i in 0 until a.length()) a.optJSONObject(i)?.let { j ->
            inv.add(InvItem(j.optInt("id"), j.optInt("bag"), j.optInt("idx"), j.optInt("n", 1)))
        } }
        val caps = HashMap<Int, Pair<Int, Int>>()
        o.optJSONObject("bag_caps")?.let { c -> c.keys().forEach { k ->
            val a = c.optJSONArray(k)
            if (a != null && a.length() >= 2) k.toIntOrNull()?.let { caps[it] = a.optInt(0) to a.optInt(1) }
        } }
        val gil = o.optLong("gil", -1L).takeIf { it >= 0 }
        GearSnapshot(
            character = o.optString("character"),
            mainJob = o.optString("main_job").uppercase(),
            subJob = o.optString("sub_job").uppercase(),
            jobLevels = levels,
            bags = bags,
            items = items,
            jobGear = jobGear,
            updated = o.optLong("updated"),
            jobStats = jobStats,
            inventory = inv,
            bagCaps = caps,
            gil = gil,
        )
    }.getOrNull()
}

/** One line of chat from OmniWatch. from/to are set on tells: who sent it, or who it went to. */
/** One of your seven auction house sale slots. left: seconds until an unsold listing comes back. */
data class MarketSale(val slot: Int, val status: String, val name: String, val id: Int, val count: Int,
                      val price: Long, val left: Long?)

/** An item in the Marketplace: in your bazaar (price > 0) or one you could list or send. slot is its
 *  place in your inventory, where that matters (sending). */
data class MarketItem(val id: Int, val name: String, val count: Int, val stack: Int = 1, val price: Long = 0,
                      val slot: Int = 0)

/** An auction house search result. stack: this row is the stack listing; avail: how many are up. */
data class BuyRow(val id: Int, val name: String, val level: Int, val stack: Boolean, val ssize: Int, val avail: Int?)

/** One line of the buy queue. */
data class BuyQueued(val id: Int, val name: String, val qty: Int, val start: Long, val max: Long, val inc: Long,
                     val stack: Boolean, val status: String)

/** One delivery box slot. gil: it's gil, count is the amount. */
data class BoxSlot(val slot: Int, val id: Int, val count: Long, val name: String, val who: String, val gil: Boolean)

data class DeliveryBox(val open: String, val busy: Boolean, val box: String, val note: String,
                       val inbox: List<BoxSlot>, val outbox: List<BoxSlot>, val inv: List<MarketItem>)

/** The Marketplace tab: OmniWatch's AH window (Buy, Sell with the bazaar, Delivery). */
data class Market(val character: String, val gil: Long?, val sales: List<MarketSale>, val ahInv: List<MarketItem>,
                  val bazaar: List<MarketItem>, val bazaarInv: List<MarketItem>,
                  val search: String, val buy: List<BuyRow>, val queue: List<BuyQueued>, val running: Boolean,
                  val box: DeliveryBox?, val log: List<String>, val logSeq: Int)

/** Where Sync jobs is: state is idle, starting, running, done, cancelled or error. */
data class JobSync(val state: String, val done: Int, val total: Int, val job: String,
                   val error: String, val skipped: List<String>, val saved: List<String>) {
    val busy: Boolean get() = state == "starting" || state == "running"
}

data class ChatLine(val seq: Int, val ch: String, val t: Long, val text: String, val self: Boolean,
                    val from: String?, val to: String?)

class ChatBatch(val boot: Long, val seq: Int, val lines: List<ChatLine>,
                val blocked: Set<String>? = null)   // OmniWatch's chat blacklist, lowercase (null: older OmniWatch)

/** One owned copy of an item, located by bag and slot so augmented copies stay apart. */
data class OwnedItem(val id: Int, val bag: Int, val idx: Int, val augs: List<String>)

data class GearSnapshot(
    val character: String,
    val mainJob: String,
    val subJob: String,
    val jobLevels: Map<String, Int>,
    val bags: Map<Int, String>,
    val items: List<OwnedItem>,
    val jobGear: Map<String, Map<String, OwnedItem>>,
    val updated: Long,
    val jobStats: Map<String, JobStats> = emptyMap(),
    val inventory: List<InvItem> = emptyList(),      // every item in every bag, with its count
    val bagCaps: Map<Int, Pair<Int, Int>> = emptyMap(),   // bag -> used, max
    val gil: Long? = null,
)

/** One stack in a bag, gear or not. */
data class InvItem(val id: Int, val bag: Int, val idx: Int, val count: Int)

/** What a quest sync with OmniWatch came back with. */
class QuestSync(val character: String, val ticks: Map<String, Set<String>>, val added: Int, val unmatched: Int)

/** What OmniWatch's Statistics panel read on a job, and the gear that was worn when it did:
 *  the phone shows these numbers for that gear and moves them by its own gear sums for any other.
 *  Keys are OmniWatch's ("accuracy", "physical damage taken", "tp per hit"...). */
data class JobStats(val sub: String, val stats: Map<String, Double>, val worn: Map<String, OwnedItem>)

/** The equipment grid, in the game's own 4x4 order, with each slot's bit in the item slot mask. */
object GearSlots {
    data class Slot(val key: String, val label: String, val bit: Int)

    val GRID: List<Slot> = listOf(
        Slot("main", "Main", 0), Slot("sub", "Sub", 1), Slot("range", "Range", 2), Slot("ammo", "Ammo", 3),
        Slot("head", "Head", 4), Slot("neck", "Neck", 9), Slot("left_ear", "Ear 1", 11), Slot("right_ear", "Ear 2", 12),
        Slot("body", "Body", 5), Slot("hands", "Hands", 6), Slot("left_ring", "Ring 1", 13), Slot("right_ring", "Ring 2", 14),
        Slot("back", "Back", 15), Slot("waist", "Waist", 10), Slot("legs", "Legs", 7), Slot("feet", "Feet", 8),
    )

    fun slot(key: String): Slot? = GRID.firstOrNull { it.key == key }

    /** Job abbreviation -> its bit in the item jobs mask (WAR = 1 ... RUN = 22). */
    val JOB_ORDER = listOf(
        "WAR", "MNK", "WHM", "BLM", "RDM", "THF", "PLD", "DRK", "BST", "BRD", "RNG",
        "SAM", "NIN", "DRG", "SMN", "BLU", "COR", "PUP", "DNC", "SCH", "GEO", "RUN"
    )
    fun jobBit(job: String): Int = JOB_ORDER.indexOf(job.uppercase()).let { if (it < 0) -1 else it + 1 }

    /** Bags you can equip straight out of: Inventory and the Mog Wardrobes. */
    private val EQUIP_BAGS = setOf(0, 8, 10, 11, 12, 13, 14, 15, 16)
    fun canEquipFrom(bag: Int) = bag in EQUIP_BAGS
}
