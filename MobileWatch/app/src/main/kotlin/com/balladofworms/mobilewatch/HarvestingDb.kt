package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class HarvestItem(val name: String, val rarity: String)
data class HarvestZone(val name: String, val items: List<HarvestItem>)

/** Rarity ordering for gathering (Harvesting/Mining/Excavation): rarest first.
 *  SR > VR > R > U > C > VC, with unknown "?" sorted last. Trailing '-' variants
 *  (e.g. "SR-") rank with their base tier. */
internal fun rarityRank(r: String): Int = when (r.uppercase().trimEnd('-')) {
    "VC" -> 0
    "C" -> 1
    "U" -> 2
    "R" -> 3
    "VR" -> 4
    "SR" -> 5
    "" -> 7
    else -> 6   // "?" and anything unrecognized
}

/** Sort a gathering zone's items commonest-first (VC) down to rarest (SR), breaking ties by name. */
internal fun List<HarvestItem>.sortedByRarity(): List<HarvestItem> =
    sortedWith(compareBy({ rarityRank(it.rarity) }, { it.name }))

class HarvestingDb(val zones: List<HarvestZone>) {

    companion object {
        fun load(context: Context): HarvestingDb {
            val zones = ArrayList<HarvestZone>()
            runCatching {
                val text = context.assets.open("harvesting.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val arr = JSONObject(text).getJSONArray("zones")
                for (i in 0 until arr.length()) {
                    val o = arr.getJSONObject(i)
                    val items = ArrayList<HarvestItem>()
                    o.optJSONArray("items")?.let { a ->
                        for (j in 0 until a.length()) {
                            val g = a.getJSONObject(j)
                            items.add(HarvestItem(g.optString("n"), g.optString("r")))
                        }
                    }
                    zones.add(HarvestZone(o.optString("n"), items.sortedByRarity()))
                }
            }
            return HarvestingDb(zones)
        }
    }
}
