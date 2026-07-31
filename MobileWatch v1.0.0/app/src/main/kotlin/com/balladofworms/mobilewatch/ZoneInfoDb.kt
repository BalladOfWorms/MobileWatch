package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class TravelPoint(val name: String, val coord: String)
data class TransportRow(val board: String, val depart: String, val arrive: String)
data class ZoneTransport(val name: String, val rows: List<TransportRow>)
data class ZoneNm(val name: String, val level: String, val spawn: String, val drops: String)
data class ZoneMob(val name: String, val level: String)
data class ZoneQuest(val name: String, val fame: String, val npc: String, val reward: String)
data class ZoneAssault(val rank: String, val name: String, val objective: String)
data class ZoneReive(val name: String, val ki: String, val loc: String)
data class ZoneGeasGroup(val title: String, val rows: List<ZoneNm>)
data class ZoneBattle(val name: String, val type: String, val cap: String)
data class ZoneProcRow(val types: String, val w1: String, val w2: String, val w3: String, val currency: String, val jobs: String)
data class ZoneInfo(
    val continent: String,
    val banner: String,
    val footprint: String,
    val apparatus: String,
    val weatherOverride: String,
    val regionOverride: String,
    val type: String,
    val travel: List<TravelPoint>,
    val connects: List<String>,
    val transport: List<ZoneTransport>,
    val nms: List<ZoneNm>,
    val mobs: List<ZoneMob>,
    val quests: List<ZoneQuest>,
    val battlefields: List<ZoneBattle>,
    val nomap: Boolean,
    val assaults: List<ZoneAssault> = emptyList(),
    val reives: List<ZoneReive> = emptyList(),
    val geasfete: List<ZoneGeasGroup> = emptyList(),
    val procs: List<ZoneProcRow> = emptyList(),
    val notes: List<String> = emptyList(),
)

class ZoneInfoDb private constructor(private val map: Map<String, ZoneInfo>) {
    fun forSlug(slug: String): ZoneInfo? = map[slug]

    companion object {
        fun load(context: Context): ZoneInfoDb {
            val out = HashMap<String, ZoneInfo>()
            runCatching {
                val text = context.assets.open("zoneinfo.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val root = JSONObject(text)
                val keys = root.keys()
                while (keys.hasNext()) {
                    val slug = keys.next(); val o = root.getJSONObject(slug)
                    val tArr = o.optJSONArray("travel")
                    val travel = if (tArr != null) (0 until tArr.length()).map {
                        val t = tArr.getJSONObject(it); TravelPoint(t.optString("n"), t.optString("c"))
                    } else emptyList()
                    val cArr = o.optJSONArray("connects")
                    val connects = if (cArr != null) (0 until cArr.length()).map {
                        val el = cArr.opt(it)
                        if (el is JSONObject) el.optString("n") else el.toString()
                    }.filter { it.isNotBlank() } else emptyList()
                    val trArr = o.optJSONArray("transport")
                    val transport = if (trArr != null) (0 until trArr.length()).map {
                        val t = trArr.getJSONObject(it)
                        val rArr = t.optJSONArray("rows")
                        val rows = if (rArr != null) (0 until rArr.length()).map { j ->
                            val r = rArr.getJSONObject(j)
                            TransportRow(r.optString("b"), r.optString("d"), r.optString("a"))
                        } else emptyList()
                        ZoneTransport(t.optString("n"), rows)
                    } else emptyList()
                    val nArr = o.optJSONArray("nms")
                    val nms = if (nArr != null) (0 until nArr.length()).map {
                        val n = nArr.getJSONObject(it)
                        ZoneNm(n.optString("n"), n.optString("lv"), n.optString("spawn"), n.optString("drops"))
                    } else emptyList()
                    val mArr = o.optJSONArray("mobs")
                    val mobs = if (mArr != null) (0 until mArr.length()).map {
                        val el = mArr.opt(it)
                        if (el is JSONObject) ZoneMob(el.optString("n"), el.optString("lv"))
                        else ZoneMob(el.toString(), "")
                    } else emptyList()
                    val qArr = o.optJSONArray("quests")
                    val quests = if (qArr != null) (0 until qArr.length()).map {
                        val q = qArr.getJSONObject(it)
                        ZoneQuest(q.optString("n"), q.optString("fame"), q.optString("npc"), q.optString("reward"))
                    } else emptyList()
                    val bArr = o.optJSONArray("battlefields")
                    val battlefields = if (bArr != null) (0 until bArr.length()).map {
                        val b = bArr.getJSONObject(it)
                        ZoneBattle(b.optString("n"), b.optString("type"), b.optString("cap"))
                    } else emptyList()
                    val asArr = o.optJSONArray("assaults")
                    val assaults = if (asArr != null) (0 until asArr.length()).map {
                        val a = asArr.getJSONObject(it)
                        ZoneAssault(a.optString("r"), a.optString("n"), a.optString("o"))
                    } else emptyList()
                    val rvArr = o.optJSONArray("reives")
                    val reives = if (rvArr != null) (0 until rvArr.length()).map {
                        val r = rvArr.getJSONObject(it)
                        ZoneReive(r.optString("n"), r.optString("ki"), r.optString("loc"))
                    } else emptyList()
                    val gfArr = o.optJSONArray("geasfete")
                    val geasfete = if (gfArr != null) (0 until gfArr.length()).map {
                        val g = gfArr.getJSONObject(it)
                        val grArr = g.optJSONArray("rows")
                        val rows = if (grArr != null) (0 until grArr.length()).map { j ->
                            val n = grArr.getJSONObject(j)
                            ZoneNm(n.optString("n"), n.optString("lv"), n.optString("spawn"), n.optString("drops"))
                        } else emptyList()
                        ZoneGeasGroup(g.optString("t"), rows)
                    } else emptyList()
                    val pArr = o.optJSONArray("procs")
                    val procs = if (pArr != null) (0 until pArr.length()).map {
                        val p = pArr.getJSONObject(it)
                        ZoneProcRow(p.optString("t"), p.optString("w1"), p.optString("w2"), p.optString("w3"), p.optString("cur"), p.optString("jobs"))
                    } else emptyList()
                    val noArr = o.optJSONArray("notes")
                    val notes = if (noArr != null) (0 until noArr.length()).map {
                        noArr.optString(it)
                    }.filter { it.isNotBlank() } else emptyList()
                    out[slug] = ZoneInfo(o.optString("continent"), o.optString("banner"), o.optString("footprint"), o.optString("apparatus"), o.optString("weather"), o.optString("region"), o.optString("type"), travel, connects, transport, nms, mobs, quests, battlefields, o.optBoolean("nomap", false), assaults, reives, geasfete, procs, notes)
                }
            }
            return ZoneInfoDb(out)
        }
    }
}
