package com.balladofworms.mobilewatch

import kotlin.math.truncate

/**
 * The Character tab's Statistics grid: OmniWatch's cells, in OmniWatch's order, with OmniWatch's
 * keys, formats, colours and caps, so the two read the same.
 *
 * Where the numbers come from:
 *  - When OmniWatch has seen you on the job, its panel values (base stats, skills, traits, merits,
 *    Job Points, food and buffs all included) arrive with the gear that was worn when they were
 *    read. The grid shows those, moved by the difference between that gear and the set on the
 *    phone, as the phone's own gear sums find it. Gear the phone swaps also moves what it feeds:
 *    DEX into accuracy, STR into attack, AGI into ranged accuracy and evasion, VIT into defence,
 *    Store TP into TP per hit.
 *  - Without that, the grid is gear only, and the cells only OmniWatch can know show "--".
 */
object StatsModel {
    data class Cell(val key: String, val label: String, val element: Boolean = false)

    /** null = an empty square. */
    val GRID: List<List<Cell?>> = listOf(
        listOf(Cell("str", "STR"), Cell("dex", "DEX"), Cell("vit", "VIT"), Cell("agi", "AGI"),
            Cell("int", "INT"), Cell("mnd", "MND"), Cell("chr", "CHR")),
        listOf(Cell("haste", "Gear Haste"), Cell("magic haste", "Magic Haste"), Cell("ja haste", "JA Haste"),
            Cell("total haste", "Total Haste"), Cell("tp per hit", "TP/Hit"), Cell("hits to ws", "Hit→WS"),
            Cell("weapon skill damage", "WSD")),
        listOf(Cell("dual wield", "DW Gear"), Cell("dw trait", "DW Traits"), Cell("dw needed", "DW To Cap"),
            Cell("double attack", "DA"), Cell("triple attack", "TA"), Cell("quadruple attack", "QA"),
            Cell("store tp", "STP")),
        listOf(Cell("accuracy", "Acc1"), Cell("accuracy2", "Acc2"), Cell("attack", "Att1"), Cell("attack2", "Att2"),
            Cell("critical hit rate", "Crit"), Cell("subtle blow", "S.Blow"), Cell("enmity", "Emn.")),
        listOf(Cell("ranged accuracy", "RAcc"), Cell("ranged attack", "RAtt"), Cell("snapshot", "Snapshot"),
            Cell("rapid shot", "R.Shot"), Cell("regen", "Regen"), Cell("refresh", "Refresh"), Cell("regain", "Regain")),
        listOf(Cell("damage taken", "DT"), Cell("physical damage taken", "PDT"), Cell("magic damage taken", "MDT"),
            Cell("breath damage taken", "BDT"), Cell("defense", "Def"), Cell("evasion", "Eva"),
            Cell("magic evasion", "MEva")),
        listOf(Cell("fast cast", "Fast Cast"), Cell("quick magic", "Quick Magic"),
            Cell("spell interruption rate", "S.Int."), Cell("magic accuracy", "MAcc"),
            Cell("magic attack bonus", "MAB"), Cell("cure potency", "Cure Pot"), Cell("magic def. bonus", "MDB")),
        listOf(Cell("fire", "Fire", true), Cell("thunder", "Lightning", true), Cell("earth", "Earth", true),
            Cell("wind", "Wind", true), null, null, Cell("_resist", "Resist")),
        listOf(Cell("ice", "Ice", true), Cell("water", "Water", true), Cell("light", "Light", true),
            Cell("dark", "Dark", true), null, null, Cell("movement speed", "SPEED")),
    )

