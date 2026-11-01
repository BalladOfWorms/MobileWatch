package com.balladofworms.mobilewatch

/**
 * Gear stats, read from the item text the way the game prints it ("DEF:155 HP+127 Accuracy+64
 * "Fast Cast"+5% Haste+3%") and from your copies' augments, which use the same wording.
 *
 * What a piece gives you is summed; what a piece gives your pet ("Pet:", "Avatar:", "Automaton:",
 * "Wyvern:", "Luopan:") is summed apart. Anything that only applies sometimes -- a latent effect,
 * a set bonus, day or weather, Unity rank, Dynamis, aftermath, "Citizen of..." -- is never added
 * in: it's kept as the item's own words and listed under the totals, so the numbers stay honest.
 */
object GearStats {
    /** One stat the panel knows by name. pct: shown with a %. lowerBetter: DT and friends. */
    data class Def(val key: String, val label: String, val group: String, val pct: Boolean = false,
                   val lowerBetter: Boolean = false)

    val GROUPS = listOf("Attributes", "Melee", "Ranged", "Magic", "Defence", "Utility", "Skills", "Other")

    private val DEFS: List<Pair<Def, List<String>>> = listOf(
        Def("hp", "HP", "Attributes") to listOf("hp"),
        Def("mp", "MP", "Attributes") to listOf("mp"),
        Def("str", "STR", "Attributes") to listOf("str"),
        Def("dex", "DEX", "Attributes") to listOf("dex"),
        Def("vit", "VIT", "Attributes") to listOf("vit"),
        Def("agi", "AGI", "Attributes") to listOf("agi"),
        Def("int", "INT", "Attributes") to listOf("int"),
        Def("mnd", "MND", "Attributes") to listOf("mnd"),
        Def("chr", "CHR", "Attributes") to listOf("chr"),

        Def("acc", "Accuracy", "Melee") to listOf("accuracy", "acc"),
        Def("att", "Attack", "Melee") to listOf("attack", "atk", "att"),
        Def("da", "Double Attack", "Melee", pct = true) to listOf("doubleattack", "dblatk"),
        Def("ta", "Triple Attack", "Melee", pct = true) to listOf("tripleattack", "trplatk", "tripleatk"),
        Def("qa", "Quad. Attack", "Melee", pct = true) to listOf("quadrupleattack", "quadattack", "quadatk"),
        Def("stp", "Store TP", "Melee") to listOf("storetp", "stp"),
        Def("crit", "Crit. rate", "Melee", pct = true) to listOf("criticalhitrate", "crithitrate", "critrate"),
        Def("critdmg", "Crit. damage", "Melee", pct = true) to listOf("criticalhitdamage", "crithitdamage", "crithitdmg", "critdmg"),
        Def("wsd", "WS damage", "Melee", pct = true) to listOf("weaponskilldamage", "weaponskilldmg", "wsdamage", "wsdmg"),
        Def("dw", "Dual Wield", "Melee", pct = true) to listOf("dualwield"),
        Def("sb", "Subtle Blow", "Melee") to listOf("subtleblow"),
        Def("sb2", "Subtle Blow II", "Melee") to listOf("subtleblowii"),
        Def("pdl", "Phys. dmg. limit", "Melee", pct = true) to listOf("physicaldamagelimit", "physdmglimit"),
        Def("tpb", "TP Bonus", "Melee") to listOf("tpbonus"),
        Def("regain", "Regain", "Melee") to listOf("regain"),
        Def("sc", "Skillchain Bonus", "Melee") to listOf("skillchainbonus"),
        Def("counter", "Counter", "Melee", pct = true) to listOf("counter"),
        Def("ma", "Martial Arts", "Melee") to listOf("martialarts"),
        Def("kick", "Kick Attacks", "Melee", pct = true) to listOf("kickattacks"),
        Def("zanshin", "Zanshin", "Melee", pct = true) to listOf("zanshin"),

        Def("racc", "Rng. Accuracy", "Ranged") to listOf("rangedaccuracy", "rngacc", "racc", "raccuracy", "rangedacc"),
        Def("ratt", "Rng. Attack", "Ranged") to listOf("rangedattack", "rngatk", "ratk", "rattack", "rangedatk"),
        Def("snap", "Snapshot", "Ranged", pct = true) to listOf("snapshot"),
        Def("rapid", "Rapid Shot", "Ranged", pct = true) to listOf("rapidshot"),
        Def("barrage", "Barrage", "Ranged") to listOf("barrage"),

        Def("macc", "Magic Accuracy", "Magic") to listOf("magicaccuracy", "magacc", "macc", "maccuracy", "magicacc"),
        Def("mab", "Magic Atk. Bonus", "Magic") to listOf("magicatkbonus", "magatkbns", "matkbonus", "magicattackbonus", "mab"),
        Def("mdmg", "Magic Damage", "Magic") to listOf("magicdamage", "magdmg", "magicdmg"),
        Def("fc", "Fast Cast", "Magic", pct = true) to listOf("fastcast"),
        Def("cure", "Cure potency", "Magic", pct = true) to listOf("curepotency", "curepot"),
        Def("cure2", "Cure potency II", "Magic", pct = true) to listOf("curepotencyii", "curepotii"),
        Def("curerecv", "Cure received", "Magic", pct = true) to listOf("curepotencyreceived", "curepotreceived", "curereceived", "potencyofcureeffectsreceived"),
        Def("mbb", "Magic burst dmg.", "Magic") to listOf("magicburstdamage", "magicburstdmg", "magburstdmg", "magicburstbonus", "magburstbonus", "mbb"),
        Def("mbb2", "Magic burst dmg. II", "Magic") to listOf("magicburstdamageii", "magicburstdmgii", "magburstdmgii", "magicburstbonusii", "mbbii"),
        Def("cmp", "Conserve MP", "Magic") to listOf("conservemp"),
        Def("qm", "Quick Magic", "Magic", pct = true) to listOf("quickmagic", "occquickensspellcasting", "occasionallyquickensspellcasting"),
        Def("sird", "Spell interrupt. rate", "Magic", pct = true, lowerBetter = true) to listOf("spellinterruptionratedown", "spellinterruptionrate", "spellinterruptiondown"),
        Def("enhdur", "Enhancing duration", "Magic", pct = true) to listOf("enhancingmagicduration", "enhancingmagiceffectduration", "enhmagduration", "enhancingmagicdur"),
        Def("song", "Song cast time", "Magic", pct = true, lowerBetter = true) to listOf("songspellcastingtime"),

        Def("def", "DEF", "Defence") to listOf("def", "defense"),
        Def("eva", "Evasion", "Defence") to listOf("evasion", "eva"),
        Def("meva", "Magic Evasion", "Defence") to listOf("magicevasion", "magevasion", "mageva", "meva", "magiceva"),
        Def("mdb", "Magic Def. Bonus", "Defence") to listOf("magicdefbonus", "magdefbns", "mdefbonus", "magicdefensebonus", "mdefb", "mdefbns", "mdb"),
        Def("dt", "Damage taken", "Defence", pct = true, lowerBetter = true) to listOf("damagetaken", "dmgtaken", "dt"),
        Def("pdt", "Phys. dmg. taken", "Defence", pct = true, lowerBetter = true) to listOf("physicaldamagetaken", "physdmgtaken", "physicaldmgtaken", "pdt"),
        Def("mdt", "Magic dmg. taken", "Defence", pct = true, lowerBetter = true) to listOf("magicdamagetaken", "magicdmgtaken", "magdmgtaken", "mdt"),
        Def("pdt2", "Phys. dmg. taken II", "Defence", pct = true, lowerBetter = true) to listOf("physicaldamagetakenii", "physdmgtakenii"),
        Def("mdt2", "Magic dmg. taken II", "Defence", pct = true, lowerBetter = true) to listOf("magicdamagetakenii", "magicdmgtakenii", "magdmgtakenii"),
        Def("resall", "Resist all elements", "Defence") to listOf("resistallelements", "resallele", "allelementalresistances", "allelementalresistance"),
        Def("bdt", "Breath dmg. taken", "Defence", pct = true, lowerBetter = true) to listOf("breathdamagetaken", "breathdmgtaken"),

        Def("haste", "Haste", "Utility", pct = true) to listOf("haste"),
        Def("refresh", "Refresh", "Utility") to listOf("refresh"),
        Def("regen", "Regen", "Utility") to listOf("regen"),
        Def("enmity", "Enmity", "Utility") to listOf("enmity"),
        Def("th", "Treasure Hunter", "Utility") to listOf("treasurehunter"),
        Def("move", "Movement speed", "Utility", pct = true) to listOf("movementspeed"),
    )

