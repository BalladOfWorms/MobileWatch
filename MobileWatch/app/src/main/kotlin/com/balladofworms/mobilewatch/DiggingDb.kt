package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class DigItem(val name: String, val rarity: String)
data class DigZone(
    val name: String,
    val items: List<DigItem>,
    val burrow: List<DigItem>,
    val bore: List<DigItem>,
) {
    val all: List<DigItem> get() = items + burrow + bore
}

class DiggingDb(val zones: List<DigZone>) {

    companion object {
        fun load(context: Context): DiggingDb {
            val zones = ArrayList<DigZone>()
            runCatching {
                val text = context.assets.open("digging.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val arr = JSONObject(text).getJSONArray("zones")
                fun items(o: JSONObject, key: String): List<DigItem> {
                    val a = o.optJSONArray(key) ?: return emptyList()
                    return (0 until a.length()).map {
                        val g = a.getJSONObject(it)
                        DigItem(g.optString("n"), g.optString("r"))
                    }
                }
                for (i in 0 until arr.length()) {
                    val o = arr.getJSONObject(i)
                    zones.add(DigZone(o.optString("n"), items(o, "items"), items(o, "burrow"), items(o, "bore")))
                }
            }
            return DiggingDb(zones)
        }
    }
}