    /** The panel as the phone lays it out: the attributes across the top, then OmniWatch's cells
     *  under Attack, Magic, Defense and Misc, each a label and a value. */
    val ATTRIBUTES = listOf("str" to "STR", "dex" to "DEX", "vit" to "VIT", "agi" to "AGI",
        "int" to "INT", "mnd" to "MND", "chr" to "CHR")
    val SECTIONS: List<Pair<String, List<Pair<String, String>>>> = listOf(
        "Attack" to listOf(
            "accuracy" to "Acc1", "accuracy2" to "Acc2", "attack" to "Att1", "attack2" to "Att2",
            "ranged accuracy" to "RAcc", "ranged attack" to "RAtt",
            "haste" to "Gear Haste", "magic haste" to "Magic Haste", "ja haste" to "JA Haste",
            "total haste" to "Total Haste", "dual wield" to "DW Gear", "dw trait" to "DW Traits",
            "dw needed" to "DW To Cap", "double attack" to "DA", "triple attack" to "TA",
            "quadruple attack" to "QA", "store tp" to "STP", "critical hit rate" to "Crit",
            "weapon skill damage" to "WSD", "subtle blow" to "S.Blow",
            "tp per hit" to "TP/Hit", "hits to ws" to "Hit→WS",
            "snapshot" to "Snapshot", "rapid shot" to "R.Shot"),
        "Magic" to listOf(
            "magic accuracy" to "MAcc", "magic attack bonus" to "MAB",
            "fast cast" to "Fast Cast", "quick magic" to "Quick Magic",
            "spell interruption rate" to "S.Int.", "cure potency" to "Cure Pot"),
        "Defense" to listOf(
            "damage taken" to "DT", "physical damage taken" to "PDT",
            "magic damage taken" to "MDT", "breath damage taken" to "BDT",
            "defense" to "Def", "evasion" to "Eva", "magic evasion" to "MEva",
            "magic def. bonus" to "MDB",
            "fire" to "Fire", "ice" to "Ice", "wind" to "Wind", "earth" to "Earth",
            "thunder" to "Lightning", "water" to "Water", "light" to "Light", "dark" to "Dark"),
        "Misc" to listOf(
            "regen" to "Regen", "refresh" to "Refresh", "regain" to "Regain",
            "enmity" to "Emn.", "movement speed" to "Speed"),
    )

    // OmniWatch's display rules (OmniWatch.py: PERCENT_CELLS, INVERT_SIGN_CELLS, TOTAL_CELLS,
    // NO_SIGN_CELLS, STAT_CAPS).
    val PERCENT = setOf("haste", "magic haste", "ja haste", "total haste", "double attack", "triple attack",
        "quadruple attack", "dual wield", "dw trait", "dw needed", "weapon skill damage", "fast cast",
        "quick magic", "critical hit rate", "spell interruption rate", "cure potency", "damage taken",
        "physical damage taken", "magic damage taken", "breath damage taken", "movement speed")
    val INVERT = setOf("damage taken", "physical damage taken", "magic damage taken", "breath damage taken",
        "spell interruption rate")
    val TOTAL = setOf("accuracy", "attack", "accuracy2", "attack2", "ranged accuracy", "ranged attack",
        "defense", "evasion", "tp per hit", "hits to ws")
    val NO_SIGN = setOf("dw trait", "dw needed", "total haste")
    val CAPS: Map<String, Double> = mapOf(
        "haste" to 25.0, "magic haste" to 43.75, "ja haste" to 25.0, "total haste" to 80.0,
        "dual wield" to 80.0, "fast cast" to 80.0, "quick magic" to 50.0, "store tp" to 100.0,
        "subtle blow" to 50.0, "enmity" to 100.0, "spell interruption rate" to -100.0,
        "cure potency" to 50.0, "movement speed" to 60.0, "physical damage taken" to -50.0,
        "magic damage taken" to -50.0, "breath damage taken" to -50.0, "damage taken" to -50.0,
    )

    /** Cells that are gear and nothing else in OmniWatch's panel: shown straight from the set. */
    val GEAR_ONLY = setOf("haste", "dual wield", "critical hit rate", "enmity", "quick magic")

    /** Cells only OmniWatch can fill: buffs, traits and the TP maths. */
    private val ONLY_OW = setOf("magic haste", "ja haste", "total haste", "tp per hit", "hits to ws",
        "dw trait", "dw needed")

    /** Which cells lean on the weapons' skill and delay: a weapon swap makes them estimates. */
    val WEAPON_BOUND = setOf("accuracy", "accuracy2", "attack", "attack2", "ranged accuracy", "ranged attack",
        "tp per hit", "hits to ws", "dw needed")

    /** The phone's gear sums, under OmniWatch's keys. PDT/MDT/BDT carry DT, as OmniWatch's do. */
    fun gearAsOw(g: Map<String, Int>): Map<String, Double> {
        fun v(k: String) = (g[k] ?: 0).toDouble()
        val m = HashMap<String, Double>()
        for (k in listOf("str", "dex", "vit", "agi", "int", "mnd", "chr", "haste", "regen", "refresh", "regain", "enmity", "snapshot"))
            m[k] = v(if (k == "snapshot") "snap" else k)
        m["weapon skill damage"] = v("wsd"); m["dual wield"] = v("dw")
        m["double attack"] = v("da"); m["triple attack"] = v("ta"); m["quadruple attack"] = v("qa")
        m["store tp"] = v("stp"); m["critical hit rate"] = v("crit"); m["subtle blow"] = v("sb")
        m["accuracy"] = v("acc"); m["accuracy2"] = v("acc"); m["attack"] = v("att"); m["attack2"] = v("att")
        m["ranged accuracy"] = v("racc"); m["ranged attack"] = v("ratt"); m["rapid shot"] = v("rapid")
        m["damage taken"] = v("dt"); m["physical damage taken"] = v("dt") + v("pdt")
        m["magic damage taken"] = v("dt") + v("mdt"); m["breath damage taken"] = v("dt") + v("bdt")
        m["defense"] = v("def"); m["evasion"] = v("eva"); m["magic evasion"] = v("meva")
        m["magic def. bonus"] = v("mdb"); m["fast cast"] = v("fc"); m["quick magic"] = v("qm")
        m["spell interruption rate"] = v("sird"); m["magic accuracy"] = v("macc")
        m["magic attack bonus"] = v("mab"); m["cure potency"] = v("cure"); m["movement speed"] = v("move")
        for (e in listOf("fire", "thunder", "earth", "wind", "ice", "water", "light", "dark")) m[e] = v("resall")
        return m
    }

