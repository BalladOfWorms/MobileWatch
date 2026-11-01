package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

/** One row to tick: a mission ("1-1", The Zeruhn Report) or a mount. id is what the tick is
 *  stored under, the same key OmniWatch's checklist uses, so the two can sync. */
data class ClItem(val id: String, val code: String, val name: String, val desc: String)

/** A mission line (Bastok, Rise of the Zilart...), keyed like OmniWatch's checklist tab. */
data class ClCat(val key: String, val label: String, val items: List<ClItem>)

/**
 * Missions and mounts, from assets/checklists.json. The mission lists and their order are
 * OmniWatch's own checklist lists; the mounts are every mount in the game's resources.
 */
class ChecklistDb private constructor(val missions: List<ClCat>, val mounts: List<ClItem>) {
    fun mission(key: String): ClCat? = missions.firstOrNull { it.key == key }

    companion object {
        const val MOUNTS = "mounts"

        fun load(ctx: Context): ChecklistDb {
            val root = JSONObject(ctx.assets.open("checklists.json").bufferedReader().use { it.readText() })
            val ms = ArrayList<ClCat>()
            root.optJSONArray("missions")?.let { arr ->
                for (i in 0 until arr.length()) {
                    val o = arr.optJSONObject(i) ?: continue
                    val items = ArrayList<ClItem>()
                    o.optJSONArray("items")?.let { a -> for (j in 0 until a.length()) a.optJSONObject(j)?.let { m ->
                        items.add(ClItem(m.optString("id"), m.optString("code"), m.optString("name"), ""))
                    } }
                    ms.add(ClCat(o.optString("key"), o.optString("label"), items))
                }
            }
            val mounts = ArrayList<ClItem>()
            root.optJSONArray("mounts")?.let { a -> for (j in 0 until a.length()) a.optJSONObject(j)?.let { m ->
                mounts.add(ClItem(m.optString("id"), "", m.optString("name"), m.optString("desc")))
            } }
            return ChecklistDb(ms, mounts)
        }
    }
}