    private val BY_ALIAS: Map<String, Def> = HashMap<String, Def>().apply {
        DEFS.forEach { (d, names) -> names.forEach { put(it, d) } }
    }
    private val BY_KEY: Map<String, Def> = DEFS.associate { it.first.key to it.first }
    private val ORDER: Map<String, Int> = DEFS.mapIndexed { i, p -> p.first.key to i }.toMap()

    fun def(key: String): Def = BY_KEY[key] ?: run {
        // Not one the panel knows by name: kept under its own words, in Skills or Other.
        val label = key.removePrefix("x:")
        Def(key, label, if (label.endsWith(" skill", true) || label.endsWith(" skills", true)) "Skills" else "Other",
            pct = false)
    }

    /** Gear caps worth flagging. DT shows against -50% as PDT (DT + PDT) and MDT (DT + MDT). */
    val CAPS: Map<String, Int> = mapOf("haste" to 25, "fc" to 80, "cure" to 50, "cure2" to 30, "mbb" to 40, "sb" to 50)
    const val DT_CAP = -50

    // A stat is a name then a signed number, as in HP+127, "Fast Cast"+5%, Damage taken-7%,
    // Healing magic skill +34. The name is letters, dots, apostrophes and spaces.
    private val TOKEN = Regex("(?<![A-Za-z0-9])([A-Za-z][A-Za-z.' \\-]*?)\\s?([+-]\\d+)(%?)")
    private val FIXED = Regex("\\b(DEF|DMG|Delay):\\s?([+-]?\\d+)")
    private val SIRD = Regex("Spell interruption rate down\\s*(\\d+)%", RegexOption.IGNORE_CASE)
    private val PET_HEAD = Regex("^(Pet|Avatar|Automaton|Wyvern|Luopan)(\\s*(&|and)\\s*\\w+)?\\s*:\\s*", RegexOption.IGNORE_CASE)
    private val COND_HEAD = Regex("^[A-Z][^:+\\-%0-9\"]{1,44}:")