    class Values(
        val v: Map<String, Double?>,        // cell key -> value (null = "--")
        val approx: Set<String>,            // estimates: the weapons differ from what OmniWatch saw
        val anchored: Boolean,              // OmniWatch's numbers underneath
    )

    /**
     * set: the phone's gear sums for the grid. anchor: OmniWatch's panel for this job, and
     * worn: the phone's gear sums for the gear worn when it was read. weaponsDiffer: main, sub or
     * range isn't the piece OmniWatch saw.
     */
    fun values(set: Map<String, Int>, anchor: Map<String, Double>?, worn: Map<String, Int>?,
               weaponsDiffer: Boolean): Values {
        val g = gearAsOw(set)
        val out = HashMap<String, Double?>()
        if (anchor == null || worn == null) {
            for (row in GRID) for (c in row) {
                if (c == null || c.key.startsWith("_")) continue
                out[c.key] = if (c.key in ONLY_OW) null else g[c.key]?.takeIf { it != 0.0 }
            }
            return Values(out, emptySet(), false)
        }
        val w = gearAsOw(worn)
        fun d(k: String) = (g[k] ?: 0.0) - (w[k] ?: 0.0)
        fun tr(x: Double) = truncate(x)
        for (row in GRID) for (c in row) {
            if (c == null || c.key.startsWith("_")) continue
            val base = anchor[c.key]
            out[c.key] = when (c.key) {
                "magic haste", "ja haste", "dw trait" -> base
                // Gear and nothing else: the set's own sum, so what you were wearing in game
                // never shows through.
                in GEAR_ONLY -> g[c.key]?.takeIf { it != 0.0 }
                else -> if (base == null && d(c.key) == 0.0) null else (base ?: 0.0) + d(c.key)
            }
        }
        // What the attributes feed (the in-game formulas; the gear sums above already carry each
        // stat's own +Accuracy, +Attack...).
        val dStr = d("str"); val dDex = d("dex"); val dAgi = d("agi"); val dVit = d("vit")
        fun bump(k: String, by: Double) { out[k]?.let { out[k] = it + by } }
        bump("accuracy", tr(dDex * 0.75)); bump("accuracy2", tr(dDex * 0.75))
        bump("attack", dStr); bump("attack2", tr(dStr * 0.5))
        bump("ranged accuracy", tr(dAgi * 0.75)); bump("ranged attack", dStr)
        bump("evasion", tr(dAgi * 0.5)); bump("defense", tr(dVit * 1.5))
        // Haste: gear haste only counts to its 25% cap inside the total.
        val hasteNow = anchor["haste"]; val hasteNew = out["haste"]
        if (hasteNow != null && hasteNew != null) anchor["total haste"]?.let {
            out["total haste"] = it - minOf(hasteNow, 25.0) + minOf(hasteNew, 25.0)
        }
        // Dual Wield still needed from gear drops by whatever DW the set adds.
        anchor["dw needed"]?.let { out["dw needed"] = it - d("dual wield") }
        // TP per hit moves with Store TP (same weapons); hits to WS follows it.
        val stpNow = anchor["store tp"] ?: 0.0
        val stpNew = out["store tp"] ?: stpNow
        anchor["tp per hit"]?.let { tp ->
            val nt = tp * (100 + stpNew) / (100 + stpNow)
            out["tp per hit"] = nt
            anchor["hits to ws"]?.let { h -> if (nt > 0) out["hits to ws"] = h * tp / nt }
        }
        return Values(out, if (weaponsDiffer) WEAPON_BOUND else emptySet(), true)
    }

    /** Dual Wield % needed for the delay cap at [haste] % total haste (80% cap). */
    fun dwRequired(haste: Double): Double {
        val h = haste.coerceIn(0.0, 80.0) / 100.0
        return kotlin.math.max(0.0, kotlin.math.ceil(100.0 * (1.0 - 0.2 / (1.0 - h))))
    }

