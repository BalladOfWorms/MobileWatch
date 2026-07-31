package com.balladofworms.mobilewatch

import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.time.LocalDateTime
import java.time.ZoneOffset

/**
 * Domain Invasion location per world, from whereisdi.com's public Directus API
 * (same source the Whereisdi Windower/Ashita addons read; the bearer token is the
 * published read-only anonymous token). Ported from OmniWatch.
 */
object DomainInvasion {
    private const val API_URL = "https://api.whereisdi.com/items/di?fields=*.*"
    private const val TOKEN = "Bearer 82j1GCjQxUCxriN-XhXicb6Ts8G400l7"

    data class DiInfo(val location: String, val updatedEpoch: Long?)

    /** Fetch the current DI zone for [world], or null on error / no report. Call off the main thread. */
    fun fetch(world: String): DiInfo? {
        val conn = (URL(API_URL).openConnection() as HttpURLConnection).apply {
            connectTimeout = 8000; readTimeout = 8000
            setRequestProperty("Authorization", TOKEN)
            setRequestProperty("Accept", "application/json")
            setRequestProperty("User-Agent", "MobileWatch (FFXI companion)")
        }
        return try {
            if (conn.responseCode != 200) return null
            val body = conn.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
            val data = JSONObject(body).optJSONArray("data") ?: return null
            val target = world.lowercase()
            for (i in 0 until data.length()) {
                val e = data.optJSONObject(i) ?: continue
                val srv = e.opt("server")
                val srvName = when (srv) {
                    is JSONObject -> srv.optString("name")
                    is String -> srv
                    else -> ""
                }
                if (srvName.lowercase() != target) continue
                val loc = e.opt("location")
                val locName = when (loc) {
                    is JSONObject -> loc.optString("en_us").ifBlank { loc.optString("ja_jp") }
                    is String -> loc
                    else -> ""
                }
                return DiInfo(locName.ifBlank { "(unknown)" }, parseEpoch(e.optString("date_updated")))
            }
            null
        } catch (e: Exception) {
            null
        } finally {
            conn.disconnect()
        }
    }

    /** API emits UTC ISO-8601 without a 'Z' suffix. */
    private fun parseEpoch(s: String?): Long? {
        if (s.isNullOrBlank() || s.length < 19) return null
        return runCatching { LocalDateTime.parse(s.substring(0, 19)).toEpochSecond(ZoneOffset.UTC) }.getOrNull()
    }
}

/**
 * Limbus NM / ??? spawn reports per world, from whereisnm.com's public REST API
 * (no auth). Ported from OmniWatch.
 */
object WhereIsNm {
    private const val API_URL = "https://whereisnm.com/api/v1/reports"

    data class NmEntry(
        val display: String, val enemy: String, val isQuestion: Boolean,
        val area: String, val minsUpdate: Double?
    )

    fun fetch(world: String): List<WhereIsNm.NmEntry> {
        val conn = (java.net.URL(API_URL).openConnection() as java.net.HttpURLConnection).apply {
            connectTimeout = 8000; readTimeout = 8000
            setRequestProperty("Accept", "application/json")
            setRequestProperty("User-Agent", "MobileWatch (FFXI companion)")
            setRequestProperty("x-client-type", "WhereIsNM-Frontend")
        }
        return try {
            if (conn.responseCode != 200) return emptyList()
            val body = conn.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
            val records = extractRecords(body)
            val tgt = world.lowercase()
            val out = ArrayList<NmEntry>()
            for (i in 0 until records.length()) {
                val r = records.optJSONObject(i) ?: continue
                if (r.optString("server").lowercase() != tgt) continue
                if (r.optBoolean("expired", false)) continue
                val display = r.optString("displayName").ifBlank { r.optString("display_name") }.ifBlank { "(unknown spot)" }
                val enemy = r.optString("enemyDisplay").ifBlank { r.optString("enemy_display") }
                    .ifBlank { r.optString("enemyInput") }.ifBlank { "???" }
                val spawn = r.optString("spawnType").ifBlank { r.optString("spawn_type") }.lowercase()
                val area = r.optString("area").lowercase()
                val mu = r.optDouble("minutesSinceUpdate", r.optDouble("minutes_since_update", Double.NaN))
                out.add(NmEntry(display, enemy, spawn == "question", area, if (mu.isNaN()) null else mu))
            }
            val rank = mapOf("apollyon" to 0, "temenos" to 1)
            out.sortedWith(compareBy({ rank[it.area] ?: 9 }, { it.minsUpdate ?: 1e9 }))
        } catch (e: Exception) {
            emptyList()
        } finally {
            conn.disconnect()
        }
    }

    private fun extractRecords(body: String): org.json.JSONArray {
        val t = body.trim()
        if (t.startsWith("[")) return org.json.JSONArray(t)
        val obj = org.json.JSONObject(t)
        for (k in listOf("reports", "data", "results", "items")) obj.optJSONArray(k)?.let { return it }
        return org.json.JSONArray()
    }
}

