package com.balladofworms.mobilewatch

import android.content.Context
import org.json.JSONObject

data class RecipeYield(val name: String, val qty: Int)
data class RecipeIngredient(val name: String, val qty: Int)
data class Recipe(
    val id: Int,
    val name: String,
    val nqQty: Int,
    val hq: List<RecipeYield>,
    val level: Int,
    val levelText: String,
    val rank: String,
    val crystal: String,
    val sub: String,
    val keyItem: String,
    val ingredients: List<RecipeIngredient>,
)

class RecipeDb(private val map: Map<String, List<Recipe>>) {

    fun recipesFor(craft: String): List<Recipe> = map[craft] ?: emptyList()

    companion object {
        fun load(context: Context): RecipeDb {
            val out = HashMap<String, List<Recipe>>()
            runCatching {
                val text = context.assets.open("recipes.json").bufferedReader(Charsets.UTF_8).use { it.readText() }
                val crafts = JSONObject(text).getJSONObject("crafts")
                for (key in crafts.keys()) {
                    val arr = crafts.getJSONObject(key).getJSONArray("recipes")
                    val list = ArrayList<Recipe>()
                    for (i in 0 until arr.length()) {
                        val o = arr.getJSONObject(i)
                        val hArr = o.optJSONArray("hq")
                        val hq = if (hArr != null) (0 until hArr.length()).map {
                            val h = hArr.getJSONObject(it)
                            RecipeYield(h.optString("n"), h.optInt("x", 1))
                        } else emptyList()
                        val iArr = o.optJSONArray("ing")
                        val ings = if (iArr != null) (0 until iArr.length()).map {
                            val g = iArr.getJSONObject(it)
                            RecipeIngredient(g.optString("n"), g.optInt("x", 1))
                        } else emptyList()
                        list.add(
                            Recipe(
                                i, o.optString("nq"), o.optInt("nqx", 1), hq,
                                o.optInt("lv", 0), o.optString("lvx"), o.optString("rank"),
                                o.optString("crystal"), o.optString("sub"), o.optString("ki"), ings
                            )
                        )
                    }
                    out[key] = list.sortedWith(compareBy({ it.level }, { it.name }))
                }
            }
            return RecipeDb(out)
        }
    }
}