    private fun aliasKey(name: String) = name.lowercase().filter { it.isLetterOrDigit() }

    /** What one piece gives. stats/pet: key -> value. weapon: DMG and Delay. cond: the item's own
     *  words for what applies only sometimes. */
    class Parsed(
        val stats: MutableMap<String, Int> = LinkedHashMap(),
        val pet: MutableMap<String, Int> = LinkedHashMap(),
        var dmg: Int = 0, var delay: Int = 0,
        val cond: MutableList<String> = ArrayList(),
    )

    private fun add(into: MutableMap<String, Int>, rawName: String, value: Int) {
        val name = rawName.trim()
        if (name.isEmpty()) return
        // A known stat at the end of a longer phrase still counts ("Occasionally Haste" is not a
        // thing, but wording can run into a stat); an unknown phrase of more than four words is
        // a sentence, not a stat, and is left out.
        val words = name.split(' ').filter { it.isNotBlank() }
        var d = BY_ALIAS[aliasKey(name)]
        if (d == null) for (n in minOf(words.size - 1, 5) downTo 1) {
            d = BY_ALIAS[aliasKey(words.takeLast(n).joinToString(" "))]
            if (d != null) break
        }
        val key = d?.key ?: if (words.size <= 4) "x:" + name.trimEnd('.').replaceFirstChar { it.uppercase() } else return
        into[key] = (into[key] ?: 0) + value
    }

    private fun scan(text: String, into: MutableMap<String, Int>, p: Parsed, weapon: Boolean) {
        var rest = text
        FIXED.findAll(text).forEach { m ->
            val v = m.groupValues[2].toInt()
            when (m.groupValues[1]) {
                "DEF" -> into["def"] = (into["def"] ?: 0) + v
                "DMG" -> if (weapon) p.dmg += v
                "Delay" -> if (weapon) p.delay += v
            }
            rest = rest.replace(m.value, " ")
        }
        rest = rest.replace(Regex("\\(Max\\.?\\s*\\d+\\)"), " ").replace("\"", "")
        // Printed without a sign: "Spell interruption rate down 10%".
        SIRD.find(rest)?.let { m ->
            into["sird"] = (into["sird"] ?: 0) - m.groupValues[1].toInt()   // "down": stored as -N, as OmniWatch does
            rest = rest.replace(m.value, " ")
        }
        TOKEN.findAll(rest).forEach { m -> add(into, m.groupValues[1], m.groupValues[2].toInt()) }
    }

