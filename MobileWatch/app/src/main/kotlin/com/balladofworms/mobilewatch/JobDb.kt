package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class Job(val id: Int, val code: String, val name: String)
data class PetSection(val title: String, val items: List<JobSpell>)
/** One entry in a Beastmaster familiar's Ready list. `charges` is free text ("1 charge",
 *  "Not available via Ready"); `index` is the /bstpet number where a page publishes it. */
data class PetReady(val name: String, val charges: String, val desc: String,
                   val index: String, val skillchain: String = "")
data class Pet(
    val name: String, val sub: String, val sections: List<PetSection>,
    // Everything below is Beastmaster familiar detail and is empty for Summoner avatars.
    val family: String = "", val job: String = "", val level: String = "", val cap: String = "",
    val hp: String = "", val damage: String = "", val tp: String = "", val duration: String = "",
    // The Lv.99 jug pages add these: the familiar's ecosystem, attack/defence modifiers, and a
    // stat block measured at the pet's level cap. `stats` is label -> value, kept in page order.
    val eco: String = "", val atkMod: String = "", val defMod: String = "",
    val stats: List<Pair<String, String>> = emptyList(),
    val traits: List<String> = emptyList(),
    val notes: List<String> = emptyList(),
    val ready: List<PetReady> = emptyList(),
    // true when the page states the familiar HAS no Ready abilities, as opposed to us not
    // having recorded them yet. Absent key = unrecorded, explicit [] = genuinely none.
    val readyKnown: Boolean = false,
)
data class JobAbility(val name: String, val level: Int)
data class JobTrait(val name: String, val levels: String)   // e.g. "25, 50, 75"
data class JobSpell(val name: String, val level: String)   // "5" or "Gift"
data class SpellInfo(
    val type: String, val elem: String, val skill: String,
    val mp: Int, val cast: String, val recast: String,
    val jobs: List<Pair<String, String>>   // (jobcode, level)
)

private val STAT_ORDER = listOf(
    "hp" to "HP", "acc" to "Accuracy", "atk" to "Attack", "eva" to "Evasion", "def" to "Defense")

