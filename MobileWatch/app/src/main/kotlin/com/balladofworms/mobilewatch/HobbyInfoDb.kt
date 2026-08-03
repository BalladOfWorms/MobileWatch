package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class HobbyNpc(val name: String, val purpose: String, val zone: String, val loc: String)
data class HobbyNpcGroup(val zone: String, val rows: List<HobbyNpc>)
data class HobbyItem(val name: String, val bonus: String, val source: String)
data class HobbyItemSection(val section: String, val note: String, val rows: List<HobbyItem>)
data class HobbyInfo(
    val guild: String,
    val enroll: String,
    val hours: String,
    val holiday: String,
    val npcs: List<HobbyNpcGroup>,
    val items: List<HobbyItemSection>,
)

class HobbyInfoDb(private val map: Map<String, HobbyInfo>) {

    fun infoFor(key: String): HobbyInfo? = map[key]

    companion object {
        fun load(context: Context): HobbyInfoDb {
            val out = HashMap<String, HobbyInfo>()
            runCatching {
                val text = context.assets.open("hobbyinfo.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val hobbies = JSONObject(text).getJSONObject("hobbies")
                for (key in hobbies.keys()) {
                    val o = hobbies.getJSONObject(key)
                    val nArr = o.optJSONArray("npcs")
                    val npcs = if (nArr != null) (0 until nArr.length()).map { i ->
                        val grp = nArr.getJSONObject(i)
                        val rArr = grp.optJSONArray("rows")
                        val rows = if (rArr != null) (0 until rArr.length()).map { j ->
                            val r = rArr.getJSONObject(j)
                            HobbyNpc(r.optString("n"), r.optString("p"), r.optString("zone"), r.optString("loc"))
                        } else emptyList()
                        HobbyNpcGroup(grp.optString("zone"), rows)
                    } else emptyList()
                    val iArr = o.optJSONArray("items")
                    val items = if (iArr != null) (0 until iArr.length()).map { i ->
                        val sec = iArr.getJSONObject(i)
                        val rArr = sec.optJSONArray("rows")
                        val rows = if (rArr != null) (0 until rArr.length()).map { j ->
                            val r = rArr.getJSONObject(j)
                            HobbyItem(r.optString("n"), r.optString("b"), r.optString("src"))
                        } else emptyList()
                        HobbyItemSection(sec.optString("section"), sec.optString("note"), rows)
                    } else emptyList()
                    out[key] = HobbyInfo(
                        o.optString("guild"), o.optString("enroll"), o.optString("hours"), o.optString("holiday"),
                        npcs, items
                    )
                }
            }
            return HobbyInfoDb(out)
        }
    }
}