    /** Read one item: its description, then the augments on this copy (or the ones the lua names). */
    fun parse(desc: String, augs: List<String>): Parsed {
        val p = Parsed()
        var mode = 0                         // 0 you, 1 pet, 2 only sometimes
        val cond = StringBuilder()
        for (raw in desc.split('\n')) {
            var line = raw.trim()
            if (line.isEmpty()) continue
            if (mode != 2) {
                val pet = PET_HEAD.find(line)
                if (pet != null) { mode = 1; line = line.substring(pet.value.length) }
                else if (COND_HEAD.containsMatchIn(line) && !line.startsWith("DEF") && !line.startsWith("DMG")
                    && !line.startsWith("Cannot Equip")) mode = 2
            }
            when (mode) {
                0 -> scan(line, p.stats, p, weapon = true)
                1 -> scan(line, p.pet, p, weapon = false)
                else -> { if (cond.isNotEmpty()) cond.append(' '); cond.append(line) }
            }
        }
        if (cond.isNotEmpty()) p.cond.add(cond.toString())
        for (a in augs) {
            val s = a.trim()
            if (s.isEmpty() || s.startsWith("Path:", true) || s.startsWith("Rank:", true)) continue
            val pet = PET_HEAD.find(s)
            if (pet != null) scan(s.substring(pet.value.length), p.pet, p, weapon = false)
            else scan(s, p.stats, p, weapon = true)
        }
        return p
    }

    private val cache = HashMap<String, Parsed>()

    /**
     * Stats some items have that their text doesn't print ("Enhances "Dual Wield" effect" is +5 on
     * one item, +3 on another): OmniWatch's own ow_enhanced table, item id -> "dual wield+5", from
     * assets/item_enhanced.json. Without it a piece like that would read as giving nothing.
     */
    @Volatile var enhanced: Map<Int, String> = emptyMap()
        set(v) { field = v; synchronized(this) { cache.clear() } }

    @Synchronized
    fun of(item: Item, augs: List<String>): Parsed =
        cache.getOrPut(item.id.toString() + "|" + augs.joinToString("\u001f")) {
            parse(item.desc, augs + listOfNotNull(enhanced[item.id]))
        }

    /** The grid, summed. */
    class Totals(
        val stats: Map<String, Int>,
        val pet: Map<String, Int>,
        val weapons: List<Triple<String, Int, Int>>,     // slot label, DMG, Delay
        val cond: List<Pair<String, String>>,            // item name, words
    )

    /** pieces: slot key -> (item, augments). */
    fun total(pieces: Map<String, Pair<Item, List<String>>>): Totals {
        val st = LinkedHashMap<String, Int>()
        val pet = LinkedHashMap<String, Int>()
        val weapons = ArrayList<Triple<String, Int, Int>>()
        val cond = ArrayList<Pair<String, String>>()
        for (slot in GearSlots.GRID) {
            val (item, augs) = pieces[slot.key] ?: continue
            val p = of(item, augs)
            p.stats.forEach { (k, v) -> st[k] = (st[k] ?: 0) + v }
            p.pet.forEach { (k, v) -> pet[k] = (pet[k] ?: 0) + v }
            if (p.dmg > 0 || p.delay > 0) weapons.add(Triple(slot.label, p.dmg, p.delay))
            p.cond.forEach { cond.add(item.name to it) }
        }
        return Totals(st, pet, weapons, cond)
    }

    /** Sort keys the panel's way: its own order for known stats, then alphabetically. */
    fun sorted(keys: Collection<String>): List<String> =
        keys.sortedWith(compareBy({ ORDER[it] ?: Int.MAX_VALUE }, { it.lowercase() }))

    /** "+12", "-3%", "25%". */
    fun fmt(key: String, v: Int, signed: Boolean = true): String {
        val d = def(key)
        val n = if (signed && v > 0) "+$v" else "$v"
        return if (d.pct) "$n%" else n
    }

    /** What putting `next` in place of `now` changes, most important first. */
    fun diff(now: Parsed?, next: Parsed?): List<Pair<String, Int>> {
        val keys = LinkedHashSet<String>()
        now?.stats?.keys?.let { keys.addAll(it) }
        next?.stats?.keys?.let { keys.addAll(it) }
        return sorted(keys).mapNotNull { k ->
            val d = (next?.stats?.get(k) ?: 0) - (now?.stats?.get(k) ?: 0)
            if (d == 0) null else k to d
        }
    }

    /** Whether a change is for the better: green, else red. Other/Skills count up as better too. */
    fun better(key: String, delta: Int): Boolean = if (def(key).lowerBetter) delta < 0 else delta > 0
}
