package com.balladofworms.mobilewatch

/** All 16 live worlds and their search-server addresses (124.150.154.61-.76). */
object Worlds {
    val map: LinkedHashMap<String, String> = linkedMapOf(
        "Asura" to "124.150.154.76",
        "Bahamut" to "124.150.154.61",
        "Bismarck" to "124.150.154.74",
        "Carbuncle" to "124.150.154.64",
        "Cerberus" to "124.150.154.73",
        "Fenrir" to "124.150.154.65",
        "Lakshmi" to "124.150.154.75",
        "Leviathan" to "124.150.154.68",
        "Odin" to "124.150.154.69",
        "Phoenix" to "124.150.154.63",
        "Quetzalcoatl" to "124.150.154.70",
        "Ragnarok" to "124.150.154.72",
        "Shiva" to "124.150.154.62",
        "Siren" to "124.150.154.71",
        "Sylph" to "124.150.154.66",
        "Valefor" to "124.150.154.67",
    )
    val names: List<String> = map.keys.toList()
    fun ip(world: String): String? = map[world]
}
