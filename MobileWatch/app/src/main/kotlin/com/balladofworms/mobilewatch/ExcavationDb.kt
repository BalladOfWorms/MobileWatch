package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class ExcavationZone(val name: String, val items: List<HarvestItem>)

class ExcavationDb(val zones: List<ExcavationZone>) {

    companion object {
        fun load(context: Context): ExcavationDb {
            val zones = ArrayList<ExcavationZone>()
            runCatching {
                val text = context.assets.open("excavation.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
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
                    zones.add(ExcavationZone(o.optString("n"), items.sortedByRarity()))
                }
            }
            return ExcavationDb(zones)
        }
    }
}
