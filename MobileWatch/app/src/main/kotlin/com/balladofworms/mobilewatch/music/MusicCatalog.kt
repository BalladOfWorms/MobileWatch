package com.balladofworms.mobilewatch.music

import android.content.Context
import org.json.JSONObject

// OmniPlayer's track catalogue (assets/music/catalog.json) and the same recognition rules, so a
// .bgw file gets its real name, composer and expansion the moment it's found.
//
// The same musicNNN number turns up in more than one of the game's sound folders, so a file is
// never named by its number alone:
//   1. A folder with "soundN" in its path is that sound folder: its own catalogue section is
//      certain for the numbers it has, and any other section with 2+ of its numbers there too.
//   2. A folder without it (a copy, or a section not tied to a folder) is judged by what's IN it:
//      the section that accounts for most of its numbers wins, if that's more than chance.
//   3. Otherwise the file's fingerprint, remembered from an earlier time it was recognised.

class CatalogEntry(val expansion: String, val title: String, val composer: String, val heard: String,
                   val how: String)

class MusicCatalog private constructor(
    // section key -> (section expansion, number -> row)
    private val sections: Map<String, Pair<String, Map<Int, List<String>>>>
) {
    private val folderKey = Regex("^sound\\d*$")

    private fun entry(sec: String, n: Int, how: String): CatalogEntry {
        val (exp, rows) = sections.getValue(sec)
        val r = rows.getValue(n)
        return CatalogEntry(r.getOrNull(3)?.takeIf { it.isNotBlank() } ?: exp,
            r.getOrElse(0) { "" }, r.getOrElse(1) { "" }, r.getOrElse(2) { "" },
            "${exp}, music%03d (%s)".format(n, how))
    }

    private fun has(sec: String, n: Int?) = n != null && sections[sec]?.second?.containsKey(n) == true

    /**
     * Recognise every BGW track in [tracks] (they carry their folder path and number), using and
     * updating [fingerprints] (fingerprint -> "section|number").
     */
    fun assign(tracks: List<MusicTrack>, fingerprints: MutableMap<String, String>) {
        tracks.filter { it.isBgw }.groupBy { it.folder }.forEach { (_, group) ->
            val named = group.first().folder.split('/').map { it.lowercase() }
                .lastOrNull { folderKey.matches(it) }
            // A soundN folder this catalogue has nothing for is judged by its contents instead.
            val sec: String? = if (named != null && group.any { has(named, it.number) }) named else null
            val counts = sections.keys.filter { it != sec }
                .associateWith { k -> group.count { has(k, it.number) } }
            val best = counts.maxByOrNull { it.value }
            val nums = group.count { it.number != null }
            val winner: String? = if (sec == null && best != null && best.value > 0 &&
                (best.value >= 5 || best.value >= 0.4 * maxOf(1, nums))) best.key else null
            for (t in group) {
                val n = t.number
                var pick: String? = null
                var how = ""
                if (sec != null) {
                    if (has(sec, n)) { pick = sec; how = "its sound folder" }
                    else {
                        val owners = counts.filter { has(it.key, n) && it.value >= 2 }
                            .entries.sortedBy { it.value }
                        if (owners.size == 1 || (owners.size > 1 && owners.last().value > owners[owners.size - 2].value)) {
                            pick = owners.last().key; how = "by its number -- folder not confirmed"
                        }
                    }
                } else if (winner != null) {
                    if (has(winner, n)) { pick = winner; how = "what's in its folder" }
                    else {
                        val owners = sections.keys.filter { has(it, n) }
                            .map { it to (counts[it] ?: 0) }.sortedBy { it.second }
                        if (owners.size == 1 || (owners.size > 1 && owners.last().second > owners[owners.size - 2].second)) {
                            pick = owners.last().first; how = "what's in its folder"
                        }
                    }
                }
                if (pick != null && n != null) {
                    t.cat = entry(pick, n, how)
                    t.fingerprint?.let { fingerprints[it] = "$pick|$n" }
                    continue
                }
                val hit = t.fingerprint?.let { fingerprints[it] }?.split('|')
                if (hit != null && hit.size == 2) {
                    val hn = hit[1].toIntOrNull()
                    if (has(hit[0], hn)) t.cat = entry(hit[0], hn!!, "its fingerprint")
                }
            }
        }
    }

    companion object {
        @Volatile private var loaded: MusicCatalog? = null

        fun get(ctx: Context): MusicCatalog = loaded ?: synchronized(this) {
            loaded ?: load(ctx).also { loaded = it }
        }

        private fun load(ctx: Context): MusicCatalog {
            val text = runCatching {
                ctx.assets.open("music/catalog.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
            }.getOrDefault("{}")
            val secs = JSONObject(text).optJSONObject("sections") ?: JSONObject()
            val out = LinkedHashMap<String, Pair<String, Map<Int, List<String>>>>()
            for (key in secs.keys()) {
                val s = secs.getJSONObject(key)
                val rows = HashMap<Int, List<String>>()
                val tr = s.optJSONObject("tracks") ?: continue
                for (num in tr.keys()) {
                    val a = tr.getJSONArray(num)
                    rows[num.toIntOrNull() ?: continue] = List(a.length()) { a.optString(it) }
                }
                out[key] = s.optString("expansion") to rows
            }
            return MusicCatalog(out)
        }
    }
}