class JobDb private constructor(
    val jobs: List<Job>,
    private val abilities: Map<Int, List<JobAbility>>,
    private val traits: Map<Int, List<JobTrait>>,
    private val spells: Map<Int, List<JobSpell>>,
    private val rolls: Map<Int, List<JobAbility>>,
    private val spellInfo: Map<String, SpellInfo>,
    private val pets: Map<Int, List<Pet>>,
) {
    fun abilitiesFor(id: Int): List<JobAbility> = abilities[id] ?: emptyList()
    fun traitsFor(id: Int): List<JobTrait> = traits[id] ?: emptyList()
    fun spellsFor(id: Int): List<JobSpell> = spells[id] ?: emptyList()
    fun rollsFor(id: Int): List<JobAbility> = rolls[id] ?: emptyList()
    fun spellInfoFor(name: String): SpellInfo? = spellInfo[name]
    fun petsFor(id: Int): List<Pet> = pets[id] ?: emptyList()

    companion object {
        fun load(context: Context): JobDb {
            val text = context.assets.open("jobs.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)

            val jArr = root.getJSONArray("jobs")
            val jobs = (0 until jArr.length()).map {
                val o = jArr.getJSONObject(it)
                Job(o.getInt("id"), o.getString("code"), o.getString("name"))
            }

            val ab = HashMap<Int, List<JobAbility>>()
            val abObj = root.getJSONObject("abilities")
            for (job in jobs) {
                val arr = abObj.optJSONArray(job.id.toString()) ?: continue
                ab[job.id] = (0 until arr.length()).map {
                    val o = arr.getJSONObject(it); JobAbility(o.getString("n"), o.getInt("lv"))
                }
            }

            val tr = HashMap<Int, List<JobTrait>>()
            val trObj = root.getJSONObject("traits")
            for (job in jobs) {
                val arr = trObj.optJSONArray(job.id.toString()) ?: continue
                tr[job.id] = (0 until arr.length()).map {
                    val o = arr.getJSONObject(it); JobTrait(o.getString("n"), o.optString("lvs", o.optInt("lv").toString()))
                }
            }
            val sp = HashMap<Int, List<JobSpell>>()
            val spObj = root.optJSONObject("spells")
            if (spObj != null) for (job in jobs) {
                val arr = spObj.optJSONArray(job.id.toString()) ?: continue
                sp[job.id] = (0 until arr.length()).map {
                    val o = arr.getJSONObject(it); JobSpell(o.getString("n"), o.getString("l"))
                }
            }
            val rl = HashMap<Int, List<JobAbility>>()
            val rlObj = root.optJSONObject("rolls")
            if (rlObj != null) for (job in jobs) {
                val arr = rlObj.optJSONArray(job.id.toString()) ?: continue
                rl[job.id] = (0 until arr.length()).map {
                    val o = arr.getJSONObject(it); JobAbility(o.getString("n"), o.getInt("lv"))
                }
            }
            val si = HashMap<String, SpellInfo>()
            val siObj = root.optJSONObject("spellinfo")
            if (siObj != null) {
                val keys = siObj.keys()
                while (keys.hasNext()) {
                    val k = keys.next(); val o = siObj.getJSONObject(k)
                    val ja = o.optJSONArray("jobs")
                    val jl = if (ja != null) (0 until ja.length()).map {
                        val p = ja.getJSONArray(it); p.getString(0) to p.getString(1)
                    } else emptyList()
                    si[k] = SpellInfo(o.optString("type"), o.optString("elem"), o.optString("skill"),
                        o.optInt("mp"), o.optString("cast"), o.optString("recast"), jl)
                }
            }
            val pt = HashMap<Int, List<Pet>>()
            val ptObj = root.optJSONObject("pets")
            if (ptObj != null) for (job in jobs) {
                val arr = ptObj.optJSONArray(job.id.toString()) ?: continue
                pt[job.id] = (0 until arr.length()).map {
                    val po = arr.getJSONObject(it)
                    val secArr = po.optJSONArray("sections")
                    val secs = if (secArr != null) (0 until secArr.length()).map { si2 ->
                        val so = secArr.getJSONObject(si2)
                        val ia = so.getJSONArray("items")
                        PetSection(so.getString("t"), (0 until ia.length()).map { ii ->
                            val io = ia.getJSONObject(ii); JobSpell(io.getString("n"), io.getString("l"))
                        })
                    } else emptyList()
                    val rdArr = po.optJSONArray("ready")
                    val rd = if (rdArr != null) (0 until rdArr.length()).map { ri ->
                        val ro = rdArr.getJSONObject(ri)
                        PetReady(ro.optString("n"), ro.optString("c"), ro.optString("d"),
                            ro.optString("i"), ro.optString("sc"))
                    } else emptyList()
                    val trArr = po.optJSONArray("traits")
                    val tr2 = if (trArr != null) (0 until trArr.length()).map { ti -> trArr.getString(ti) }
                              else emptyList()
                    val ntArr = po.optJSONArray("notes")
                    val nt = if (ntArr != null) (0 until ntArr.length()).map { ni -> ntArr.getString(ni) }
                             else emptyList()
                    val stObj = po.optJSONObject("stats")
                    val st2 = if (stObj != null) STAT_ORDER.filter { stObj.has(it.first) }
                        .map { it.second to stObj.optString(it.first) } else emptyList()
                    Pet(po.getString("n"), po.optString("sub", ""), secs,
                        po.optString("fam"), po.optString("job"), po.optString("lvl"), po.optString("cap"),
                        po.optString("hp"), po.optString("dmg"), po.optString("tp"), po.optString("dur"),
                        po.optString("eco"), po.optString("atk"), po.optString("def"), st2,
                        tr2, nt, rd, po.has("ready"))
                }
            }
            return JobDb(jobs, ab, tr, sp, rl, si, pt)
        }
    }
}
