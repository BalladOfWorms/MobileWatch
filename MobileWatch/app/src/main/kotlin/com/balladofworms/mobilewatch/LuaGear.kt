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
 * Reads the gear sets out of GearSwap job files on the phone, with no PC involved.
 *
 * The files are run by LuaJ inside assets/gearswap_sandbox.lua, which stands in for GearSwap
 * (set_combine, gear.*, `empty`, state/M{...} stubs) and walks the finished `sets` table. Only
 * the base, table, string, math and bit32 libraries are loaded: a gear file gets no io, os or
 * Java access.
 */
object LuaGear {
    /** One piece a set names. bag is the set's own bag= ("wardrobe3"), when it gives one. */
    data class SetRef(val name: String, val bag: String, val augs: List<String>)

    /** A set: its path ("sets.midcast.Cure") and slot -> piece, with null where it empties the slot. */
    data class GearSet(val path: String, val slots: Map<String, SetRef?>)

    class Result(val sets: List<GearSet>, val warnings: List<String>)

    /**
     * Run [files] (name to source, shared files first) as [main]/[sub] at [level], returning every
     * set that names at least one piece of gear. Never throws: a file that won't load becomes a
     * warning, and whatever sets did build are still returned.
     */
    fun run(sandbox: String, files: List<Pair<String, String>>, main: String, sub: String, level: Int): Result {
        val text = try {
            val g = Globals()
            g.load(BaseLib()); g.load(PackageLib()); g.load(Bit32Lib())
            g.load(TableLib()); g.load(StringLib()); g.load(MathLib())
            LoadState.install(g)
            LuaC.install(g)
            val arr = LuaTable()
            files.forEachIndexed { i, (name, src) ->
                val t = LuaTable()
                t.set("name", name)
                t.set("src", src)
                arr.set(i + 1, t)
            }
            g.set("__files", arr)
            g.set("__main", LuaValue.valueOf(main))
            g.set("__sub", LuaValue.valueOf(sub))
            g.set("__level", LuaValue.valueOf(level))
            g.load(sandbox, "=gearswap_sandbox").call().tojstring()
        } catch (e: Throwable) {
            return Result(emptyList(), listOf(e.message ?: e.toString()))
        }
        return parse(text)
    }

    fun parse(text: String): Result {
        val sets = ArrayList<GearSet>()
        val warns = ArrayList<String>()
        var path: String? = null
        var slots = LinkedHashMap<String, SetRef?>()
        fun flush() { path?.let { sets.add(GearSet(it, slots)) }; path = null; slots = LinkedHashMap() }
        for (line in text.split('\n')) {
            val f = line.split('\t')
            when (f[0]) {
                "S" -> { flush(); path = f.getOrNull(1) }
                "I" -> if (f.size >= 3) slots[f[1]] = SetRef(
                    name = f[2],
                    bag = f.getOrNull(3) ?: "",
                    augs = f.getOrNull(4)?.split('\u001f')?.filter { it.isNotBlank() } ?: emptyList())
                "E" -> if (f.size >= 2) slots[f[1]] = null
                "W" -> f.getOrNull(1)?.let { warns.add(it) }
            }
        }
        flush()
        return Result(sets, warns)
    }

    /** "Wormfood_Whm_Gear.lua" -> "WHM"; "Wormfood-Globals.lua" -> null (shared by every job). */
    fun jobOf(fileName: String): String? =
        fileName.substringBeforeLast('.').split(Regex("[^A-Za-z]+"))
            .map { it.uppercase() }.firstOrNull { it in GearSlots.JOB_ORDER }
}
