package com.balladofworms.mobilewatch

import org.luaj.vm2.Globals
import org.luaj.vm2.LoadState
import org.luaj.vm2.LuaTable
import org.luaj.vm2.LuaValue
import org.luaj.vm2.compiler.LuaC
import org.luaj.vm2.lib.BaseLib
import org.luaj.vm2.lib.Bit32Lib
import org.luaj.vm2.lib.MathLib
import org.luaj.vm2.lib.PackageLib
import org.luaj.vm2.lib.StringLib
import org.luaj.vm2.lib.TableLib

/**
 * Buffs and food for the Character tab, from OmniWatch's own sim (assets/omniwatch_sim.lua is
 * OmniWatch_Sim.lua as it ships). The phone runs that file with LuaJ and asks it, the same way
 * OmniWatch does: its BUFF_DATA lists the songs, rolls and spells, its compute turns the picks
 * into stat additions, and its food table does the same for food. A newer OmniWatch_Sim.lua
 * dropped into assets brings its buffs along with no code change here.
 */
object SimBuffs {
    data class Def(val id: String, val job: String, val name: String, val kind: String,
                   val plusMax: Int, val optimalJob: String, val notes: String)

    /** One buff you've put up. level is a roll's number (1-11); plus is Song+/Roll+/Geomancy+. */
    data class Active(val id: String, val plus: Int = 0, val level: Int = 11, val optimal: Boolean = false,
                      val sv: Boolean = false, val marcato: Boolean = false, val cc: Boolean = false,
                      val bolster: Boolean = false)

    class Engine(src: String) {
        private val m: LuaTable
        val defs: List<Def>
        /** Food ids the sim knows, in its own order. */
        val foods: List<Int>

        init {
            val g = Globals()
            g.load(BaseLib()); g.load(PackageLib()); g.load(Bit32Lib())
            g.load(TableLib()); g.load(StringLib()); g.load(MathLib())
            LoadState.install(g)
            LuaC.install(g)
            // Only the export/import paths touch windower; buffs and food never do.
            g.set("windower", LuaTable())
            m = g.load(src, "=omniwatch_sim").call().checktable()
            val list = m.get("list_buffs").call()
            val out = ArrayList<Def>()
            for (i in 1..list.length()) {
                val e = list.get(i)
                val id = e.get("id").tojstring()
                val d = m.get("get_buff_def").call(LuaValue.valueOf(id))
                out.add(Def(id, e.get("job").tojstring(), e.get("name").tojstring(), d.get("kind").optjstring("song"),
                    d.get("plus_max").optint(0), d.get("optimal_job").optjstring(""), d.get("notes").optjstring("")))
            }
            defs = out
            // _FOOD_STATS is local to the file; its ids are read from the table's source lines and
            // kept only where food_entry() agrees the sim knows them.
            val block = src.substringAfter("local _FOOD_STATS = {", "").substringBefore("\n}")
            foods = Regex("""\[(\d+)]\s*=\s*\{""").findAll(block).map { it.groupValues[1].toInt() }
                .filter { !m.get("food_entry").call(LuaValue.valueOf(it)).isnil() }.distinct().toList()
        }

        fun def(id: String): Def? = defs.firstOrNull { it.id == id }

        /**
         * What [active] and [food] add, under OmniWatch's stat keys ("magic haste", "accuracy",
         * "attack pct", "store tp"...). [base] holds the stats before food, for the foods that
         * give a percent of a stat up to a cap.
         */
        @Synchronized
        fun compute(active: List<Active>, food: Int?, base: Map<String, Double>): Map<String, Double> {
            val set = m.get("set_value")
            fun call(k: String, v: String) { set.call(LuaValue.valueOf(k), LuaValue.valueOf(v)) }
            set.call(LuaValue.valueOf("reset"))
            var n = 0
            for (a in active) {
                if (def(a.id) == null) continue
                call("buff_add", a.id); n++
                call("buff_update", "$n:plus:${a.plus}")
                call("buff_update", "$n:level:${a.level}")
                call("buff_update", "$n:optimal:${a.optimal}")
                call("buff_update", "$n:boost_sv:${a.sv}")
                call("buff_update", "$n:boost_marcato:${a.marcato}")
                call("buff_update", "$n:boost_cc:${a.cc}")
                call("buff_update", "$n:boost_bolster:${a.bolster}")
            }
            call("food", (food ?: 0).toString())
            val out = HashMap<String, Double>()
            fun take(t: LuaValue) {
                if (!t.istable()) return
                var k = LuaValue.NIL
                while (true) {
                    val nx = t.next(k)
                    k = nx.arg1()
                    if (k.isnil()) break
                    val v = nx.arg(2)
                    if (v.isnumber()) out[k.tojstring()] = (out[k.tojstring()] ?: 0.0) + v.todouble()
                }
            }
            take(m.get("compute_active_buff_stats").call())
            val bt = LuaTable()
            base.forEach { (k, v) -> bt.set(k, LuaValue.valueOf(v)) }
            take(m.get("get_food_stats").call(bt))
            return out
        }
    }

    /** Which boosts a buff can take: Soul Voice and Marcato for songs, Crooked Cards for rolls,
     *  Bolster / Blaze of Glory for Geomancy. */
    fun boosts(d: Def): List<String> = when {
        d.kind == "roll" -> listOf("cc")
        d.kind == "song" && d.job == "BRD" -> listOf("sv", "marcato")
        d.kind == "song" && d.job == "GEO" -> listOf("bolster")
        else -> emptyList()
    }

    fun boostLabel(k: String) = when (k) {
        "sv" -> "Soul Voice"; "marcato" -> "Marcato"; "cc" -> "Crooked Cards"; "bolster" -> "Bolster"; else -> k
    }

    // ---- saved picks ------------------------------------------------------------------------
    fun encode(list: List<Active>): String = list.joinToString("\n") {
        listOf(it.id, it.plus, it.level, it.optimal, it.sv, it.marcato, it.cc, it.bolster).joinToString("|")
    }

    fun decode(s: String?): List<Active> = (s ?: "").split('\n').mapNotNull { line ->
        val f = line.split('|')
        if (f.size < 8 || f[0].isBlank()) null else runCatching {
            Active(f[0], f[1].toInt(), f[2].toInt(), f[3].toBoolean(), f[4].toBoolean(), f[5].toBoolean(),
                f[6].toBoolean(), f[7].toBoolean())
        }.getOrNull()
    }
}
