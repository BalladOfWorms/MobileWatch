package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

/**
 * The full player weapon-skill reference, weapon by weapon, in the wiki's own order
 * (unlock order — skill level, then the quest WS, then the REMA tiers).
 *
 * Deliberately holds NO skillchain properties: the list screen resolves those by
 * name out of SkillchainDb, so chain data has exactly one source of truth. A WS the
 * wiki prints as "No Property" carries `noProp` and simply has no entry there.
 *
 *   req  — weapon skill level ("200"), or the unlock class ("Quest", "Relic",
 *          "Empyrean", "Aeonic", "Mythic", "Ergon", "Prime"). Automaton's ranged
 *          values keep the wiki's brackets ("(245)").
 *   jobs — the table's job columns; for Automaton, the four frames instead.
 */
data class WsEntry(val name: String, val req: String, val noProp: Boolean)

data class WsWeapon(
    val type: String,
    val jobs: List<String>,
    val note: String?,
    val ws: List<WsEntry>,
)

class WsListDb private constructor(val weapons: List<WsWeapon>) {

    companion object {
        fun load(context: Context): WsListDb {
            val text = context.assets.open("weaponskills.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)
            val arr = root.optJSONArray("weapons")
            val out = ArrayList<WsWeapon>(arr?.length() ?: 0)
            for (i in 0 until (arr?.length() ?: 0)) {
                val o = arr!!.getJSONObject(i)
                val ja = o.optJSONArray("jobs")
                val jobs = if (ja == null) emptyList() else (0 until ja.length()).map { ja.getString(it) }
                val wa = o.optJSONArray("ws")
                val ws = ArrayList<WsEntry>(wa?.length() ?: 0)
                for (j in 0 until (wa?.length() ?: 0)) {
                    val e = wa!!.getJSONObject(j)
                    ws.add(WsEntry(e.optString("n"), e.optString("req"), e.optBoolean("np", false)))
                }
                out.add(WsWeapon(o.optString("type"), jobs, o.optString("note").ifBlank { null }, ws))
            }
            return WsListDb(out)
        }
    }
}
