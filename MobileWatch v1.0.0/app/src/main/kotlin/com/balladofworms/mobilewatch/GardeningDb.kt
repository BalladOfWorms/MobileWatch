package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class GardenSeed(val name: String, val type: String, val affinity: String)

/** One harvest result within a planting: item name + per-pot yield range (only pots with a value). */
data class GardenResult(val name: String, val pots: Map<String, String>)

/** One wiki table = one seed grown with one crystal (crystal "None" for the no-crystal table).
 *  Two-feed seeds (Cactus Stems, Tree Saplings) also carry crystal2 = the Second Feed crystal. */
data class GardenPlanting(
    val seed: String,
    val crystal: String,
    val crystal2: String?,
    val results: List<GardenResult>,
) {
    /** Stable key for SaveableState / list keys. */
    val id: String get() = if (crystal2 != null) "$seed|$crystal|$crystal2" else "$seed|$crystal"
    /** Pots that appear anywhere in this planting's results. */
    val potsUsed: Set<String> get() = results.flatMap { it.pots.keys }.toSet()
    /** Display label for the crystal feed(s): "Fire" or, for two-feed seeds, "None \u2192 Fire". */
    fun crystalLabel(): String {
        val a = if (crystal == "None") "No Crystal" else crystal
        return if (crystal2 == null) a else "${if (crystal == "None") "None" else crystal} \u2192 ${if (crystal2 == "None") "None" else crystal2}"
    }
}

class GardeningDb(
    val pots: List<String>,
    val seeds: List<GardenSeed>,
    val plantings: List<GardenPlanting>,
) {
    fun seed(name: String): GardenSeed? = seeds.firstOrNull { it.name == name }

    companion object {
        fun load(context: Context): GardeningDb {
            val pots = ArrayList<String>()
            val seeds = ArrayList<GardenSeed>()
            val plantings = ArrayList<GardenPlanting>()
            runCatching {
                val text = context.assets.open("gardening.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val root = JSONObject(text)
                root.optJSONArray("pots")?.let { a -> for (i in 0 until a.length()) pots.add(a.getString(i)) }
                root.optJSONArray("seeds")?.let { a ->
                    for (i in 0 until a.length()) {
                        val o = a.getJSONObject(i)
                        seeds.add(GardenSeed(o.optString("n"), o.optString("type"), o.optString("affinity")))
                    }
                }
                root.optJSONArray("plantings")?.let { a ->
                    for (i in 0 until a.length()) {
                        val o = a.getJSONObject(i)
                        val results = ArrayList<GardenResult>()
                        o.optJSONArray("results")?.let { ra ->
                            for (j in 0 until ra.length()) {
                                val r = ra.getJSONObject(j)
                                val potMap = LinkedHashMap<String, String>()
                                r.optJSONObject("pots")?.let { po ->
                                    val keys = po.keys()
                                    while (keys.hasNext()) { val k = keys.next(); potMap[k] = po.getString(k) }
                                }
                                results.add(GardenResult(r.optString("n"), potMap))
                            }
                        }
                        plantings.add(GardenPlanting(o.optString("seed"), o.optString("crystal"),
                            if (o.has("crystal2")) o.optString("crystal2") else null, results))
                    }
                }
            }
            return GardeningDb(pots, seeds, plantings)
        }
    }
}
