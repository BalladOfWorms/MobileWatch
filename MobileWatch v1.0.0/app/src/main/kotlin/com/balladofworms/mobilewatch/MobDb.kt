package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

data class Mob(
    val key: String,
    val name: String,
    val family: String,
    val levelLo: Int,
    val levelHi: Int,
    val weaknesses: List<Pair<String, String?>>,  // (name, "+25%") physical first, then magical
    val strengths: List<Pair<String, String?>>,   // (name, "-50%")
    val immune: List<String>,
    val absorb: List<String>,
    val aggro: Boolean,
    val links: Boolean,
    val nm: Boolean,
    val abilities: List<String>,
    val spells: List<String>,
    val detects: List<String>,
    val job: String,
    val respawn: Int,
    val crystal: String,
    val spawn: String,
    val drops: String,
    val nmLevel: String,
    val notes: List<String> = emptyList(),
    /** Step-by-step path to spawning this mob (Abyssea pop chains). */
    val farm: List<String> = emptyList(),
    val sub: String? = null,
    val eco: String? = null,
    val zones: List<Pair<String, String?>> = emptyList(),
    val image: String? = null,
    // Content tags — Abyssea / Dynamis / Voidwatch / Salvage / ... Deliberately a LIST, not a
    // String: optJSONArray is null-safe, so an absent key AND a JSON null both give emptyList(),
    // where an optString field would hand back the literal "null" (the rev-127 null-poison class).
    // Format is `Group[: Section[: Role]]` — see contentParts() in MobileWatchApp.kt.
    val content: List<String> = emptyList(),
) {
    val respawnText: String
        get() = when {
            respawn <= 0 -> ""
            respawn < 60 -> "$respawn sec"
            respawn % 60 == 0 -> "${respawn / 60} min"
            else -> "${respawn / 60}m ${respawn % 60}s"
        }

    val levelText: String
        get() = when {
            nmLevel.isNotEmpty() -> "Lv $nmLevel"
            levelLo <= 0 && levelHi <= 0 -> ""
            levelLo == levelHi -> "Lv $levelLo"
            else -> "Lv $levelLo\u2013$levelHi"
        }
}

data class AbilityInfo(val desc: String?, val type: String?, val notes: String?, val range: String?,
                       val target: String?, val effects: List<String>, val element: String? = null)

data class SubType(val name: String, val weaknesses: List<Pair<String, String?>>,
                   val strengths: List<Pair<String, String?>>, val notes: List<String>,
                   val image: String? = null)

data class ResistSet(val label: String, val weaknesses: List<Pair<String, String?>>,
                     val strengths: List<Pair<String, String?>>)