/**
 * Official Square Enix events from the PlayOnline FFXI topics RSS feed.
 * Parses each item to title / event-period / short summary / link.
 */
object SeEvents {
    private const val URL = "https://www.playonline.com/pcd2/topics/ff11us/topics.xml"

    data class Event(val title: String, val period: String, val summary: String, val link: String)

    private const val DATE =
        """[A-Z][a-z]+,?\s+[A-Z][a-z]+\s+\d{1,2}(?:,?\s+\d{4})?,?\s+at\s+\d{1,2}:\d{2}\s*[ap]\.?m\.?(?:\s*\([A-Z]+\))?"""
    private val PERIOD_RE = Regex(
        """(?:Event|Campaign|Point\s+distribution|Point\s+exchange|Sale|Discount|Limited\s+Time)\s+Period\s*:?\s*($DATE)\s*to\s*($DATE)""",
        setOf(RegexOption.IGNORE_CASE, RegexOption.DOT_MATCHES_ALL)
    )
    private val PERIOD_RE2 = Regex("""($DATE)\s*to\s*($DATE)""", setOf(RegexOption.IGNORE_CASE, RegexOption.DOT_MATCHES_ALL))
    private val LABEL_RE = Regex(
        """(?:Event|Campaign|Point\s+distribution|Point\s+exchange|Sale|Discount|Limited\s+Time)\s+Period\s*:?""",
        RegexOption.IGNORE_CASE
    )

    // Namespace-agnostic: matches <item>, <rss:item>, <entry>, <atom:entry>, ...
    private val ITEM_RE = Regex("""(?is)<(?:\w+:)?(?:item|entry)\b[^>]*>(.*?)</(?:\w+:)?(?:item|entry)>""")

    fun fetch(): List<SeEvents.Event> {
        val conn = (java.net.URL(URL).openConnection() as java.net.HttpURLConnection).apply {
            connectTimeout = 8000; readTimeout = 10000; instanceFollowRedirects = true
            setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android) MobileWatch/1.0")
            setRequestProperty("Accept", "application/xml, text/xml, application/rss+xml, */*")
        }
        return try {
            if (conn.responseCode != 200) return emptyList()
            val body = conn.inputStream.bufferedReader(Charsets.UTF_8).use { it.readText() }
            val out = ArrayList<Event>()
            val seen = HashSet<String>()
            for (m in ITEM_RE.findAll(body)) {
                val blk = m.groupValues[1]
                val title = htmlToText(tag(blk, "title"))
                if (title.isBlank()) continue
                if (!seen.add(title.take(18).lowercase())) continue   // dedup lifecycle-duplicate titles
                val clean = htmlToText(firstTag(blk, "description", "summary"))
                out.add(Event(title, extractPeriod(clean), extractSummary(clean), getLink(blk)))
            }
            out
        } catch (e: Exception) {
            emptyList()
        } finally {
            conn.disconnect()
        }
    }

    /** Inner text of the first <name>/<ns:name> tag in [block], CDATA-unwrapped. */
    private fun tag(block: String, name: String): String {
        val m = Regex("""(?is)<(?:\w+:)?$name\b[^>]*>(.*?)</(?:\w+:)?$name>""").find(block) ?: return ""
        return m.groupValues[1].trim().removePrefix("<![CDATA[").removeSuffix("]]>").trim()
    }

    private fun firstTag(block: String, vararg names: String): String {
        for (n in names) { val v = tag(block, n); if (v.isNotBlank()) return v }
        return ""
    }

    /** RSS <link>URL</link> text, or Atom <link href="URL"/> attribute. */
    private fun getLink(block: String): String {
        val t = tag(block, "link")
        if (t.isNotBlank()) return t
        val m = Regex("""(?is)<(?:\w+:)?link\b[^>]*\bhref=["']([^"']+)["']""").find(block)
        return m?.groupValues?.get(1) ?: ""
    }

    @Suppress("DEPRECATION")
    private fun htmlToText(html: String): String {
        if (html.isBlank()) return ""
        val text = android.text.Html.fromHtml(html, android.text.Html.FROM_HTML_MODE_LEGACY).toString()
        return text.replace(Regex("""\n{3,}"""), "\n\n").trim()
    }

    private fun extractPeriod(clean: String): String {
        val m = PERIOD_RE.find(clean) ?: PERIOD_RE2.find(clean) ?: return ""
        return "${m.groupValues[1].trim()} to ${m.groupValues[2].trim()}"
    }

    private fun extractSummary(clean: String): String {
        val cut = LABEL_RE.find(clean)?.range?.first ?: -1
        var blurb = if (cut > 0) clean.substring(0, cut).trim() else clean.trim()
        blurb = blurb.replace(Regex("""\n?Read on\s+for details\.?\s*$""", RegexOption.IGNORE_CASE), "").trim()
        if (blurb.length > 300) blurb = blurb.substring(0, 300).trimEnd() + "\u2026"
        return blurb
    }
}
