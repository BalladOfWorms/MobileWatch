package com.balladofworms.mobilewatch.music

// Which track is a zone's music, from the catalogue's "where it's heard" lines.
//
// Those lines name places: a zone ("Rabao", "The Sanctuary of Zi'Tah"), a region
// ("Ronfaure", "Gustaberg", "Elshimo Lowlands"), or a past-era zone ("East Ronfaure (S)").
// A zone page matches, best first: a track named after the zone ("Metalworks"); a track
// heard in the zone itself; a track heard in a place the zone's name starts with ("Castle
// Zvahl" for Castle Zvahl Baileys); and, for outdoor and town zones only, a track heard across
// the zone's region (Ronfaure's theme for East Ronfaure). Dungeons have their own music, so
// they never borrow the region's. Past-era [S] zones prefer the past-era music.
// Lines that aren't places ("Battle theme", "Mission scenes") simply never match.

object ZoneMusic {
    // The zone -> music table (assets/music/zone_music.json): slug -> music file number, 0 for
    // a zone with no music. It comes from server zone data captured from the game, so it's the
    // first answer; the name matching below only covers zones it doesn't list.
    @Volatile private var table: Map<String, Int>? = null

    fun table(ctx: android.content.Context): Map<String, Int> = table ?: synchronized(this) {
        table ?: runCatching {
            val o = org.json.JSONObject(ctx.assets.open("music/zone_music.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }).getJSONObject("zones")
            val m = HashMap<String, Int>()
            for (k in o.keys()) m[k] = o.getInt(k)
            m as Map<String, Int>
        }.getOrDefault(emptyMap()).also { table = it }
    }

    /** The zone's music by the table: Some(track or null for silent), or None if not listed. */
    private fun fromTable(tracks: List<MusicTrack>, slug: String, table: Map<String, Int>?): Pair<Boolean, MusicTrack?> {
        val n = table?.get(slug) ?: return false to null
        if (n == 0) return true to null
        val t = tracks.filter { it.number == n && it.isBgw }
            .sortedWith(compareBy({ if (it.cat != null) 0 else 1 }, { it.fileName }))
            .firstOrNull() ?: tracks.firstOrNull { it.number == n }
        return true to t
    }
    private val notes = Regex("\\((?!s\\))[^)]*\\)")         // "(Ark Angels)" etc., but not "(S)"

    private fun norm(s: String) = s.lowercase()
        .removePrefix("kingdom of ")                         // "Kingdom of San d'Oria" = the region
        .replace("[s]", "(s)")
        .replace("'", "")                                   // "Chateau dOraguille" = "Chateau d'Oraguille"
        .replace(Regex("\\s*-\\s*"), "-")                   // "Dynamis - Tavnazia" = "Dynamis-Tavnazia"
        .replace(notes, " ")
        .replace(Regex("\\s+"), " ")
        .trim()

    private fun places(heard: String): List<String> =
        heard.split(',').map { norm(it) }.filter { it.isNotEmpty() }

    fun pick(tracks: List<MusicTrack>, zoneName: String, region: String, type: String = "",
             slug: String = "", table: Map<String, Int>? = null): MusicTrack? {
        val (listed, hit) = fromTable(tracks, slug, table)
        if (listed) return hit
        val zone = norm(zoneName)
        val past = zone.endsWith("(s)")
        // Region music only for outdoor and town zones (unknown type counts as outdoor) --
        // and for Dynamis - Divergence [D] areas, which share their content's music.
        val divergence = zone.endsWith("[d]")
        val reg = if (divergence || type.isBlank() || type.equals("Field", true) || type.equals("City", true))
            norm(region).removeSuffix("s").ifEmpty { norm(region) } else ""
        var best: MusicTrack? = null
        var bestScore = 0
        for (t in tracks) {
            val heard = t.heard
            if (heard.isBlank()) continue
            var score = if (norm(t.title) == zone) 6 else 0           // named after the zone
            for (p in places(heard)) {
                val s = when {
                    p == zone -> 5                                   // the zone itself
                    zone.startsWith("$p ") || zone.startsWith("$p-") -> 4   // "castle zvahl" -> ... baileys
                    zone.endsWith(" $p") -> 4                        // "airship" -> bastok-jeuno airship
                    past && p == "$reg (s)" -> 3                     // its region, in the past
                    reg.isNotEmpty() && (p == reg || p.removeSuffix("s") == reg) ->
                        if (past) 1 else 2                           // its region ("Airships")
                    reg.isNotEmpty() && p.startsWith("$reg ") -> 2   // "dynamis-divergence wave 1 / wave 2"
                    else -> 0
                }
                if (s > score) score = s
            }
            if (score > bestScore || (score == bestScore && score > 0 &&
                    (t.number ?: Int.MAX_VALUE) < (best?.number ?: Int.MAX_VALUE))) {
                best = t; bestScore = score
            }
        }
        return if (bestScore > 0) best else null
    }
}
