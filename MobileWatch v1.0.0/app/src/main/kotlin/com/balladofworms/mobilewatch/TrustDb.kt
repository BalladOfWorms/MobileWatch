package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

/**
 * One alter ego. `role` is the role its Trust-spell icon carries on BG-wiki
 * (Tank / Melee Fighter / Ranged Fighter / Caster / Healer / Support / Special) —
 * that is the grouping the Trusts tab lists them under.
 *
 * acquisition / features / synergy are bullet lists; a line's indent level is
 * carried by its leading spaces (2 per level) so the JSON stays a flat array.
 */
data class Trust(
    val name: String,
    val role: String,
    val job: String,
    val spells: List<String>,
    val abilities: List<String>,
    val ws: List<String>,
    val acquisition: List<String>,
    val features: List<String>,
    val synergy: List<String>,
    /** Portrait asset path, folder included ("trustart/aaev.jpg") — a bare stem is a silent miss. */
    val image: String?,
)

/** One of the general Trust reference sections that head the Trusts tab (bullet lines, 2-space indent). */
data class TrustInfo(val title: String, val lines: List<String>)

class TrustDb private constructor(
    val roles: List<String>,
    val trusts: List<Trust>,
    val info: List<TrustInfo>,
) {
    private val byName: Map<String, Trust> = trusts.associateBy { it.name }

    fun byRole(role: String): List<Trust> = trusts.filter { it.role == role }
    fun trust(name: String): Trust? = byName[name]

    companion object {
        private fun strList(o: JSONObject, k: String): List<String> {
            val a = o.optJSONArray(k) ?: return emptyList()
            return (0 until a.length()).map { a.getString(it) }
        }

        fun load(context: Context): TrustDb {
            val text = context.assets.open("trusts.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)
            val roles = strList(root, "roles")
            val arr = root.optJSONArray("trusts")
            val out = ArrayList<Trust>(arr?.length() ?: 0)
            for (i in 0 until (arr?.length() ?: 0)) {
                val o = arr!!.getJSONObject(i)
                out.add(
                    Trust(
                        name = o.optString("n"),
                        role = o.optString("role"),
                        job = o.optString("job"),
                        spells = strList(o, "spells"),
                        abilities = strList(o, "abilities"),
                        ws = strList(o, "ws"),
                        acquisition = strList(o, "acq"),
                        features = strList(o, "feat"),
                        synergy = strList(o, "syn"),
                        image = o.optString("img").ifBlank { null },
                    )
                )
            }
            val iarr = root.optJSONArray("info")
            val info = ArrayList<TrustInfo>(iarr?.length() ?: 0)
            for (i in 0 until (iarr?.length() ?: 0)) {
                val o = iarr!!.getJSONObject(i)
                info.add(TrustInfo(o.optString("title"), strList(o, "lines")))
            }
            return TrustDb(roles, out, info)
        }
    }
}
