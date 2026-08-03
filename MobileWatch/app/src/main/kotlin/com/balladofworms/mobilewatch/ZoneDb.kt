package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class Zone(
    val id: Int,
    val name: String,
    val slug: String,
    val region: String = "",
    val weather: List<String> = emptyList(),
)

class ZoneDb private constructor(private val index: List<Zone>) {
    fun all(): List<Zone> = index

    /** Matches zone name or slug; empty query returns the full list. */
    fun search(query: String, limit: Int = 400): List<Zone> {
        val q = query.trim().lowercase()
        if (q.isEmpty()) return index
        return index.asSequence()
            .filter { it.name.lowercase().contains(q) || it.slug.contains(q) }
            .sortedWith(compareBy({ if (it.name.lowercase().startsWith(q)) 0 else 1 }, { it.name.lowercase() }))
            .take(limit)
            .toList()
    }

    companion object {
        fun load(context: Context): ZoneDb {
            val text = context.assets.open("zones.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
            val arr = JSONObject(text).getJSONArray("zones")
            val dummies = setOf("none", "gm home")
            val list = ArrayList<Zone>(arr.length())
            for (i in 0 until arr.length()) {
                val o = arr.getJSONObject(i)
                val name = o.optString("name")
                if (name.isBlank() || name.lowercase() in dummies) continue
                val wx = o.optJSONArray("weather")
                val weather = if (wx != null) (0 until wx.length()).map { wx.getString(it) } else emptyList()
                list.add(Zone(o.optInt("id"), name, o.optString("slug"),
                    o.optString("region", ""), weather))
            }
            list.sortBy { it.name.lowercase() }
            return ZoneDb(list)
        }
    }
}