    /**
     * Add buffs and food (OmniWatch's sim keys, from [SimBuffs]) on top of [base]. Flat stats add
     * to their cells; "attack pct" and "defense pct" scale the totals (only when they are totals,
     * i.e. OmniWatch's numbers are underneath); attributes also feed Accuracy/Attack/Evasion/
     * Defense as gear attributes do; haste rebuilds Total Haste from its three parts, each to its
     * cap, and DW To Cap follows it.
     */
    fun withBuffs(base: Values, buffs: Map<String, Double>): Values {
        if (buffs.isEmpty()) return base
        val out = HashMap(base.v)
        fun add(k: String, by: Double) { if (by != 0.0) out[k] = (out[k] ?: 0.0) + by }
        val skip = setOf("attack pct", "defense pct", "accuracy", "attack", "hp", "mp")
        for ((k, v) in buffs) if (k !in skip) add(k, v)
        add("accuracy", buffs["accuracy"] ?: 0.0); add("accuracy2", buffs["accuracy"] ?: 0.0)
        add("attack", buffs["attack"] ?: 0.0); add("attack2", buffs["attack"] ?: 0.0)
        if (base.anchored) {
            fun tr(x: Double) = truncate(x)
            val dStr = buffs["str"] ?: 0.0; val dDex = buffs["dex"] ?: 0.0
            val dAgi = buffs["agi"] ?: 0.0; val dVit = buffs["vit"] ?: 0.0
            fun bump(k: String, by: Double) { out[k]?.let { out[k] = it + by } }
            bump("accuracy", tr(dDex * 0.75)); bump("accuracy2", tr(dDex * 0.75))
            bump("attack", dStr); bump("attack2", tr(dStr * 0.5))
            bump("ranged accuracy", tr(dAgi * 0.75)); bump("ranged attack", dStr)
            bump("evasion", tr(dAgi * 0.5)); bump("defense", tr(dVit * 1.5))
            buffs["attack pct"]?.let { p ->
                for (k in listOf("attack", "attack2", "ranged attack")) out[k]?.let { out[k] = Math.floor(it * (1 + p / 100)) }
            }
            buffs["defense pct"]?.let { p -> out["defense"]?.let { out["defense"] = Math.floor(it * (1 + p / 100)) } }
        }
        if ((buffs["magic haste"] ?: 0.0) != 0.0 || (buffs["ja haste"] ?: 0.0) != 0.0) {
            val before = base.v["total haste"]
            val total = (minOf(out["haste"] ?: 0.0, 25.0) + minOf(out["magic haste"] ?: 0.0, 43.75) +
                minOf(out["ja haste"] ?: 0.0, 25.0)).coerceAtMost(80.0)
            out["total haste"] = Math.round(total * 10) / 10.0
            val need = base.v["dw needed"]
            if (need != null && before != null) out["dw needed"] = need + dwRequired(total) - dwRequired(before)
        }
        return Values(out, base.approx, base.anchored)
    }

    enum class Tone { NONE, GOOD, BAD, PLAIN, WARN }

    /** The text and colour OmniWatch would give this value (anchored), or the gear-only form. */
    fun format(key: String, value: Double?, anchored: Boolean): Pair<String, Tone> {
        if (value == null) return "--" to Tone.NONE
        if ((anchored && key in TOTAL) || key == "defense") {
            return (if (key == "hits to ws") String.format("%.1f", value) else Math.round(value).toString()) to Tone.PLAIN
        }
        val isInt = value == Math.floor(value)
        val txt0 = when {
            !isInt -> if (key in NO_SIGN) String.format("%.1f", value) else String.format("%+.1f", value)
            key in NO_SIGN || key == "dw needed" -> value.toInt().toString()
            value.toInt() == 0 -> "0"
            else -> String.format("%+d", value.toInt())
        }
        val txt = if (key in PERCENT) "$txt0%" else txt0
        CAPS[key]?.let { cap ->
            if (if (key in INVERT) value < cap else value > cap) return txt to Tone.BAD
        }
        if (key == "dw needed") return txt to when { value < 0 -> Tone.BAD; value == 0.0 -> Tone.GOOD; else -> Tone.WARN }
        val good = if (key in INVERT) value < 0 else value > 0
        val bad = if (key in INVERT) value > 0 else value < 0
        return txt to when { good -> Tone.GOOD; bad -> Tone.BAD; else -> Tone.PLAIN }
    }

    /** A change between two values is good when it moves the stat the right way. */
    fun better(key: String, delta: Double): Boolean = when (key) {
        "hits to ws", "dw needed" -> delta < 0
        in INVERT -> delta < 0
        else -> delta > 0
    }
}
