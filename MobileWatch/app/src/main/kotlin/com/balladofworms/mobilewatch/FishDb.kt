package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class FishSpot(val name: String, val note: String, val best: Boolean)
data class FishGear(val name: String, val best: Boolean, val mayBreak: Boolean, val tooSmall: Boolean)
data class Fish(
    val name: String,
    val level: Int,
    val levelText: String,
    val rank: String,
    val water: String,
    val zones: List<FishSpot>,
    val rods: List<FishGear>,
    val baits: List<FishGear>,
    val keyItem: String,
)

class FishDb(val fish: List<Fish>) {

    companion object {
        fun load(context: Context): FishDb {
            val out = ArrayList<Fish>()
            runCatching {
                val text = context.assets.open("fishing.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val arr = JSONObject(text).getJSONArray("fish")
                for (i in 0 until arr.length()) {
                    val o = arr.getJSONObject(i)
                    val zArr = o.optJSONArray("zones")
                    val zones = if (zArr != null) (0 until zArr.length()).map {
                        val z = zArr.getJSONObject(it)
                        FishSpot(z.optString("n"), z.optString("note"), z.optBoolean("best", false))
                    } else emptyList()
                    fun gear(key: String): List<FishGear> {
                        val gArr = o.optJSONArray(key) ?: return emptyList()
                        return (0 until gArr.length()).map {
                            val g = gArr.getJSONObject(it)
                            FishGear(g.optString("n"), g.optBoolean("best", false), g.optBoolean("mb", false), g.optBoolean("ts", false))
                        }
                    }
                    out.add(
                        Fish(
                            o.optString("n"), o.optInt("lv", 0), o.optString("lvx"), o.optString("rank"), o.optString("water"),
                            zones, gear("rods"), gear("baits"), o.optString("ki")
                        )
                    )
                }
            }
            return FishDb(out.sortedWith(compareBy({ it.level }, { it.name })))
        }
    }
}
