package com.balladofworms.mobilewatch

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.net.Uri
import android.provider.DocumentsContract
import java.io.File

/**
 * The GearSwap job files the Character tab reads its sets from.
 *
 * You pick a folder on the phone once (Settings > Gear luas), then tick the files to use. Ticked
 * files are copied into the app's own storage, so the tab works offline and with the folder gone;
 * whenever the folder is still reachable the copies are refreshed from it, so editing a lua and
 * copying it back to the phone is all it takes.
 *
 * A file whose name carries a job ("Wormfood_Whm_Gear.lua", "WHM.lua") belongs to that job. One
 * with no job in its name ("Wormfood-Globals.lua", "Mytha-Items.lua") is shared and is loaded
 * ahead of every job's files, which is where gear.* helpers usually live.
 */
object GearLuas {
    private const val P_TREE = "luas_tree"
    private const val P_SELECTED = "luas_selected"

    data class Entry(val name: String, val docId: String)

    private fun dir(ctx: Context) = File(ctx.filesDir, "luas").apply { mkdirs() }

    fun folder(prefs: SharedPreferences): Uri? = prefs.getString(P_TREE, null)?.let { Uri.parse(it) }

    /** A human name for the chosen folder ("FFXI/Gearswap/luas"). */
    fun folderLabel(prefs: SharedPreferences): String? = folder(prefs)?.let { uri ->
        runCatching { DocumentsContract.getTreeDocumentId(uri).substringAfter(':').ifBlank { "/" } }.getOrNull()
    }

    fun setFolder(ctx: Context, prefs: SharedPreferences, uri: Uri) {
        runCatching {
            ctx.contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        prefs.edit().putString(P_TREE, uri.toString()).apply()
    }

    fun selected(prefs: SharedPreferences): Set<String> =
        prefs.getString(P_SELECTED, "")!!.split('\n').filter { it.isNotBlank() }.toSet()

    private fun saveSelected(prefs: SharedPreferences, names: Set<String>) {
        prefs.edit().putString(P_SELECTED, names.sorted().joinToString("\n")).apply()
    }

    /** The .lua files in the chosen folder, or null when it can't be read (moved, permission gone). */
    fun list(ctx: Context, prefs: SharedPreferences): List<Entry>? {
        val tree = folder(prefs) ?: return null
        return runCatching {
            val children = DocumentsContract.buildChildDocumentsUriUsingTree(tree, DocumentsContract.getTreeDocumentId(tree))
            val out = ArrayList<Entry>()
            ctx.contentResolver.query(children, arrayOf(
                DocumentsContract.Document.COLUMN_DOCUMENT_ID,
                DocumentsContract.Document.COLUMN_DISPLAY_NAME), null, null, null)?.use { c ->
                while (c.moveToNext()) {
                    val id = c.getString(0) ?: continue
                    val name = c.getString(1) ?: continue
                    if (name.endsWith(".lua", ignoreCase = true)) out.add(Entry(name, id))
                }
            }
            out.sortedBy { it.name.lowercase() }
        }.getOrNull()
    }

    /** Tick or untick one file. Ticking copies it in now; unticking deletes the saved copy. */
    fun setUsed(ctx: Context, prefs: SharedPreferences, name: String, used: Boolean) {
        val sel = selected(prefs).toMutableSet()
        if (used) sel.add(name) else { sel.remove(name); File(dir(ctx), name).delete() }
        saveSelected(prefs, sel)
        if (used) sync(ctx, prefs)
    }

    /**
     * Refresh the saved copies from the folder, when it can be reached. Returns true when any file
     * changed, so the sets get read again. With the folder unreachable the saved copies are used
     * as they are.
     */
    fun sync(ctx: Context, prefs: SharedPreferences): Boolean {
        val tree = folder(prefs) ?: return false
        val entries = list(ctx, prefs) ?: return false
        val sel = selected(prefs)
        var changed = false
        for (e in entries) {
            if (e.name !in sel) continue
            val text = runCatching {
                val uri = DocumentsContract.buildDocumentUriUsingTree(tree, e.docId)
                ctx.contentResolver.openInputStream(uri)?.use { it.readBytes().toString(Charsets.UTF_8) }
            }.getOrNull() ?: continue
            val f = File(dir(ctx), e.name)
            if (!f.isFile || f.readText() != text) { f.writeText(text); changed = true }
        }
        return changed
    }

    /** The saved files in use, as (name, source). */
    fun saved(ctx: Context, prefs: SharedPreferences): List<Pair<String, String>> {
        val sel = selected(prefs)
        return dir(ctx).listFiles()?.filter { it.isFile && it.name in sel }
            ?.sortedBy { it.name.lowercase() }
            ?.mapNotNull { f -> runCatching { f.name to f.readText() }.getOrNull() } ?: emptyList()
    }

    /** Jobs that have at least one file of their own. */
    fun jobs(files: List<Pair<String, String>>): Set<String> = files.mapNotNull { LuaGear.jobOf(it.first) }.toSet()

    /**
     * The files to run for one job, in load order: every shared file, then the job's own, with
     * gear files last (Selindrile loads the job file, the globals, then the gear file).
     */
    fun forJob(files: List<Pair<String, String>>, job: String): List<Pair<String, String>> {
        val shared = files.filter { LuaGear.jobOf(it.first) == null }
        val own = files.filter { LuaGear.jobOf(it.first) == job }
            .sortedBy { if (it.first.contains("gear", ignoreCase = true)) 1 else 0 }
        return if (own.isEmpty()) emptyList() else shared + own
    }
}
