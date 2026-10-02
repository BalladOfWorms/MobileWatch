package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

/**
 * One quest as the in-game quest log lists it.
 *
 * `slug` is only set where the BG-wiki article title differs from the name
 * the log shows — the Voidwatch ops are written "VW Op. #115: ..." in game
 * but their wiki pages drop the hash. Everything else resolves from the
 * name, so the field is null for all but a handful of rows.
 */
data class Quest(val name: String, val slug: String?)

/**
 * One section of the quest log. `key` is the storage key the completion
 * ticks are filed under, so renaming a section would orphan its ticks.
 */
data class QuestArea(val key: String, val label: String, val quests: List<Quest>)

/**
 * The quest log, by area. Areas are held in the order the game lists them
 * rather than alphabetically; quests inside an area are alphabetical, which
 * is how you scan for one you have just finished.
 */
class QuestDb private constructor(val areas: List<QuestArea>) {

    fun area(key: String): QuestArea? = areas.firstOrNull { it.key == key }

    /** Every quest across every area — the denominator on the tab header. */
    val total: Int = areas.sumOf { it.quests.size }

    companion object {
        fun load(ctx: Context): QuestDb {
            val text = ctx.assets.open("quests.json").bufferedReader().use { it.readText() }
            val root = JSONObject(text)
            val arr = root.optJSONArray("areas")
            val areas = ArrayList<QuestArea>()
            for (i in 0 until (arr?.length() ?: 0)) {
                val o = arr!!.optJSONObject(i) ?: continue
                val qarr = o.optJSONArray("quests")
                val quests = ArrayList<Quest>()
                for (j in 0 until (qarr?.length() ?: 0)) {
                    val q = qarr!!.optJSONObject(j) ?: continue
                    val n = q.optString("n", "")
                    if (n.isBlank()) continue
                    val slug = q.optString("slug", "").ifBlank { null }
                    quests.add(Quest(n, slug))
                }
                areas.add(QuestArea(o.optString("key", ""), o.optString("label", ""), quests))
            }
            return QuestDb(areas)
        }
    }
}