class MobDb private constructor(
    private val byKey: Map<String, Mob>,
    private val nameIndex: List<Mob>,
    private val abilities: Map<String, AbilityInfo>,
    private val familyIcons: Map<String, String>,
    private val familyNotesMap: Map<String, List<String>>,
    private val familySubtypesMap: Map<String, List<SubType>>,
    private val familyEcoMap: Map<String, String>,
    private val familyResistSetsMap: Map<String, List<ResistSet>>,
) {
    /** Matches mob name or family, so typing a family (e.g. "Yagudo") lists them all. */
    fun get(key: String): Mob? = byKey[key]

    private val allSorted: List<Mob> by lazy { nameIndex.sortedBy { it.name.lowercase() } }
    fun all(): List<Mob> = allSorted

    fun search(query: String, limit: Int = 300): List<Mob> {
        val q = query.trim().lowercase()
        if (q.isEmpty()) return emptyList()
        return nameIndex.asSequence()
            .filter { it.name.lowercase().contains(q) || it.family.lowercase().contains(q) ||
                      (familyEcoMap[it.family]?.lowercase()?.contains(q) == true) }
            .sortedWith(compareBy(
                { if (it.name.lowercase().startsWith(q)) 0 else if (it.name.lowercase().contains(q)) 1 else 2 },
                { it.name.lowercase() }))
            .take(limit)
            .toList()
    }

    /** Asset path for a family's icon, or null if none. */
    fun iconPath(family: String): String? =
        familyIcons[family]?.let { "mobicons/$it" } ?: if (family.isNotBlank()) "mobicons/$family.jpg" else null

    /** Ability description info (parenthetical conditions stripped for lookup). */
    fun ability(name: String): AbilityInfo? = abilities[name] ?: abilities[name.substringBefore('(').trim()]

    /** Family-wide general notes (bullet points) shown read-only on the mob card. */
    fun familyNotes(family: String): List<String> = familyNotesMap[family] ?: emptyList()

    /** Sub-type resistance variants for a family (e.g. Lynx under Coeurl). */
    fun subtypes(family: String): List<SubType> = familySubtypesMap[family] ?: emptyList()

    /** Named resistance sets for families that shift resistances mid-fight (e.g. Peiste Green/Purple/Orange). */
    fun resistSets(family: String): List<ResistSet> = familyResistSetsMap[family] ?: emptyList()

    /** Ecosystem (broad Family: Beast, Lizard, Vermin...) for a specific type. */
    fun ecosystem(family: String): String? = familyEcoMap[family]

    /** Ecosystem for a specific mob — its per-mob override if set, else the family's ecosystem. */
    fun ecosystemOf(mob: Mob): String? = mob.eco ?: familyEcoMap[mob.family]

    /** Icon path for a mob: its sub-type's image if it belongs to one, else the family icon. */
    fun iconForMob(mob: Mob): String? {
        mob.image?.let { return it }
        mob.sub?.let { s ->
            familySubtypesMap[mob.family]?.firstOrNull { it.name.equals(s, ignoreCase = true) }?.image?.let { return it }
        }
        return iconPath(mob.family)
    }

    companion object {
        private fun strList(o: JSONObject, k: String): List<String> {
            val a: JSONArray = o.optJSONArray(k) ?: return emptyList()
            return (0 until a.length()).map { a.getString(it) }
        }

        private fun modList(o: JSONObject, k: String): List<Pair<String, String?>> {
            val a: JSONArray = o.optJSONArray(k) ?: return emptyList()
            return (0 until a.length()).map {
                val e = a.getJSONArray(it)
                e.getString(0) to if (e.isNull(1)) null else e.optString(1).ifBlank { null }
            }
        }

        fun load(context: Context): MobDb {
            val text = context.assets.open("mobs.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)

            val mobsObj = root.getJSONObject("mobs")
            val byKey = HashMap<String, Mob>(mobsObj.length())
            val keys = mobsObj.keys()
            while (keys.hasNext()) {
                val key = keys.next()
                val o = mobsObj.getJSONObject(key)
                val lv = o.optJSONArray("lv")
                byKey[key] = Mob(
                    key = key,
                    name = o.optString("n", key),
                    family = o.optString("fam", ""),
                    levelLo = lv?.optInt(0, 0) ?: 0,
                    levelHi = lv?.optInt(1, 0) ?: 0,
                    weaknesses = modList(o, "wk"),
                    strengths = modList(o, "st"),
                    immune = strList(o, "im"),
                    absorb = strList(o, "ab_el"),
                    aggro = o.optBoolean("agg", false),
                    links = o.optBoolean("lnk", false),
                    nm = o.optBoolean("nm", false),
                    abilities = strList(o, "ab"),
                    spells = strList(o, "sp"),
                    detects = strList(o, "det"),
                    job = o.optString("job", ""),
                    respawn = o.optInt("resp", 0),
                    crystal = o.optString("crys", ""),
                    spawn = o.optString("spawn", ""),
                    drops = o.optString("drops", ""),
                    nmLevel = o.optString("nmlv", ""),
                    notes = o.optJSONArray("notes")?.let { arr -> (0 until arr.length()).map { arr.getString(it) } }
                        ?: o.optString("notes").ifBlank { null }?.let { listOf(it) } ?: emptyList(),
                    farm = o.optJSONArray("farm")?.let { arr -> (0 until arr.length()).map { arr.getString(it) } }
                        ?: o.optString("farm").ifBlank { null }?.let { listOf(it) } ?: emptyList(),
                    sub = o.optString("sub").ifBlank { null },
                    eco = o.optString("eco").ifBlank { null },
                    zones = o.optJSONArray("zones")?.let { arr ->
                        (0 until arr.length()).map { i ->
                            val e = arr.get(i)
                            if (e is JSONArray) e.getString(0) to (if (e.length() > 1 && !e.isNull(1)) e.optString(1).ifBlank { null } else null)
                            else e.toString() to null
                        }
                    } ?: emptyList(),
                    image = o.optString("img").ifBlank { null },
                    content = strList(o, "content"),
                )
            }

            val abilities = HashMap<String, AbilityInfo>()
            root.optJSONObject("abilities")?.let { ao ->
                val ak = ao.keys()
                while (ak.hasNext()) {
                    val name = ak.next()
                    val a = ao.getJSONObject(name)
                    abilities[name] = AbilityInfo(
                        desc = a.optString("d").ifBlank { null },
                        type = a.optString("t").ifBlank { null },
                        notes = a.optString("notes").ifBlank { null },
                        range = a.optString("r").ifBlank { null },
                        target = a.optString("tgt").ifBlank { null },
                        effects = strList(a, "fx"),
                        element = a.optString("el").ifBlank { null },
                    )
                }
            }

            val familyIcons = HashMap<String, String>()
            root.optJSONObject("family_icons")?.let { fo ->
                val fk = fo.keys()
                while (fk.hasNext()) { val f = fk.next(); familyIcons[f] = fo.getString(f) }
            }

            val familyNotes = HashMap<String, List<String>>()
            root.optJSONObject("family_notes")?.let { no ->
                val nk = no.keys()
                while (nk.hasNext()) {
                    val f = nk.next()
                    val arr = no.getJSONArray(f)
                    familyNotes[f] = (0 until arr.length()).map { arr.getString(it) }
                }
            }

            val familySubtypes = HashMap<String, List<SubType>>()
            root.optJSONObject("family_subtypes")?.let { so ->
                val sk = so.keys()
                while (sk.hasNext()) {
                    val f = sk.next()
                    val arr = so.getJSONArray(f)
                    familySubtypes[f] = (0 until arr.length()).map { i ->
                        val obj = arr.getJSONObject(i)
                        SubType(
                            name = obj.optString("name"),
                            weaknesses = modList(obj, "wk"),
                            strengths = modList(obj, "st"),
                            notes = obj.optJSONArray("notes")?.let { arr -> (0 until arr.length()).map { arr.getString(it) } }
                                ?: obj.optString("notes").ifBlank { null }?.let { listOf(it) } ?: emptyList(),
                            image = obj.optString("img").ifBlank { null }
                        )
                    }
                }
            }

            val familyEco = HashMap<String, String>()
            root.optJSONObject("family_eco")?.let { eo ->
                val ek = eo.keys()
                while (ek.hasNext()) { val f = ek.next(); familyEco[f] = eo.getString(f) }
            }

            val familyResistSets = HashMap<String, List<ResistSet>>()
            root.optJSONObject("family_resist_sets")?.let { ro ->
                val rk = ro.keys()
                while (rk.hasNext()) {
                    val f = rk.next()
                    val arr = ro.getJSONArray(f)
                    familyResistSets[f] = (0 until arr.length()).map { i ->
                        val obj = arr.getJSONObject(i)
                        ResistSet(
                            label = obj.optString("label"),
                            weaknesses = modList(obj, "wk"),
                            strengths = modList(obj, "st"),
                        )
                    }
                }
            }

            val index = byKey.values.sortedBy { it.name.lowercase() }
            return MobDb(byKey, index, abilities, familyIcons, familyNotes, familySubtypes, familyEco, familyResistSets)
        }
    }
}
