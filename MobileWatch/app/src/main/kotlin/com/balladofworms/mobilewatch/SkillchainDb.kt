package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class WeaponSkill(
    val id: Int, val name: String, val type: String, val props: List<String>, val aeonic: String? = null
) {
    /** Properties this WS can CLOSE with (adds the aeonic Light/Darkness close if it's an aeonic WS). */
    val closingProps: List<String> get() = if (aeonic != null) props + aeonic else props
}

data class SkillchainResult(
    val name: String,
    val level: Int,
    val elements: List<String>,   // magic-burst elements
    val viaFirst: String,         // closing property of WS1
    val viaSecond: String,        // opening property of WS2
)

class SkillchainDb private constructor(
    val weaponSkills: List<WeaponSkill>,
    private val chains: Map<String, Pair<Int, List<String>>>,        // name -> (level, elements)
    private val combos: Map<String, Map<String, Pair<String, Int>>>, // first -> second -> (result, level)
) {
    val types: List<String> = listOf("All") + weaponSkills.map { it.type }.distinct().sortedBy { it }

    /** Name -> WS, so the weapon-skill reference list can pull chain properties without duplicating them. */
    private val byName: Map<String, WeaponSkill> = weaponSkills.associateBy { it.name }

    fun wsByName(name: String): WeaponSkill? = byName[name]

    fun search(query: String, type: String): List<WeaponSkill> {
        val q = query.trim().lowercase()
        return weaponSkills.filter {
            (type == "All" || it.type == type) && (q.isEmpty() || it.name.lowercase().contains(q))
        }
    }

    /** True if any opener property combines with any closer property. */
    fun chainsInto(openers: List<String>, closers: List<String>): Boolean {
        for (a in openers) for (b in closers) if (combos[a]?.containsKey(b) == true) return true
        return false
    }

    /** Best skillchain from any opener property into a closer WS, or null. */
    private fun bestCombo(openers: List<String>, closer: WeaponSkill): SkillchainResult? {
        var best: Triple<String, Int, Pair<String, String>>? = null   // result, level, (opener, closer)
        for (pa in openers) for (pb in closer.closingProps) {
            val r = combos[pa]?.get(pb) ?: continue
            // A level-4 Light/Darkness closed via the WS's AEONIC property becomes
            // Radiance/Umbra (needs the aeonic weapon). A normal Light/Darkness close
            // stays Light/Darkness Lv 4.
            var name = r.first
            if (r.second == 4 && pb == closer.aeonic) {
                name = when (name) { "Light" -> "Radiance"; "Darkness" -> "Umbra"; else -> name }
            }
            if (best == null || r.second > best!!.second) best = Triple(name, r.second, pa to pb)
        }
        val res = best ?: return null
        return SkillchainResult(res.first, res.second, chains[res.first]?.second ?: emptyList(),
            res.third.first, res.third.second)
    }

    /**
     * Chain a sequence of weaponskills (WS1 opens, WS2 closes, WS3/WS4 continue).
     * Returns one result per successful step; stops when a step can't chain.
     */
    fun chain(seq: List<WeaponSkill>): List<SkillchainResult> {
        val out = ArrayList<SkillchainResult>()
        if (seq.size < 2) return out
        var cur = bestCombo(seq[0].props, seq[1]) ?: return out
        out.add(cur)
        var i = 2
        while (i < seq.size) {
            val next = bestCombo(listOf(cur.name), seq[i]) ?: break
            out.add(next); cur = next; i++
        }
        return out
    }

    /** Elements (magic-burst) for a chain name, for display of a single WS's chain properties. */
    fun elementsFor(chain: String): List<String> = chains[chain]?.second ?: emptyList()

    companion object {
        fun load(context: Context): SkillchainDb {
            val text = context.assets.open("skillchains.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)

            val wsArr = root.getJSONArray("weaponskills")
            val ws = ArrayList<WeaponSkill>(wsArr.length())
            for (i in 0 until wsArr.length()) {
                val o = wsArr.getJSONObject(i)
                val pa = o.getJSONArray("props")
                ws.add(WeaponSkill(o.getInt("id"), o.getString("name"), o.getString("type"),
                    (0 until pa.length()).map { pa.getString(it) }, o.optString("aeonic").ifBlank { null }))
            }

            val chains = HashMap<String, Pair<Int, List<String>>>()
            val cObj = root.getJSONObject("chains")
            val cKeys = cObj.keys()
            while (cKeys.hasNext()) {
                val k = cKeys.next(); val o = cObj.getJSONObject(k)
                val el = o.optJSONArray("elements")
                val els = if (el != null) (0 until el.length()).map { el.getString(it) } else emptyList()
                chains[k] = o.optInt("lvl", 1) to els
            }

            val combos = HashMap<String, Map<String, Pair<String, Int>>>()
            val kObj = root.getJSONObject("combos")
            val kKeys = kObj.keys()
            while (kKeys.hasNext()) {
                val first = kKeys.next(); val inner = kObj.getJSONObject(first)
                val innerKeys = inner.keys()
                val m = HashMap<String, Pair<String, Int>>()
                while (innerKeys.hasNext()) {
                    val second = innerKeys.next(); val arr = inner.getJSONArray(second)
                    m[second] = arr.getString(0) to arr.getInt(1)
                }
                combos[first] = m
            }
            return SkillchainDb(ws, chains, combos)
        }
    }
}
