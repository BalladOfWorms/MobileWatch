package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

/** One FFXI item, mirroring the desktop app's ffxi_items.json fields. */
data class Item(
    val id: Int,
    val name: String,
    val category: String,
    val stack: Int,
    val desc: String,
    val rareEx: String,
    val slotMask: Int,
    val level: Int,
    val ilevel: Int,
    val jobsMask: Long,
)

/**
 * Loads ffxi_items.json from assets and provides the same name search the
 * desktop app uses (substring match, prefix hits first, then alphabetical).
 */
class ItemDb private constructor(
    private val byId: Map<Int, Item>,
    private val nameIndex: List<Item>, // sorted by lowercase name
    private val disambig: Map<Int, String>, // id -> suffix for same-named items
) {
    fun get(id: Int): Item? = byId[id]

    /** Display label for the results list: appends a level/DMG suffix to items
     *  that share a name (REMA upgrade stages), leaving unique names untouched. */
    fun label(item: Item): String =
        disambig[item.id]?.let { "${item.name}   \u2014   $it" } ?: item.name

    private val allSorted: List<Item> by lazy { nameIndex.sortedBy { it.name.lowercase() } }
    fun all(): List<Item> = allSorted

    fun search(query: String, limit: Int = 300): List<Item> {
        val q = query.trim().lowercase()
        if (q.isEmpty()) return emptyList()
        return nameIndex.asSequence()
            .filter { it.name.lowercase().contains(q) }
            .sortedWith(compareBy({ if (it.name.lowercase().startsWith(q)) 0 else 1 }, { it.name.lowercase() }))
            .take(limit)
            .toList()
    }

    companion object {
        fun load(context: Context): ItemDb {
            val text = context.assets.open("ffxi_items.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)
            val byId = HashMap<Int, Item>(root.length())
            val keys = root.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                val id = k.toIntOrNull() ?: continue
                val o = root.getJSONObject(k)
                byId[id] = Item(
                    id = id,
                    name = o.optString("n", ""),
                    category = o.optString("c", "?"),
                    stack = o.optInt("s", 1),
                    desc = o.optString("d", ""),
                    rareEx = o.optString("re", ""),
                    slotMask = o.optInt("sl", 0),
                    level = o.optInt("lv", 0),
                    ilevel = o.optInt("il", 0),
                    jobsMask = o.optLong("j", 0L),
                )
            }
            val index = byId.values.sortedBy { it.name.lowercase() }
            val disambig = buildDisambig(byId)
            return ItemDb(byId, index, disambig)
        }

        // Same-named items get a short suffix: item level (or level), with weapon
        // DMG as the tiebreaker when stages share a level. Items with neither are
        // left alone (not the weapons we care about).
        private val DMG_RE = Regex("DMG:\\s*(\\d+)")
        private fun buildDisambig(byId: Map<Int, Item>): Map<Int, String> {
            val byName = HashMap<String, MutableList<Item>>()
            for (it in byId.values) byName.getOrPut(it.name.lowercase()) { ArrayList() }.add(it)
            val out = HashMap<Int, String>()
            fun lvtag(it: Item): String = when {
                it.ilevel > 0 -> "iLv ${it.ilevel}"
                it.level > 0 -> "Lv ${it.level}"
                else -> ""
            }
            for ((_, group) in byName) {
                if (group.size < 2) continue
                val base = group.associate { it.id to lvtag(it) }
                val counts = base.values.groupingBy { it }.eachCount()
                for (it in group) {
                    var tag = base[it.id] ?: ""
                    if (tag.isEmpty() || (counts[tag] ?: 0) > 1) {
                        val dmg = DMG_RE.find(it.desc)?.groupValues?.get(1)
                        if (dmg != null) tag = if (tag.isEmpty()) "DMG $dmg" else "$tag  DMG $dmg"
                    }
                    if (tag.isNotEmpty()) out[it.id] = tag
                }
            }
            return out
        }
    }
}

/** Decode helpers matching the desktop app. */
object FfxiDecode {
    private val JOBS = arrayOf(
        "", "WAR", "MNK", "WHM", "BLM", "RDM", "THF", "PLD", "DRK", "BST", "BRD",
        "RNG", "SAM", "NIN", "DRG", "SMN", "BLU", "COR", "PUP", "DNC", "SCH", "GEO", "RUN"
    )
    private val SLOTS = arrayOf(
        "Main", "Sub", "Range", "Ammo", "Head", "Body", "Hands", "Legs", "Feet",
        "Neck", "Waist", "L.Ear", "R.Ear", "L.Ring", "R.Ring", "Back"
    )

    fun jobs(mask: Long): String {
        if (mask == 0L) return ""
        val on = (1..22).filter { (mask and (1L shl it)) != 0L }.map { JOBS[it] }
        return if (on.size == 22) "All jobs" else on.joinToString(" ")
    }

    fun slots(mask: Int): String {
        if (mask == 0) return ""
        val txt = (0 until 16).filter { (mask and (1 shl it)) != 0 }.joinToString("/") { SLOTS[it] }
        return txt.replace("L.Ear/R.Ear", "Ears").replace("L.Ring/R.Ring", "Rings")
    }
}
