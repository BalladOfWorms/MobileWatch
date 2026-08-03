package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class LoggingZone(val name: String, val items: List<HarvestItem>)

class LoggingDb(val zones: List<LoggingZone>) {

    companion object {
        fun load(context: Context): LoggingDb {
            val zones = ArrayList<LoggingZone>()
            runCatching {
                val text = context.assets.open("logging.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
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
                    zones.add(LoggingZone(o.optString("n"), items.sortedByRarity()))
                }
            }
            return LoggingDb(zones)
        }
    }
}
