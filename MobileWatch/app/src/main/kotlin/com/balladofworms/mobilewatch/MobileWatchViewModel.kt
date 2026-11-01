package com.balladofworms.mobilewatch

import android.app.Application
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/** The Trusts tab's ticks, under the same key as OmniWatch's checklist category. */
private const val TRUSTS = "trusts"

data class SaleRow(
    val price: Int, val date: Long, val seller: String, val buyer: String, val stack: Boolean
)

data class UiState(
    val ready: Boolean = false,
    val mode: String = "character",       // the tab: character | chat | items | mobs ...
    val query: String = "",
    val results: List<Item> = emptyList(),
    val mobResults: List<Mob> = emptyList(),
    val selectedMob: Mob? = null,
    val selectedSubtype: SubType? = null,
    val mobLevelCtx: String = "",
    val mobView: String = "all",
    val zoneView: String = "all",
    val mobFilter: String = "all",
    val zoneFilter: String = "all",
    val zoneResults: List<Zone> = emptyList(),
    val selectedZone: Zone? = null,
    val showMap: Boolean = false,
    val scChain: List<WeaponSkill> = emptyList(),
    val showSettings: Boolean = false,
    val showMusic: Boolean = false,            // the music player screen (header note button)
    val selectedJob: Job? = null,
    val selectedHobby: String? = null,
    val selectedContent: String? = null,       // Content tab: which content type (e.g. "dynamis")
    val selectedContentZone: String? = null,   // Content tab: which zone page inside it
    val selectedTrust: String? = null,         // Trusts tab: which alter ego's page is open
    val selectedQuestArea: String? = null,     // Quests tab: which log area is open
    val selectedMissionCat: String? = null,    // Missions tab: which mission line is open
    val showWsList: Boolean = false,           // Chains tab: the full weapon-skill reference page
    val selectedFish: Fish? = null,
    val selectedRecipe: Recipe? = null,
    val selectedDigZone: DigZone? = null,
    val selectedPlanting: GardenPlanting? = null,
    val selectedHarvestZone: HarvestZone? = null,
    val selectedMineZone: MiningZone? = null,
    val selectedExcZone: ExcavationZone? = null,
    val selectedLogZone: LoggingZone? = null,
    val showHobbyInfo: Boolean = false,
    val selectedSpell: String? = null,
    val selectedPet: Pet? = null,
    val diLoading: Boolean = false,
    val di: DomainInvasion.DiInfo? = null,
    val diError: Boolean = false,
    val nmLoading: Boolean = false,
    val nm: List<WhereIsNm.NmEntry> = emptyList(),
    val nmError: Boolean = false,
    val seLoading: Boolean = false,
    val se: List<SeEvents.Event> = emptyList(),
    val seError: Boolean = false,
    val world: String = "Phoenix",
    val population: String = "\u2014",
    val selected: Item? = null,
    val historyLoading: Boolean = false,
    val history: List<SaleRow> = emptyList(),
    val onsaleSingle: Int? = null,
    val onsaleStack: Int? = null,
    val filter: String = "all",            // all | single | stack
    val crossLoading: Boolean = false,
    val crossRanking: List<Pair<String, Int>> = emptyList(), // world -> median, cheapest first
    val crossForm: String = "single",   // which form the ranking represents
    val historyNote: String? = null,
)

private const val QUEST_TICKS_KEY = "quest_ticks"

/** The Character tab: gear sets from your GearSwap luas, and your bags from OmniWatch. */
data class CharState(
    val linked: Boolean = false,              // an OmniWatch address + code are saved
    val address: String = "",
    val characters: List<String> = emptyList(),
    val selected: String? = null,             // whose bags are showing
    val snap: GearSnapshot? = null,           // last bags/levels from OmniWatch (null = never linked)
    val job: String? = null,                  // the main job picked in the top row
    val subs: Map<String, String> = emptyMap(),   // main job -> sub job picked in the second row
    val chosen: Map<String, String> = emptyMap(), // main job -> gear set path picked
    val chosenWeapons: Map<String, String> = emptyMap(), // main job -> weapon set path ("" = none)
    val slot: String? = null,                 // a slot's list page is open
    val setList: String? = null,              // a set list page is open: "gear" or "weapons"
    // Pieces picked on the phone, per main job then slot, on top of the chosen set.
    val picks: Map<String, Map<String, OwnedItem>> = emptyMap(),
    val luaNames: List<String> = emptyList(), // the lua files in use
    val setsVersion: Int = 0,                 // bumps when a job's sets have been (re)read
    val setsLoading: Boolean = false,
    val loading: Boolean = false,
    val offline: Boolean = false,             // PC not reachable: showing the saved bags
    val error: String? = null,                // the last OmniWatch connect/refresh problem, in words
    val pinned: Map<String, PinnedStats> = emptyMap(),   // main job -> stats held for Compare
    val buffs: List<SimBuffs.Active> = emptyList(),      // buffs up, from OmniWatch's sim (all jobs)
    val food: Int? = null,                               // food item id, from the sim's food list
    val simReady: Boolean = false,                       // the sim file has been read
)

/** What Compare holds: the stats panel, and which item sat in each slot, when it was pressed. */
data class PinnedStats(val grid: StatsModel.Values, val pet: Map<String, Int>, val items: Map<String, Int>,
                       val label: String)

/** The Chat tab: lines since OmniWatch started, per channel, and the send box. */
data class ChatState(
    val tab: String = "tell",                 // tell | shout | yell | ls1 | ls2
    val lines: List<ChatLine> = emptyList(),
    val seen: Map<String, Int> = emptyMap(),  // channel -> last line read
    val boot: Long = 0,                       // which OmniWatch run the lines came from
    val seq: Int = 0,
    val reachable: Boolean = true,
    val error: String? = null,
    val tellTo: String = "",
    val sending: Boolean = false,
    val sendError: String? = null,
    val blocked: Set<String> = emptySet(),    // lowercase names whose lines are hidden
)

/** What a set puts in one slot, matched to your bags. owned is null when you don't have it
 *  (or OmniWatch has never sent your bags); empty means the set clears the slot. */
data class Piece(val name: String, val item: Item?, val owned: OwnedItem?, val empty: Boolean,
                 val luaAugs: List<String> = emptyList()) {
    /** The augments this piece's stats are read with: your copy's, else the ones the lua names. */
    val augs: List<String> get() = owned?.augs ?: luaAugs
}

/** One row on a slot's page: an owned copy, its item record, and how it relates to the grid. */
data class OwnedRow(
    val owned: OwnedItem, val item: Item, val levelOk: Boolean, val equippable: Boolean,
    val inSet: Boolean,            // the chosen set's piece for this slot
    val selected: Boolean,         // what the grid shows in this slot (a pick, else the set's piece)
    val elsewhere: String?,        // the other slot this copy fills in the grid (rings, earrings), if any
)

/** One row in a slot's "all gear" list: an item the job can wear there that isn't in your bags. */
data class CatalogRow(
    val item: Item, val levelOk: Boolean,
    val inSet: Boolean,            // the chosen set names this item and you don't have it
    val selected: Boolean,         // what the grid shows in this slot
)

/** A pick of an item you don't own rides in the picks map with this bag, so the grid can show
 *  any gear, not only your own. */
const val NOT_OWNED_BAG = -1

private val CHAT_NAME = Regex("^(?:\\[\\d\\])?<([A-Za-z]{2,15})>|^([A-Za-z]{3,15})(?:\\[[^\\]]{1,30}\\])?\\s?:|^([A-Za-z]{3,15})>>")

class MobileWatchViewModel(app: Application) : AndroidViewModel(app) {

    var ui by mutableStateOf(UiState())
        private set

    var char by mutableStateOf(CharState())
        private set

    private val prefs = app.getSharedPreferences("mobilewatch", android.content.Context.MODE_PRIVATE)

    var chat by mutableStateOf(ChatState(blocked = loadBlocked()))
        private set


    private var itemDb: ItemDb? = null
    private var mobDb: MobDb? = null
    private var zoneInfoDb: ZoneInfoDb? = null
    private var zoneDb: ZoneDb? = null
    private var scDb: SkillchainDb? = null
    private var jobDb: JobDb? = null
    private var fishDb: FishDb? = null
    private var hobbyInfoDb: HobbyInfoDb? = null
    private var recipeDb: RecipeDb? = null
    private var diggingDb: DiggingDb? = null
    private var gardeningDb: GardeningDb? = null
    private var harvestingDb: HarvestingDb? = null
    private var miningDb: MiningDb? = null
    private var excavationDb: ExcavationDb? = null
    private var loggingDb: LoggingDb? = null
    private var trustDb: TrustDb? = null
    private var wsListDb: WsListDb? = null
    private var questDb: QuestDb? = null
    private val crossCache = HashMap<Int, HashMap<String, List<Pair<String, Int>>>>()
    private var popToken = 0
    private var histToken = 0
    private var crossToken = 0

    private var simEngine: SimBuffs.Engine? = null

    init {
        char = char.copy(buffs = SimBuffs.decode(prefs.getString("sim_buffs", null)),
            food = prefs.getInt("sim_food", 0).takeIf { it > 0 })
        viewModelScope.launch {
            GearStats.enhanced = withContext(Dispatchers.IO) {
                runCatching {
                    val o = org.json.JSONObject(getApplication<Application>().assets.open("item_enhanced.json")
                        .bufferedReader().use { it.readText() })
                    o.keys().asSequence().mapNotNull { k -> k.toIntOrNull()?.let { it to o.optString(k) } }.toMap()
                }.getOrDefault(emptyMap())
            }
            simEngine = withContext(Dispatchers.Default) {
                runCatching {
                    SimBuffs.Engine(getApplication<Application>().assets.open("omniwatch_sim.lua")
                        .bufferedReader().use { it.readText() })
                }.getOrNull()
            }
            char = char.copy(simReady = simEngine != null)
        }
        ui = ui.copy(
            world = prefs.getString("world", "Phoenix") ?: "Phoenix",
            mobView = prefs.getString("defMobView", "all") ?: "all",
            zoneView = prefs.getString("defZoneView", "all") ?: "all"
        )
        viewModelScope.launch {
            val app = getApplication<Application>()
            val items = withContext(Dispatchers.IO) { ItemDb.load(app) }
            val mobs = withContext(Dispatchers.IO) { runCatching { MobDb.load(app) }.getOrNull() }
            val zinfo = withContext(Dispatchers.IO) { runCatching { ZoneInfoDb.load(app) }.getOrNull() }
            val zones = withContext(Dispatchers.IO) { runCatching { ZoneDb.load(app) }.getOrNull() }
            val scs = withContext(Dispatchers.IO) { runCatching { SkillchainDb.load(app) }.getOrNull() }
            val jobs = withContext(Dispatchers.IO) { runCatching { JobDb.load(app) }.getOrNull() }
            fishDb = withContext(Dispatchers.IO) { runCatching { FishDb.load(app) }.getOrNull() }
            hobbyInfoDb = withContext(Dispatchers.IO) { runCatching { HobbyInfoDb.load(app) }.getOrNull() }
            recipeDb = withContext(Dispatchers.IO) { runCatching { RecipeDb.load(app) }.getOrNull() }
            diggingDb = withContext(Dispatchers.IO) { runCatching { DiggingDb.load(app) }.getOrNull() }
            gardeningDb = withContext(Dispatchers.IO) { runCatching { GardeningDb.load(app) }.getOrNull() }
            harvestingDb = withContext(Dispatchers.IO) { runCatching { HarvestingDb.load(app) }.getOrNull() }
            miningDb = withContext(Dispatchers.IO) { runCatching { MiningDb.load(app) }.getOrNull() }
            excavationDb = withContext(Dispatchers.IO) { runCatching { ExcavationDb.load(app) }.getOrNull() }
            loggingDb = withContext(Dispatchers.IO) { runCatching { LoggingDb.load(app) }.getOrNull() }
            trustDb = withContext(Dispatchers.IO) { runCatching { TrustDb.load(app) }.getOrNull() }
            wsListDb = withContext(Dispatchers.IO) { runCatching { WsListDb.load(app) }.getOrNull() }
            questDb = withContext(Dispatchers.IO) { runCatching { QuestDb.load(app) }.getOrNull() }
            migrateQuestTicks()
            loadSavedCharacter()
            itemDb = items
            mobDb = mobs
            zoneInfoDb = zinfo
            zoneDb = zones
            scDb = scs
            jobDb = jobs
            ui = ui.copy(ready = true)
            refreshPopulation()
            if (ui.mode == "character") refreshCharacter()
        }
    }

    private fun host(): String? = Worlds.ip(ui.world)

    /** Results-list label with the REMA level/DMG suffix (raw name elsewhere). */
    fun label(item: Item): String = itemDb?.label(item) ?: item.name
    fun itemById(id: Int): Item? = itemDb?.get(id)

    fun onQueryChange(q: String) {
        ui = when (ui.mode) {
            "mobs" -> ui.copy(query = q, mobResults = if (q.isBlank()) mobDb?.all() ?: emptyList() else mobDb?.search(q) ?: emptyList())
            "maps" -> ui.copy(query = q, zoneResults = if (q.isBlank()) zoneDb?.all() ?: emptyList() else zoneDb?.search(q) ?: emptyList())
            else -> ui.copy(query = q, results = if (q.isBlank()) itemDb?.all() ?: emptyList() else itemDb?.search(q) ?: emptyList())
        }
    }

    fun jobs(): List<Job> = jobDb?.jobs ?: emptyList()
    fun selectJob(job: Job) { ui = ui.copy(selectedJob = job) }
    fun fishList(): List<Fish> = fishDb?.fish ?: emptyList()
    fun selectHobby(k: String) { ui = ui.copy(selectedHobby = k, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false) }
    fun clearHobby() { ui = ui.copy(selectedHobby = null, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false) }
    fun selectFish(f: Fish) { ui = ui.copy(selectedFish = f) }
    fun clearFish() { ui = ui.copy(selectedFish = null) }
    fun hobbyInfo(k: String): HobbyInfo? = hobbyInfoDb?.infoFor(k)
    fun recipeList(craft: String): List<Recipe> = recipeDb?.recipesFor(craft) ?: emptyList()
    fun selectRecipe(r: Recipe) { ui = ui.copy(selectedRecipe = r) }
    fun clearRecipe() { ui = ui.copy(selectedRecipe = null) }
    fun digZones(): List<DigZone> = diggingDb?.zones ?: emptyList()
    fun selectDigZone(z: DigZone) { ui = ui.copy(selectedDigZone = z) }
    fun clearDigZone() { ui = ui.copy(selectedDigZone = null) }
    fun gardening(): GardeningDb? = gardeningDb
    fun plantings(): List<GardenPlanting> = gardeningDb?.plantings ?: emptyList()
    fun selectPlanting(p: GardenPlanting) { ui = ui.copy(selectedPlanting = p) }
    fun clearPlanting() { ui = ui.copy(selectedPlanting = null) }
    fun harvestZones(): List<HarvestZone> = harvestingDb?.zones ?: emptyList()
    fun selectHarvestZone(z: HarvestZone) { ui = ui.copy(selectedHarvestZone = z) }
    fun clearHarvestZone() { ui = ui.copy(selectedHarvestZone = null) }
    fun mineZones(): List<MiningZone> = miningDb?.zones ?: emptyList()
    fun selectMineZone(z: MiningZone) { ui = ui.copy(selectedMineZone = z) }
    fun clearMineZone() { ui = ui.copy(selectedMineZone = null) }
    fun excZones(): List<ExcavationZone> = excavationDb?.zones ?: emptyList()
    fun selectExcZone(z: ExcavationZone) { ui = ui.copy(selectedExcZone = z) }
    fun clearExcZone() { ui = ui.copy(selectedExcZone = null) }
    fun logZones(): List<LoggingZone> = loggingDb?.zones ?: emptyList()
    fun selectLogZone(z: LoggingZone) { ui = ui.copy(selectedLogZone = z) }
    fun clearLogZone() { ui = ui.copy(selectedLogZone = null) }
    fun openHobbyInfo() { ui = ui.copy(showHobbyInfo = true) }
    fun closeHobbyInfo() { ui = ui.copy(showHobbyInfo = false) }
    fun jobAbilities(id: Int): List<JobAbility> = jobDb?.abilitiesFor(id) ?: emptyList()
    fun jobTraits(id: Int): List<JobTrait> = jobDb?.traitsFor(id) ?: emptyList()
    fun jobSpells(id: Int): List<JobSpell> = jobDb?.spellsFor(id) ?: emptyList()
    fun jobRolls(id: Int): List<JobAbility> = jobDb?.rollsFor(id) ?: emptyList()
    fun selectSpell(name: String) { ui = ui.copy(selectedSpell = name) }
    fun clearSpell() { ui = ui.copy(selectedSpell = null) }
    fun spellInfo(name: String): SpellInfo? = jobDb?.spellInfoFor(name)
    /** Pets ordered by level cap, lowest first, then by name. Pets with no numeric cap are
     *  NOT sorted at all — they keep their file order and sit at the end. That matters: every
     *  Summoner avatar has a blank cap and the avatar list is in a deliberate order
     *  (Carbuncle, Ifrit, Shiva, ... then the spirits), which an alphabetical fallback would
     *  scramble. */
    fun jobPets(id: Int): List<Pet> {
        val all = jobDb?.petsFor(id) ?: emptyList()
        val (capped, uncapped) = all.partition { it.cap.toIntOrNull() != null }
        return capped.sortedWith(compareBy({ it.cap.toInt() }, { it.name })) + uncapped
    }
    fun selectPet(pet: Pet) { ui = ui.copy(selectedPet = pet) }
    fun clearPet() { ui = ui.copy(selectedPet = null) }

    fun openSettings() { ui = ui.copy(showSettings = true) }
    fun openMusic() { ui = ui.copy(showMusic = true) }

    /** From a tell alert: the Chat tab, on Tell. */
    fun openTells() {
        ui = ui.copy(showSettings = false, showMusic = false)
        setMode("chat")
        selectChatTab("tell")
    }
    fun closeMusic() { ui = ui.copy(showMusic = false) }

    fun closeSettings() { ui = ui.copy(showSettings = false) }

    fun setMode(m: String) {
        if (m == ui.mode) return
        ui = ui.copy(mode = m, query = "",
            results = if (m == "items") itemDb?.all() ?: emptyList() else emptyList(),
            mobResults = if (m == "mobs") mobDb?.all() ?: emptyList() else emptyList(),
            zoneResults = if (m == "maps") zoneDb?.all() ?: emptyList() else emptyList(),
            selected = null, selectedMob = null, selectedSubtype = null, selectedZone = null, selectedJob = null,
            selectedHobby = null, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false,
            selectedContent = null, selectedContentZone = null,
            selectedTrust = null, showWsList = false, selectedQuestArea = null, selectedMissionCat = null)
        char = char.copy(slot = null, setList = null)
        if (m == "character") refreshCharacter()
    }

    // ---- Character tab ------------------------------------------------------
    // Sets come from the GearSwap luas picked in Settings (GearLuas + LuaGear, all on the phone);
    // your bags and job levels come from OmniWatch when it's paired (CharLink). Either works
    // without the other: no OmniWatch, and the sets still show by name; no luas, and the tab
    // says where to add them.
    private var charToken = 0
    private var sandboxSrc: String? = null
    private var longNames: Map<String, Int>? = null
    private val setsCache = HashMap<String, LuaGear.Result>()   // "MAIN/SUB" -> sets
    private var luaFiles: List<Pair<String, String>> = emptyList()

    fun item(id: Int): Item? = itemDb?.get(id)

    /** What is on the phone already: the saved link, the last bags fetched, the saved luas. */
    private suspend fun loadSavedCharacter() {
        val link = CharLink.load(prefs)
        val app = getApplication<Application>()
        val (names, snap) = withContext(Dispatchers.IO) {
            val names = CharLink.cachedCharacters(app)
            val sel = CharLink.savedCharacter(prefs)?.takeIf { it in names } ?: names.firstOrNull()
            names to sel?.let { CharLink.cached(app, it) }
        }
        luaFiles = withContext(Dispatchers.IO) { loadLongNames(); GearLuas.saved(app, prefs) }
        char = char.copy(linked = link != null, address = link?.address ?: "",
            characters = names, selected = snap?.character, snap = snap,
            luaNames = luaFiles.map { it.first })
    }

    // ---- Marketplace -------------------------------------------------------
    // Your auction house sale slots and bazaar, through OmniWatch (its AH window's Sell and Bazaar
    // tabs). Listing, taking back and pricing go to the game; a moment later the phone reads the
    // result back, and OmniWatch's own message for it ("listing single ... at 5,000 gil") shows.
    var market by mutableStateOf<Market?>(null)
        private set
    var marketBusy by mutableStateOf(false)
        private set
    var marketMsg by mutableStateOf<String?>(null)
        private set

    fun loadMarket() {
        val link = CharLink.load(prefs) ?: return
        viewModelScope.launch {
            val m = withContext(Dispatchers.IO) { CharLink.market(link) }
            if (m == null) marketMsg = "Can't reach OmniWatch." else market = m
        }
    }

    /** Auction house history for one item, single or stack, on the world picked at the top:
     *  the last sales (newest first) and how many are up for sale. Asked of the search server
     *  straight from the phone, as the Items tab does; kept for two minutes. null: no answer. */
    data class AhHistory(val sales: List<SaleRow>, val onSale: Int?, val world: String)
    private val ahHistCache = HashMap<Triple<String, Int, Boolean>, Pair<Long, AhHistory>>()

    suspend fun ahHistory(itemId: Int, stack: Boolean): AhHistory? {
        val world = ui.world
        val key = Triple(world, itemId, stack)
        ahHistCache[key]?.let { (t, h) -> if (System.currentTimeMillis() - t < 120_000) return h }
        val h = host() ?: return null
        val got = withContext(Dispatchers.IO) {
            val hist = runCatching { SearchEngine.queryHistory(h, itemId, stack) }.getOrNull()
                ?.takeIf { it.ok } ?: return@withContext null
            val counts = runCatching { SearchEngine.queryCategoryCounts(h, hist.category) }.getOrNull()?.get(itemId)
            AhHistory(hist.sales.map { SaleRow(it.price, it.date, it.seller, it.buyer, stack) }.sortedByDescending { it.date },
                counts?.let { if (stack) it.second else it.first }, world)
        } ?: return null
        ahHistCache[key] = System.currentTimeMillis() to got
        return got
    }

    private fun act(vararg kv: Pair<String, Any>) = org.json.JSONObject().apply { kv.forEach { (k, v) -> put(k, v) } }

    // Buy
    fun searchAh(q: String) = marketDo(act("action" to "search", "q" to q), null)
    fun queueBuy(id: Int, stack: Boolean, qty: Int, start: Long, max: Long, inc: Long) = marketDo(act(
        "action" to "queue_add", "id" to id, "stack" to (if (stack) 1 else 0), "qty" to qty,
        "start" to start, "max" to max, "inc" to inc), "Added to the queue.", 300)
    fun unqueueBuy(index: Int) = marketDo(act("action" to "queue_del", "index" to index), null, 300)
    fun startBuying() = marketDo(act("action" to "buy_start"), "Buying.")
    fun stopBuying() = marketDo(act("action" to "buy_stop"), "Stopped.")
    fun clearMarketLog() = marketDo(act("action" to "log_clear"), null, 300)

    // Delivery box
    fun openBox(which: String) = marketDo(act("action" to "dbox_open", "box" to which), null)
    fun closeBox() {
        val link = CharLink.load(prefs) ?: return
        viewModelScope.launch(Dispatchers.IO) { CharLink.marketAct(link, act("action" to "dbox_close")) }
    }
    fun refreshBox() = marketDo(act("action" to "dbox_refresh"), null)
    fun takeFromBox(slot: Int) = marketDo(act("action" to "dbox_take", "slot" to slot), null)
    fun returnFromBox(slot: Int) = marketDo(act("action" to "dbox_return", "slot" to slot), null)
    fun boxAll() = marketDo(act("action" to "dbox_all"), null)
    fun sendItem(to: String, slot: Int, id: Int, count: Int) = marketDo(act("action" to "dbox_send", "to" to to,
        "mode" to "item", "slot" to slot, "id" to id, "amount" to count), "Sent.")
    fun sendGil(to: String, amount: Long) = marketDo(act("action" to "dbox_send", "to" to to,
        "mode" to "gil", "amount" to amount), "Sent.")

    fun refreshMarket() = marketDo(org.json.JSONObject().put("action", "refresh"), "Up to date.")
    fun sellOnAh(id: Int, single: Boolean, price: Long) = marketDo(org.json.JSONObject()
        .put("action", "sell").put("id", id).put("single", if (single) 1 else 0).put("price", price), null)
    fun takeBackAh(slot: Int) = marketDo(org.json.JSONObject().put("action", "cancel").put("slot", slot), null)
    /** price 0 takes it out of the bazaar. */
    fun setBazaar(id: Int, price: Long) = marketDo(org.json.JSONObject()
        .put("action", "bazaar").put("id", id).put("price", price),
        if (price > 0) "Bazaar price set." else "Taken out of your bazaar.")

    private fun marketDo(body: org.json.JSONObject, done: String?, waitMs: Long = 2500) {
        val link = CharLink.load(prefs) ?: return
        if (marketBusy) return
        marketBusy = true
        marketMsg = null
        viewModelScope.launch {
            try {
                val before = market?.logSeq ?: withContext(Dispatchers.IO) { CharLink.market(link) }?.logSeq ?: 0
                val err = withContext(Dispatchers.IO) { CharLink.marketAct(link, body) }
                if (err != null) { marketMsg = err; return@launch }
                // The game answers in a second or two; then read back what it did.
                kotlinx.coroutines.delay(waitMs)
                val m = withContext(Dispatchers.IO) { CharLink.market(link) }
                if (m == null) { marketMsg = "Can't reach OmniWatch."; return@launch }
                market = m
                val fresh = (m.logSeq - before).coerceIn(0, m.log.size)
                marketMsg = if (fresh > 0) m.log.takeLast(fresh).last() else done
            } finally { marketBusy = false }
        }
    }

    // ---- Sync jobs --------------------------------------------------------
    // OmniWatch walks every job in game (by the Mog House moogle) and saves each
    // one's stats; the phone starts it, follows it every two seconds, and fetches the new
    // numbers when it ends.
    var jobSync by mutableStateOf<JobSync?>(null)
        private set
    var jobSyncError by mutableStateOf<String?>(null)
        private set
    private var jobSyncWatching = false

    fun startJobSync() = jobSyncCall("start")
    fun cancelJobSync() = jobSyncCall("cancel")

    /** Pick up a sync that's already going (Settings opened mid-run). */
    fun checkJobSync() = jobSyncCall(null)

    private fun jobSyncCall(action: String?) {
        val link = CharLink.load(prefs) ?: return
        viewModelScope.launch {
            val r = withContext(Dispatchers.IO) { CharLink.jobSync(link, action) }
            if (r == null) {
                if (action != null) jobSyncError = "Can't reach OmniWatch."
                return@launch
            }
            jobSyncError = null
            jobSync = r
            if (r.busy) watchJobSync()
        }
    }

    private fun watchJobSync() {
        if (jobSyncWatching) return
        val link = CharLink.load(prefs) ?: return
        jobSyncWatching = true
        viewModelScope.launch {
            try {
                while (true) {
                    kotlinx.coroutines.delay(2000)
                    val r = withContext(Dispatchers.IO) { CharLink.jobSync(link, null) } ?: continue
                    jobSync = r
                    if (!r.busy) {
                        if (r.saved.isNotEmpty()) refreshCharacter()
                        break
                    }
                }
            } finally { jobSyncWatching = false }
        }
    }

    /** On opening the tab and from the refresh button: pick up edited luas, then ask OmniWatch
     *  for the latest bags. When the PC can't be reached the saved bags stay and it says so. */
    fun refreshCharacter() {
        reloadLuas(fromFolder = true)
        val link = CharLink.load(prefs) ?: return
        val app = getApplication<Application>()
        val token = ++charToken
        char = char.copy(loading = true, error = null)
        viewModelScope.launch {
            val hello = withContext(Dispatchers.IO) { CharLink.hello(link) }
            if (token != charToken) return@launch
            if (hello.value == null) {
                val names = withContext(Dispatchers.IO) { CharLink.cachedCharacters(app) }
                char = char.copy(loading = false, offline = true,
                    characters = (char.characters + names).distinct().sorted(),
                    error = failText(hello.fail))
                return@launch
            }
            val names = hello.value
            val sel = char.selected?.takeIf { it in names }
                ?: CharLink.savedCharacter(prefs)?.takeIf { it in names }
                ?: names.firstOrNull()
            if (sel == null) {
                char = char.copy(loading = false, offline = false, characters = names,
                    error = "OmniWatch has no gear for any character yet. Log in with OmniWatch running and it will appear.")
                return@launch
            }
            val res = withContext(Dispatchers.IO) { CharLink.fetchGear(app, link, sel) }
            if (token != charToken) return@launch
            val snap = res.value ?: char.snap.takeIf { it?.character == sel }
            char = char.copy(loading = false, offline = res.fail == CharLink.Fail.Unreachable,
                characters = names, selected = sel, snap = snap,
                picks = prunePicks(char.picks, snap),
                error = res.fail?.let { failText(it) })
        }
    }

    private fun failText(f: CharLink.Fail?): String? = when (f) {
        CharLink.Fail.BadCode -> "OmniWatch didn't accept the code. Check it in OmniWatch: Settings, MobileWatch (just above Exit)."
        CharLink.Fail.Unreachable -> "Can't reach OmniWatch, so these are the last bags the phone saw."
        CharLink.Fail.NoSnapshot -> "OmniWatch has no gear for that character yet."
        null -> null
    }

    /** Pair with OmniWatch: the address and code from its MobileWatch box. Saved only once
     *  OmniWatch has answered, so a typo never replaces a link that worked. */
    fun connectCharacter(address: String, code: String) {
        val link = CharLink.Link(CharLink.normalizeAddress(address), CharLink.normalizeCode(code))
        if (link.address.isEmpty() || link.code.length < 8) {
            char = char.copy(error = "Enter the address and the 8-character code that OmniWatch shows.")
            return
        }
        val token = ++charToken
        char = char.copy(loading = true, error = null)
        viewModelScope.launch {
            val hello = withContext(Dispatchers.IO) { CharLink.hello(link) }
            if (token != charToken) return@launch
            when (hello.fail) {
                null -> {
                    CharLink.save(prefs, link)
                    char = char.copy(linked = true, address = link.address, loading = false)
                    refreshCharacter()
                    TellAlerts.stop(getApplication()); TellAlerts.start(getApplication())   // new link
                }
                CharLink.Fail.BadCode -> char = char.copy(loading = false,
                    error = "OmniWatch answered but didn't accept that code.")
                else -> char = char.copy(loading = false,
                    error = "Nothing answered at ${link.address}. Check OmniWatch is running and the phone can reach that PC.")
            }
        }
    }

    /** Forget the OmniWatch link and the saved bags. The luas stay. */
    fun disconnectCharacter() {
        TellAlerts.stop(getApplication())
        CharLink.clear(prefs)
        CharLink.forget(getApplication())
        ++charToken
        char = char.copy(linked = false, address = "", characters = emptyList(), selected = null,
            snap = null, picks = emptyMap(), loading = false, offline = false, error = null)
    }

    fun selectCharacter(name: String) {
        if (name == char.selected) return
        CharLink.saveCharacter(prefs, name)
        val app = getApplication<Application>()
        viewModelScope.launch {
            val snap = withContext(Dispatchers.IO) { CharLink.cached(app, name) }
            char = char.copy(selected = name, snap = snap, slot = null, picks = prunePicks(char.picks, snap))
            refreshCharacter()
        }
    }

    // ---- Chat tab -----------------------------------------------------------------
    private var chatBusy = false

    /** Fetch any lines since the last poll. The tab calls this every couple of seconds while
     *  it's open; a new OmniWatch run (restart) replaces the list. */
    fun pollChat() {
        val link = CharLink.load(prefs) ?: return
        if (chatBusy) return
        chatBusy = true
        viewModelScope.launch {
            val r = withContext(Dispatchers.IO) { CharLink.chat(link, chat.seq, chat.boot) }
            chatBusy = false
            val b = r.value
            if (b == null) {
                chat = chat.copy(reachable = false, error = when (r.fail) {
                    CharLink.Fail.BadCode -> "OmniWatch didn't accept the code. Check it in Settings."
                    else -> "Can't reach OmniWatch. Chat shows once it's running."
                })
                return@launch
            }
            val fresh = b.boot != chat.boot
            val lines = ((if (fresh) emptyList() else chat.lines) + b.lines).takeLast(1500)
            val seen = if (fresh) emptyMap() else chat.seen
            // A tell that arrives with no one in the To box fills it, ready for a reply.
            // OmniWatch's blacklist is the shared one: take it, after sending any change made
            // while the PC couldn't be reached.
            b.blocked?.let { remote ->
                val pend = loadPending()
                val merged = if (pend.isEmpty()) remote else withContext(Dispatchers.IO) {
                    CharLink.setBlocked(link, pend.filterValues { it }.keys, pend.filterValues { !it }.keys)
                }?.also { savePending(emptyMap()) } ?: applyPending(remote, pend)
                if (merged != chat.blocked) saveBlocked(merged)
            }
            val lastFrom = b.lines.lastOrNull { it.ch == "tell" && it.from != null && !isBlocked(it) }?.from
            chat = chat.copy(boot = b.boot, seq = b.seq, lines = lines, seen = markRead(seen, lines, chat.tab),
                reachable = true, error = null,
                tellTo = if (chat.tellTo.isBlank() && lastFrom != null) lastFrom else chat.tellTo)
        }
    }

    private fun markRead(seen: Map<String, Int>, lines: List<ChatLine>, tab: String): Map<String, Int> {
        val top = lines.lastOrNull { it.ch == tab }?.seq ?: return seen
        return seen + (tab to top)
    }

    fun selectChatTab(tab: String) {
        chat = chat.copy(tab = tab, seen = markRead(chat.seen, chat.lines, tab), sendError = null)
    }

    /** Lines on a channel that arrived since it was last looked at (your own don't count). */
    fun chatUnread(ch: String): Int {
        val seen = chat.seen[ch] ?: 0
        return chat.lines.count { it.ch == ch && it.seq > seen && !it.self && !isBlocked(it) }
    }

    // ---- Chat: blocked names --------------------------------------------
    // One list with OmniWatch's chat blacklist: whatever is blocked on either side is blocked on
    // both. A blocked name's lines don't show and don't count toward the badges; your own lines
    // are never hidden. The phone keeps a copy for when the PC can't be reached, and a change made
    // then is sent the next time it can.

    private fun saveBlocked(set: Set<String>) {
        prefs.edit().putString("chat_blocked", set.sorted().joinToString("\n")).apply()
        chat = chat.copy(blocked = set,
            tellTo = if (chat.tellTo.lowercase() in set) "" else chat.tellTo)
    }

    /** Changes not yet sent to OmniWatch: name -> true to block, false to unblock. */
    private fun loadPending(): Map<String, Boolean> =
        prefs.getString("chat_block_pending", "")!!.split('\n').filter { it.length > 1 }
            .associate { it.substring(1) to (it[0] == '+') }

    private fun savePending(m: Map<String, Boolean>) {
        prefs.edit().putString("chat_block_pending",
            m.entries.joinToString("\n") { (if (it.value) "+" else "-") + it.key }).apply()
    }

    private fun applyPending(base: Set<String>, pend: Map<String, Boolean>): Set<String> =
        pend.entries.fold(base) { acc, (n, block) -> if (block) acc + n else acc - n }

    private fun loadBlocked(): Set<String> =
        prefs.getString("chat_blocked", "")!!.split('\n').map { it.trim().lowercase() }.filter { it.isNotEmpty() }.toSet()

    fun blockedNames(): List<String> {
        return chat.blocked.sorted().map { it.replaceFirstChar { c -> c.uppercase() } }
    }

    fun setBlocked(name: String, block: Boolean) {
        val n = name.trim().lowercase()
        if (n.isEmpty()) return
        saveBlocked(if (block) chat.blocked + n else chat.blocked - n)
        savePending(loadPending() + (n to block))
        val link = CharLink.load(prefs) ?: return
        viewModelScope.launch {
            val pend = loadPending()
            val r = withContext(Dispatchers.IO) {
                CharLink.setBlocked(link, pend.filterValues { it }.keys, pend.filterValues { !it }.keys)
            } ?: return@launch          // not reachable: sent with the next chat check
            savePending(emptyMap())
            saveBlocked(r)
        }
    }

    /** Who said a line: the tell's sender, else the name at the front ("<Name>", "Name[Zone]:"). */
    fun chatSender(l: ChatLine): String? {
        if (l.self) return null
        l.from?.let { return it }
        return CHAT_NAME.find(l.text)?.groupValues?.drop(1)?.firstOrNull { it.isNotEmpty() }
    }

    fun isBlocked(l: ChatLine): Boolean {
        if (chat.blocked.isEmpty()) return false
        return chatSender(l)?.lowercase()?.let { it in chat.blocked } == true
    }

    fun setTellTo(name: String) { chat = chat.copy(tellTo = name.filter { it.isLetter() }.take(15)) }

    /** Send on the open channel. Returns true when it went, so the box can clear. */
    fun sendChat(text: String, onSent: () -> Unit) {
        val link = CharLink.load(prefs) ?: return
        val ch = chat.tab
        val to = chat.tellTo
        if (text.isBlank() || chat.sending) return
        if (ch == "tell" && to.length < 3) { chat = chat.copy(sendError = "Who's the tell for?"); return }
        chat = chat.copy(sending = true, sendError = null)
        viewModelScope.launch {
            val err = withContext(Dispatchers.IO) { CharLink.sendChat(link, ch, to, text) }
            chat = chat.copy(sending = false, sendError = err)
            if (err == null) { onSent(); pollChat() }
        }
    }

    // ---- Gear luas (Settings) --------------------------------------------------

    fun luaFolderLabel(): String? = GearLuas.folderLabel(prefs)

    fun setLuaFolder(uri: android.net.Uri) {
        GearLuas.setFolder(getApplication(), prefs, uri)
        char = char.copy(setsVersion = char.setsVersion + 1)
    }

    /** The folder's .lua files, or null when there's no folder or it can't be read. Call off main. */
    fun luaFolderFiles(): List<GearLuas.Entry>? = GearLuas.list(getApplication(), prefs)

    fun luaSelected(): Set<String> = GearLuas.selected(prefs)

    fun setLuaUsed(name: String, used: Boolean) {
        val app = getApplication<Application>()
        viewModelScope.launch {
            withContext(Dispatchers.IO) { GearLuas.setUsed(app, prefs, name, used) }
            reloadLuas(fromFolder = false)
        }
    }

    /** Re-read the saved luas (refreshing them from the folder first when asked) and forget
     *  every job's sets, so they're read again with the new files. */
    fun reloadLuas(fromFolder: Boolean) {
        val app = getApplication<Application>()
        viewModelScope.launch {
            val files = withContext(Dispatchers.IO) {
                if (fromFolder) GearLuas.sync(app, prefs)
                GearLuas.saved(app, prefs)
            }
            if (files != luaFiles) {
                luaFiles = files
                setsCache.clear()
                char = char.copy(luaNames = files.map { it.first }, setsVersion = char.setsVersion + 1)
            }
        }
    }

    // ---- Jobs, sets, grid -------------------------------------------------------

    fun hasLuas(): Boolean = luaFiles.isNotEmpty()

    private fun levels(): Map<String, Int> = char.snap?.jobLevels ?: emptyMap()

    /** The top row: jobs with a level, plus jobs that have a lua, in the game's job order. */
    fun charMainJobs(): List<Pair<String, Int>> {
        val lv = levels()
        val withLua = GearLuas.jobs(luaFiles)
        return GearSlots.JOB_ORDER.filter { (lv[it] ?: 0) > 0 || it in withLua }.map { it to (lv[it] ?: 0) }
    }

    /** The second row: what the main job could have as a support job. */
    fun charSubJobs(main: String): List<Pair<String, Int>> {
        val lv = levels()
        val pool = if (lv.isEmpty()) GearSlots.JOB_ORDER else GearSlots.JOB_ORDER.filter { (lv[it] ?: 0) > 0 }
        return pool.filter { it != main }.map { it to (lv[it] ?: 0) }
    }

    /** The main job showing: the one picked, else the job the character is on, else the first with a lua. */
    fun charJob(): String? = char.job
        ?: char.snap?.mainJob?.ifBlank { null }?.takeIf { j -> charMainJobs().any { it.first == j } }
        ?: charMainJobs().firstOrNull()?.first

    fun charSub(main: String): String = char.subs[main]
        ?: prefs.getString("charsub_$main", null)
        ?: char.snap?.takeIf { it.mainJob == main }?.subJob
        ?: ""

    fun selectCharJob(job: String) { char = char.copy(job = job, slot = null) }

    fun selectCharSub(main: String, sub: String) {
        prefs.edit().putString("charsub_$main", sub).apply()
        char = char.copy(subs = char.subs + (main to sub))
    }

    private val setsInFlight = HashSet<String>()

    /** The sets the job's luas build with its sub job, or null until they've been read
     *  (ensureSets starts that). An empty result means the job has no lua. */
    fun charSets(main: String): LuaGear.Result? {
        val key = "$main/${charSub(main)}"
        setsCache[key]?.let { return it }
        return if (GearLuas.forJob(luaFiles, main).isEmpty()) LuaGear.Result(emptyList(), emptyList()) else null
    }

    /** Read the job's sets (for its current sub job) if they haven't been yet. Runs the luas off
     *  the main thread; the grid redraws when they're in. */
    fun ensureSets(main: String) {
        val sub = charSub(main)
        val key = "$main/$sub"
        if (setsCache.containsKey(key) || key in setsInFlight) return
        val files = GearLuas.forJob(luaFiles, main)
        if (files.isEmpty()) return
        val app = getApplication<Application>()
        val level = levels()[main]?.takeIf { it > 0 } ?: 99
        setsInFlight.add(key)
        char = char.copy(setsLoading = true)
        viewModelScope.launch {
            val res = withContext(Dispatchers.Default) {
                val sb = sandboxSrc ?: app.assets.open("gearswap_sandbox.lua").bufferedReader().use { it.readText() }
                sandboxSrc = sb
                LuaGear.run(sb, files, main, sub, level)
            }
            setsInFlight.remove(key)
            if (files == GearLuas.forJob(luaFiles, main)) setsCache[key] = res
            char = char.copy(setsLoading = setsInFlight.isNotEmpty(), setsVersion = char.setsVersion + 1)
        }
    }

    private fun pathSegments(path: String): List<String> =
        path.removePrefix("sets").split('.', '[').map { it.trim().trimEnd(']').trim('\'', '"') }.filter { it.isNotEmpty() }

    /** Weapon sets are the ones under sets.weapons (Selindrile's state.Weapons sets). */
    fun isWeaponSet(path: String): Boolean = pathSegments(path).firstOrNull().equals("weapons", ignoreCase = true)

    /** "sets.weapons.DualWeapons" -> "DualWeapons". */
    fun shortSetName(path: String): String = pathSegments(path).drop(1).joinToString(".").ifEmpty { path }

    fun gearSets(main: String): List<LuaGear.GearSet> = charSets(main)?.sets?.filterNot { isWeaponSet(it.path) } ?: emptyList()
    fun weaponSets(main: String): List<LuaGear.GearSet> = charSets(main)?.sets?.filter { isWeaponSet(it.path) } ?: emptyList()

    /** The gear set for this job: the one picked, else sets.idle, else the first idle set. */
    fun chosenSetPath(main: String): String? {
        val sets = gearSets(main).ifEmpty { return null }
        val saved = char.chosen[main] ?: prefs.getString("charset_$main", null)
        return sets.firstOrNull { it.path == saved }?.path
            ?: sets.firstOrNull { it.path == "sets.idle" }?.path
            ?: sets.firstOrNull { it.path.contains("idle", ignoreCase = true) }?.path
            ?: sets.firstOrNull()?.path
    }

    /** The weapon set for this job, or null for none (the gear set's own weapons show). */
    fun chosenWeaponPath(main: String): String? {
        val saved = char.chosenWeapons[main] ?: prefs.getString("charweap_$main", null) ?: return null
        return weaponSets(main).firstOrNull { it.path == saved }?.path
    }

    fun openSetList(kind: String) { char = char.copy(setList = kind) }
    fun closeSetList() { char = char.copy(setList = null) }

    /** Picks in the slots a set names are dropped when that set changes; the rest stay. */
    private fun dropPicks(main: String, vararg paths: String?): Map<String, Map<String, OwnedItem>> {
        val all = charSets(main)?.sets ?: emptyList()
        val slots = paths.filterNotNull().flatMap { p -> all.firstOrNull { it.path == p }?.slots?.keys ?: emptySet() }.toSet()
        val left = (char.picks[main] ?: emptyMap()).filterKeys { it !in slots }
        return if (left.isEmpty()) char.picks - main else char.picks + (main to left)
    }

    /** Choose the gear set. The weapon set stays as it is. */
    fun chooseSet(main: String, path: String) {
        val old = chosenSetPath(main)
        prefs.edit().putString("charset_$main", path).apply()
        char = char.copy(chosen = char.chosen + (main to path), picks = dropPicks(main, old, path), setList = null)
    }

    /** Choose the weapon set (null for none). The gear set stays as it is. */
    fun chooseWeapons(main: String, path: String?) {
        val old = chosenWeaponPath(main)
        prefs.edit().putString("charweap_$main", path ?: "").apply()
        char = char.copy(chosenWeapons = char.chosenWeapons + (main to (path ?: "")),
            picks = dropPicks(main, old, path), setList = null)
    }

    /** GearSwap takes an item's long name too ("Mendicant's Earring" for "Mendi. Earring"); the
     *  item data only has the short one, so the long names of equipment ride in their own file. */
    private fun loadLongNames(): Map<String, Int> = longNames ?: runCatching {
        val o = org.json.JSONObject(getApplication<Application>().assets.open("item_longnames.json")
            .bufferedReader().use { it.readText() })
        val m = HashMap<String, Int>()
        o.keys().forEach { k -> m[k] = o.optInt(k) }
        m as Map<String, Int>
    }.getOrDefault(emptyMap()).also { longNames = it }

    private fun itemByName(name: String): Item? {
        val db = itemDb ?: return null
        db.byName(name)?.let { return it }
        return (longNames ?: emptyMap())[name.trim().lowercase()]?.let { db.get(it) }
    }

    private fun augKey(s: String) = s.lowercase().filter { it.isLetterOrDigit() || it == '+' || it == '-' }

    private fun bagIdOf(name: String): Int? = when (name.lowercase().filter { it.isLetterOrDigit() }) {
        "inventory" -> 0; "wardrobe" -> 8; "wardrobe2" -> 10; "wardrobe3" -> 11; "wardrobe4" -> 12
        "wardrobe5" -> 13; "wardrobe6" -> 14; "wardrobe7" -> 15; "wardrobe8" -> 16
        else -> null
    }

    /**
     * Match each piece the set names to a copy in your bags: the set's own bag= first, then the
     * copy whose augments match best (six capes, one name), then any copy, equippable bags first.
     * A copy is used once, so two of the same ring land on two real rings.
     */
    fun resolveSet(set: LuaGear.GearSet): Map<String, Piece> {
        val snap = char.snap
        val db = itemDb
        val byName = HashMap<String, MutableList<OwnedItem>>()
        if (snap != null && db != null) snap.items.forEach { o ->
            db.get(o.id)?.let { byName.getOrPut(it.name.lowercase()) { ArrayList() }.add(o) }
        }
        val used = HashSet<Pair<Int, Int>>()
        val out = LinkedHashMap<String, Piece>()
        // Specific references (a bag, augments) are placed first so a plain reference to the same
        // item can't take the copy they name.
        val order = GearSlots.GRID.map { it.key }.filter { set.slots.containsKey(it) }
            .sortedBy { k -> set.slots[k]?.let { if (it.bag.isNotEmpty() || it.augs.isNotEmpty()) 0 else 1 } ?: 2 }
        for (k in order) {
            val ref = set.slots[k]
            if (ref == null) { out[k] = Piece("", null, null, empty = true); continue }
            val item = itemByName(ref.name)
            val copies = ((byName[ref.name.lowercase()] ?: item?.let { byName[it.name.lowercase()] }) ?: emptyList())
                .filter { (it.bag to it.idx) !in used }
                .sortedBy { if (GearSlots.canEquipFrom(it.bag)) 0 else 1 }
            val bagId = bagIdOf(ref.bag)
            val want = ref.augs.map { augKey(it) }
            fun score(o: OwnedItem): Int {
                val have = o.augs.map { augKey(it) }.toMutableList()
                return want.count { w -> have.remove(w) }
            }
            val owned = copies.firstOrNull { bagId != null && it.bag == bagId }
                ?: if (want.isNotEmpty() && copies.isNotEmpty()) {
                    val scored = copies.map { it to score(it) }.sortedByDescending { it.second }
                    if (scored.size == 1 || scored[0].second > scored[1].second) scored[0].first else copies.first()
                } else copies.firstOrNull()
            owned?.let { used.add(it.bag to it.idx) }
            out[k] = Piece(ref.name, owned?.let { db?.get(it.id) } ?: item, owned, empty = false, luaAugs = ref.augs)
        }
        return out
    }

    /** The gear set with the weapon set on top (weapons win the slots they name), matched to your
     *  bags. Empty while the luas are being read. */
    fun chosenPieces(main: String): Map<String, Piece> {
        val all = charSets(main)?.sets ?: return emptyMap()
        val gear = chosenSetPath(main)?.let { p -> all.firstOrNull { it.path == p } }
        val weap = chosenWeaponPath(main)?.let { p -> all.firstOrNull { it.path == p } }
        if (gear == null && weap == null) return emptyMap()
        val slots = LinkedHashMap<String, LuaGear.SetRef?>()
        gear?.let { slots.putAll(it.slots) }
        weap?.let { slots.putAll(it.slots) }
        return resolveSet(LuaGear.GearSet(gear?.path ?: weap!!.path, slots))
    }

    /** What the grid shows in a slot: a piece picked on the phone, else the chosen set's. */
    fun effectivePiece(main: String, slotKey: String, pieces: Map<String, Piece>): Piece? {
        char.picks[main]?.get(slotKey)?.let { o ->
            return Piece(itemDb?.get(o.id)?.name ?: "", itemDb?.get(o.id), o.takeIf { it.bag != NOT_OWNED_BAG }, false)
        }
        return pieces[slotKey]
    }

    fun isPicked(main: String, slotKey: String): Boolean = char.picks[main]?.containsKey(slotKey) == true
    fun hasPicks(main: String): Boolean = !char.picks[main].isNullOrEmpty()

    fun openCharSlot(slot: String) { char = char.copy(slot = slot) }
    fun closeCharSlot() { char = char.copy(slot = null) }

    /** Choose a piece for the open slot, then go back to the grid with it in place. Choosing
     *  the set's own piece drops the pick. */
    fun pickGear(row: OwnedRow) {
        val job = charJob() ?: return
        val slot = char.slot ?: return
        val forJob = (char.picks[job] ?: emptyMap()).toMutableMap()
        if (row.inSet) forJob.remove(slot) else forJob[slot] = row.owned
        char = char.copy(picks = char.picks + (job to forJob), slot = null)
    }

    fun resetPicks(main: String) { char = char.copy(picks = char.picks - main) }

    /** Drop picks whose copy is gone from new bags (sold, dropped, moved to another bag). */
    private fun prunePicks(picks: Map<String, Map<String, OwnedItem>>, snap: GearSnapshot?): Map<String, Map<String, OwnedItem>> {
        if (snap == null || picks.isEmpty()) return picks
        val have = snap.items.associateBy { it.bag to it.idx }
        return picks.mapValues { (_, slots) ->
            slots.mapNotNull { (k, o) -> if (o.bag == NOT_OWNED_BAG) return@mapNotNull k to o
                have[o.bag to o.idx]?.takeIf { it.id == o.id }?.let { k to it } }.toMap()
        }.filterValues { it.isNotEmpty() }
    }

    /** Everything owned that this job can wear in this slot: what the grid shows first, then the
     *  set's piece, then the highest-level pieces, gear the job is too low for last. */
    fun ownedForSlot(job: String, slotKey: String): List<OwnedRow> {
        val snap = char.snap ?: return emptyList()
        val slot = GearSlots.slot(slotKey) ?: return emptyList()
        val jobBit = GearSlots.jobBit(job)
        if (jobBit < 0) return emptyList()
        val level = snap.jobLevels[job] ?: 0
        val pieces = chosenPieces(job)
        val setCopy = pieces[slotKey]?.owned
        val shown = effectivePiece(job, slotKey, pieces)?.owned
        // Which grid square each copy currently fills, so a ring can't sit on both fingers.
        val placed = HashMap<Pair<Int, Int>, String>()
        GearSlots.GRID.forEach { s -> effectivePiece(job, s.key, pieces)?.owned?.let { placed[it.bag to it.idx] = s.label } }
        return snap.items.mapNotNull { o ->
            val rec = itemDb?.get(o.id) ?: return@mapNotNull null
            if ((rec.slotMask and (1 shl slot.bit)) == 0) return@mapNotNull null
            if ((rec.jobsMask and (1L shl jobBit)) == 0L) return@mapNotNull null
            OwnedRow(o, rec, levelOk = rec.level <= level || level == 0,
                equippable = GearSlots.canEquipFrom(o.bag),
                inSet = setCopy != null && setCopy.bag == o.bag && setCopy.idx == o.idx,
                selected = shown != null && shown.bag == o.bag && shown.idx == o.idx,
                elsewhere = placed[o.bag to o.idx]?.takeIf { it != slot.label })
        }.sortedWith(compareBy<OwnedRow>({ !it.selected }, { !it.inSet }, { !it.levelOk },
            { -maxOf(it.item.ilevel, it.item.level) }, { it.item.name.lowercase() }))
    }

    /** Choose an item you don't own for the open slot. Choosing the set's own piece drops the pick. */
    fun pickCatalog(row: CatalogRow) {
        val job = charJob() ?: return
        val slot = char.slot ?: return
        val forJob = (char.picks[job] ?: emptyMap()).toMutableMap()
        if (row.inSet) forJob.remove(slot) else forJob[slot] = OwnedItem(row.item.id, NOT_OWNED_BAG, 0, emptyList())
        char = char.copy(picks = char.picks + (job to forJob), slot = null)
    }

    private var catalogCache: Pair<String, List<Item>>? = null

    /** Every item this job can wear in this slot, from the item data, less what you already own
     *  (that's listed above it). The set's piece and the grid's piece first, then highest level. */
    fun catalogForSlot(job: String, slotKey: String): List<CatalogRow> {
        val db = itemDb ?: return emptyList()
        val slot = GearSlots.slot(slotKey) ?: return emptyList()
        val jobBit = GearSlots.jobBit(job)
        if (jobBit < 0) return emptyList()
        val key = "$job/$slotKey"
        val fits = catalogCache?.takeIf { it.first == key }?.second ?: db.all().filter { rec ->
            (rec.slotMask and (1 shl slot.bit)) != 0 && (rec.jobsMask and (1L shl jobBit)) != 0L
        }.also { catalogCache = key to it }
        val snap = char.snap
        val ownedIds = snap?.items?.map { it.id }?.toHashSet() ?: emptySet<Int>()
        val level = snap?.jobLevels?.get(job) ?: 0
        val pieces = chosenPieces(job)
        val setId = pieces[slotKey]?.takeIf { !it.empty && it.owned == null }?.item?.id
        val shownId = effectivePiece(job, slotKey, pieces)?.takeIf { !it.empty && it.owned == null }?.item?.id
        return fits.filter { it.id !in ownedIds }.map { rec ->
            CatalogRow(rec, levelOk = level == 0 || rec.level <= level,
                inSet = setId == rec.id, selected = shownId == rec.id)
        }.sortedWith(compareBy<CatalogRow>({ !it.selected }, { !it.inSet },
            { -maxOf(it.item.ilevel, it.item.level) }, { it.item.name.lowercase() }))
    }

    // ---- Character tab: stats --------------------------------------------
    private fun statInputs(main: String, withPicks: Boolean): Map<String, Pair<Item, List<String>>> {
        val pieces = chosenPieces(main)
        val out = HashMap<String, Pair<Item, List<String>>>()
        for (s in GearSlots.GRID) {
            val p = (if (withPicks) effectivePiece(main, s.key, pieces) else pieces[s.key]) ?: continue
            if (p.empty) continue
            val item = p.item ?: continue
            out[s.key] = item to p.augs
        }
        return out
    }

    /** What the grid adds up to. */
    fun gridStats(main: String): GearStats.Totals = GearStats.total(statInputs(main, true))

    /** What the chosen sets add up to before any phone picks: the baseline the panel compares to. */
    fun setStats(main: String): GearStats.Totals = GearStats.total(statInputs(main, false))

    /** The Statistics grid for the job: OmniWatch's panel moved by the phone's gear sums when
     *  OmniWatch has seen the job, else gear only. withPicks=false gives the chosen sets alone. */
    fun gridValues(main: String, withPicks: Boolean): StatsModel.Values {
        val inputs = statInputs(main, withPicks)
        val set = GearStats.total(inputs).stats
        val js = char.snap?.jobStats?.get(main)
        val db = itemDb
        if (js == null || db == null || js.stats.isEmpty()) return withSim(StatsModel.values(set, null, null, false))
        val wornInputs = js.worn.mapNotNull { (slot, o) -> db.get(o.id)?.let { slot to (it to o.augs) } }.toMap()
        val worn = GearStats.total(wornInputs).stats
        val differ = listOf("main", "sub", "range").any { k -> inputs[k]?.first?.id != js.worn[k]?.id }
        return withSim(StatsModel.values(set, js.stats, worn, differ))
    }

    // ---- Character tab: buffs and food (OmniWatch's sim) ---------------------
    private fun withSim(v: StatsModel.Values): StatsModel.Values {
        val e = simEngine ?: return v
        if (char.buffs.isEmpty() && char.food == null) return v
        // Food that gives a percent of a stat needs the stat: only real totals will do.
        val base = if (v.anchored) v.v.mapNotNull { (k, x) -> x?.let { k to it } }.toMap() else emptyMap()
        val add = runCatching { e.compute(char.buffs, char.food, base) }.getOrDefault(emptyMap())
        return StatsModel.withBuffs(v, add)
    }

    fun simDefs(): List<SimBuffs.Def> = simEngine?.defs ?: emptyList()
    fun simDef(id: String): SimBuffs.Def? = simEngine?.def(id)
    fun simFoods(): List<Pair<Int, String>> =
        simEngine?.foods?.map { it to (itemDb?.get(it)?.name ?: "Food $it") } ?: emptyList()
    fun foodName(id: Int): String = itemDb?.get(id)?.name ?: "Food $id"

    private fun saveSim(list: List<SimBuffs.Active>, food: Int?) {
        prefs.edit().putString("sim_buffs", SimBuffs.encode(list)).putInt("sim_food", food ?: 0).apply()
        char = char.copy(buffs = list, food = food)
    }

    fun addBuff(id: String) {
        val d = simDef(id) ?: return
        saveSim(char.buffs + SimBuffs.Active(id, plus = 0, level = if (d.kind == "roll") 11 else 0), char.food)
    }
    fun updateBuff(i: Int, a: SimBuffs.Active) {
        if (i !in char.buffs.indices) return
        saveSim(char.buffs.toMutableList().also { it[i] = a }, char.food)
    }
    fun removeBuff(i: Int) {
        if (i !in char.buffs.indices) return
        saveSim(char.buffs.toMutableList().also { it.removeAt(i) }, char.food)
    }
    fun setFood(id: Int?) = saveSim(char.buffs, id)
    fun clearSim() = saveSim(emptyList(), null)

    /** Compare: hold the grid's stats as they are now. Swaps, picks and set changes after this are
     *  measured against it until it's cleared. */
    fun pinStats(main: String) {
        val inputs = statInputs(main, true)
        val set = chosenSetPath(main)?.removePrefix("sets.") ?: "gear"
        val weap = chosenWeaponPath(main)?.let { shortSetName(it) }
        val label = listOfNotNull(weap, set).joinToString(" + ") + if (hasPicks(main)) " (with swaps)" else ""
        char = char.copy(pinned = char.pinned + (main to PinnedStats(gridValues(main, true),
            GearStats.total(inputs).pet, inputs.mapValues { it.value.first.id }, label)))
    }

    fun unpinStats(main: String) { char = char.copy(pinned = char.pinned - main) }

    /** The item in each grid slot now, for marking what differs from the pinned set. */
    fun gridItemIds(main: String): Map<String, Int> = statInputs(main, true).mapValues { it.value.first.id }

    /** The sub job OmniWatch read the job's numbers with, when they came from OmniWatch. */
    fun statsSub(main: String): String? = char.snap?.jobStats?.get(main)?.sub

    /** The stats of what's in the slot now (null when it's empty), for the slot page's differences. */
    fun slotNowStats(main: String, slotKey: String): GearStats.Parsed? {
        val now = effectivePiece(main, slotKey, chosenPieces(main))?.takeIf { !it.empty } ?: return null
        return now.item?.let { GearStats.of(it, now.augs) }
    }

    fun bagName(bag: Int): String = char.snap?.bags?.get(bag)?.ifBlank { null } ?: "Bag $bag"

    // ---- Trusts tab --------------------------------------------------------
    fun trustRoles(): List<String> = trustDb?.roles ?: emptyList()
    fun trustsOf(role: String): List<Trust> = trustDb?.byRole(role) ?: emptyList()
    fun trust(name: String): Trust? = trustDb?.trust(name)
    fun trustInfo(): List<TrustInfo> = trustDb?.info ?: emptyList()
    /** Total alter egos, shown on the collapsed "Alter Egos" section header. */
    fun trustCount(): Int = trustDb?.trusts?.size ?: 0
    /** Trusts you have: ticked by hand or by a sync with OmniWatch (which reads your spell list). */
    fun trustOwned(t: Trust): Boolean = clDone(TRUSTS, t.name.lowercase())
    fun toggleTrust(t: Trust) = toggleCl(TRUSTS, t.name.lowercase())
    fun trustOwnedCount(): Int {
        val d = clTicks[TRUSTS] ?: return 0
        return trustDb?.trusts?.count { it.name.lowercase() in d } ?: 0
    }
    private fun trustKey(s: String) = s.lowercase().filter { it.isLetterOrDigit() }
    fun selectTrust(name: String) { ui = ui.copy(selectedTrust = name) }
    fun clearTrust() { ui = ui.copy(selectedTrust = null) }

    // ---- Quests tab --------------------------------------------------------
    // WHY THE TICKS ARE SHAPED THIS WAY. Two things bit the first version, and
    // both are avoided rather than patched around:
    //
    //   1. A tick is ONE immutable map, area -> set of lowercased quest names,
    //      replaced wholesale on every change. A brand-new value is the one
    //      thing Compose can never miss, so a row cannot show a tick the state
    //      does not hold.
    //   2. It is stored as ONE JSON string, not as putStringSet. A string set
    //      handed back by SharedPreferences is a cached instance with rules
    //      about mutating it, and "the tick was there until I left the page"
    //      is exactly what breaking those rules looks like. A string has no
    //      such trap.
    //
    // It is also read where it is declared, not after the quest db loads, so a
    // slow or failed asset read can never cost a tick. (It has to be a property
    // initializer rather than a line in init{}: Kotlin runs those in declaration
    // order, and this property is declared well below the init block.) Being one
    // JSON blob also makes it the natural payload if this ever syncs with
    // OmniWatch.
    private var questTicks by mutableStateOf(readQuestTicks())

    fun questAreas(): List<QuestArea> = questDb?.areas ?: emptyList()
    fun questArea(key: String): QuestArea? = questDb?.area(key)
    fun selectQuestArea(key: String) { ui = ui.copy(selectedQuestArea = key) }
    fun clearQuestArea() { ui = ui.copy(selectedQuestArea = null) }

    private fun readQuestTicks(): Map<String, Set<String>> {
        val raw = prefs.getString(QUEST_TICKS_KEY, null) ?: return readLegacyQuestTicks()
        return runCatching {
            val o = org.json.JSONObject(raw)
            val out = HashMap<String, Set<String>>()
            for (k in o.keys()) {
                val arr = o.optJSONArray(k) ?: continue
                val set = HashSet<String>()
                for (i in 0 until arr.length()) set.add(arr.optString(i))
                if (set.isNotEmpty()) out[k] = set
            }
            out
        }.getOrElse { emptyMap() }
    }

    /**
     * Anything ticked under the first build's per-area string sets, brought
     * across once so nobody re-ticks a list of ninety-five by hand.
     */
    private fun readLegacyQuestTicks(): Map<String, Set<String>> {
        val out = HashMap<String, Set<String>>()
        prefs.all.keys.filter { it.startsWith("questsdone_") }.forEach { k ->
            val set = prefs.getStringSet(k, emptySet()) ?: emptySet()
            if (set.isNotEmpty()) out[k.removePrefix("questsdone_")] = HashSet(set)
        }
        return out
    }

    private fun writeQuestTicks(m: Map<String, Set<String>>) {
        val o = org.json.JSONObject()
        m.forEach { (area, names) ->
            if (names.isNotEmpty()) o.put(area, org.json.JSONArray(names.toList()))
        }
        prefs.edit().putString(QUEST_TICKS_KEY, o.toString()).apply()
    }

    fun questDone(area: String, name: String): Boolean =
        questTicks[area]?.contains(name.lowercase()) == true

    fun toggleQuest(area: String, name: String) {
        val n = name.lowercase()
        val cur = questTicks[area].orEmpty()
        val next = if (n in cur) cur - n else cur + n
        val m = questTicks.toMutableMap()
        if (next.isEmpty()) m.remove(area) else m[area] = next
        questTicks = m          // new instance: the read side cannot miss it
        writeQuestTicks(m)
    }

    /** Completed count for an area, for the "n / m" on its row. */
    fun questDoneCount(area: String): Int {
        val done = questTicks[area] ?: return 0
        return questArea(area)?.quests?.count { it.name.lowercase() in done } ?: 0
    }

    /**
     * Keep ticks when the quest list changes: a quest that was renamed, or moved to another
     * area (the Unlocking a Myth quests now file under Aht Urhgan, as they do in the game's
     * log), carries its tick to its new name and place. Runs once each time the list loads;
     * a tick that already matches is left alone, so running it again changes nothing.
     */
    private fun migrateQuestTicks() {
        val db = questDb ?: return
        val renamed = mapOf(
            "lure of the wildcat" to mapOf(
                "sandoria" to "lure of the wildcat (san d'oria)",
                "windurst" to "lure of the wildcat (windurst)",
                "jeuno" to "lure of the wildcat (jeuno)",
                "aht_urhgan" to "lure of the wildcat (whitegate)"),
            "her memories: the grave resolve" to mapOf("" to "her memories: grave resolve"),
            "vw op. #054: elshimo list" to mapOf("" to "vw op. 054: elshimo list"),
            "vw op. #101: detour to zepwell" to mapOf("" to "vw op. 101: detour to zepwell"),
            "vw op. #115: li'telor variant" to mapOf("" to "vw op. 115: li'telor variant"))
        val names = db.areas.associate { a -> a.key to a.quests.map { it.name.lowercase() }.toSet() }
        val m = HashMap<String, MutableSet<String>>()
        var changed = false
        for ((area, ticks) in questTicks) {
            for (t in ticks) {
                var name = t
                val r = renamed[t]
                if (r != null) { name = r[area] ?: r[""] ?: t; if (name != t) changed = true }
                var dest = area
                if (names[area]?.contains(name) != true) {
                    names.entries.firstOrNull { name in it.value }?.let { dest = it.key; changed = true }
                }
                m.getOrPut(dest) { HashSet() }.add(name)
            }
        }
        if (!changed) return
        questTicks = m
        writeQuestTicks(m)
    }

    // ---- Quest ticks shared with OmniWatch's checklist ---------------------
    var questSyncMsg by mutableStateOf<String?>(null)
        private set
    var questSyncing by mutableStateOf(false)
        private set

    fun questLinked(): Boolean = CharLink.load(prefs) != null

    /**
     * Sync with OmniWatch's checklist: both sides end up with every tick either had (nothing is
     * ever unticked by a sync). OmniWatch's ticks are for the character it has loaded.
     */
    fun syncQuests() {
        val link = CharLink.load(prefs) ?: return
        if (questSyncing) return
        questSyncing = true; questSyncMsg = null
        val mine = questTicks
        viewModelScope.launch {
            val r = withContext(Dispatchers.IO) { CharLink.syncQuests(link, mine) }
            questSyncing = false
            if (r == null) { questSyncMsg = "Couldn't reach OmniWatch."; return@launch }
            val db = questDb
            val m = questTicks.mapValues { it.value.toMutableSet() }.toMutableMap()
            var gained = 0
            for ((area, names) in r.ticks) {
                val known = db?.area(area)?.quests?.map { it.name.lowercase() }?.toSet() ?: continue
                for (n in names) if (n in known && m.getOrPut(area) { HashSet() }.add(n)) gained++
            }
            if (gained > 0) { questTicks = m; writeQuestTicks(m) }
            val who = r.character.ifBlank { "OmniWatch" }
            questSyncMsg = "Synced with $who: $gained new here, ${r.added} new in OmniWatch." +
                if (r.unmatched > 0) " ${r.unmatched} not in OmniWatch's list." else ""
        }
    }

    // ---- Missions and Mounts (ticks shared with OmniWatch's checklist) -------
    private var checklistDb: ChecklistDb? = null
    private fun clDb(): ChecklistDb? = checklistDb ?: runCatching { ChecklistDb.load(getApplication()) }.getOrNull()
        .also { checklistDb = it }

    private var clTicks by mutableStateOf(readClTicks())
    var clSyncMsg by mutableStateOf<Map<String, String>>(emptyMap())
        private set
    var clSyncing by mutableStateOf<String?>(null)
        private set

    private fun readClTicks(): Map<String, Set<String>> = runCatching {
        val o = org.json.JSONObject(prefs.getString("checklist_ticks", "{}")!!)
        val out = HashMap<String, Set<String>>()
        for (k in o.keys()) {
            val a = o.optJSONArray(k) ?: continue
            out[k] = (0 until a.length()).map { a.optString(it) }.toSet()
        }
        out as Map<String, Set<String>>
    }.getOrDefault(emptyMap())

    private fun writeClTicks(m: Map<String, Set<String>>) {
        val o = org.json.JSONObject()
        m.forEach { (k, v) -> if (v.isNotEmpty()) o.put(k, org.json.JSONArray(v.toList())) }
        prefs.edit().putString("checklist_ticks", o.toString()).apply()
    }

    fun missionCats(): List<ClCat> = clDb()?.missions ?: emptyList()
    fun missionCat(key: String): ClCat? = clDb()?.mission(key)
    fun mounts(): List<ClItem> = clDb()?.mounts ?: emptyList()
    fun selectMissionCat(key: String) { ui = ui.copy(selectedMissionCat = key) }
    fun clearMissionCat() { ui = ui.copy(selectedMissionCat = null) }

    fun clDone(cat: String, id: String): Boolean = clTicks[cat]?.contains(id) == true
    fun clDoneCount(cat: String, items: List<ClItem>): Int {
        val d = clTicks[cat] ?: return 0
        return items.count { it.id in d }
    }
    fun toggleCl(cat: String, id: String) {
        val cur = clTicks[cat].orEmpty()
        val m = clTicks.toMutableMap()
        m[cat] = if (id in cur) cur - id else cur + id
        clTicks = m; writeClTicks(m)
    }
    fun clearCl(cat: String) { val m = clTicks.toMutableMap(); m.remove(cat); clTicks = m; writeClTicks(m) }

    /** Sync one tab's ticks ("missions", "mounts" or "trusts") with OmniWatch's checklist, both ways. */
    fun syncChecklist(tab: String) {
        val link = CharLink.load(prefs) ?: return
        if (clSyncing != null) return
        val keys = when (tab) {
            "mounts" -> setOf(ChecklistDb.MOUNTS)
            TRUSTS -> setOf(TRUSTS)
            else -> missionCats().map { it.key }.toSet()
        }
        val mine = keys.associateWith { clTicks[it].orEmpty() }.filterValues { it.isNotEmpty() }
        clSyncing = tab
        viewModelScope.launch {
            val r = withContext(Dispatchers.IO) { CharLink.syncChecklist(link, mine) }
            clSyncing = null
            if (r == null) { clSyncMsg = clSyncMsg + (tab to "Couldn't reach OmniWatch."); return@launch }
            val known = when (tab) {
                "mounts" -> mapOf(ChecklistDb.MOUNTS to mounts().map { it.id }.toSet())
                TRUSTS -> emptyMap()
                else -> missionCats().associate { it.key to it.items.map { i -> i.id }.toSet() }
            }
            val m = clTicks.mapValues { it.value.toMutableSet() }.toMutableMap()
            var gained = 0
            if (tab == TRUSTS) {
                // OmniWatch sends every name each trust it has goes by; match on letters and digits.
                val theirs = r.ticks[TRUSTS].orEmpty().map { trustKey(it) }.toSet()
                for (t in trustDb?.trusts.orEmpty()) {
                    val forms = listOf(t.name, t.name.replace(Regex("(?i)\\bangel\\s+"), ""))
                    if (forms.any { trustKey(it) in theirs } && m.getOrPut(TRUSTS) { HashSet() }.add(t.name.lowercase())) gained++
                }
            }
            for ((cat, ids) in r.ticks) {
                val ok = known[cat] ?: continue
                for (i in ids) if (i in ok && m.getOrPut(cat) { HashSet() }.add(i)) gained++
            }
            if (gained > 0) { clTicks = m; writeClTicks(m) }
            val sent = mine.values.sumOf { it.size }
            val who = r.character.ifBlank { "OmniWatch" }
            clSyncMsg = clSyncMsg + (tab to "Synced with $who: $gained new here, ${r.added} new in OmniWatch." +
                if (r.unmatched > 0 && sent > 0) " ${r.unmatched} not in OmniWatch's list." else "")
        }
    }

    /** Wipe one area's ticks. Offered on the area page so a mis-tap is undoable. */
    fun clearQuestTicks(area: String) {
        val m = questTicks.toMutableMap()
        m.remove(area)
        questTicks = m
        writeQuestTicks(m)
    }

    // ---- Weapon-skill reference (Chains tab) -------------------------------
    fun wsWeapons(): List<WsWeapon> = wsListDb?.weapons ?: emptyList()
    /** Chain properties for a listed WS, or null when it has none ("No Property"). */
    fun wsChainInfo(name: String): WeaponSkill? = scDb?.wsByName(name)
    fun openWsList() { ui = ui.copy(showWsList = true) }
    fun closeWsList() { ui = ui.copy(showWsList = false) }

    // ---- Content tab -------------------------------------------------------
    fun selectContent(k: String) { ui = ui.copy(selectedContent = k, selectedContentZone = null) }
    fun clearContent() { ui = ui.copy(selectedContent = null, selectedContentZone = null) }
    fun selectContentZone(zone: String) { ui = ui.copy(selectedContentZone = zone) }
    fun clearContentZone() { ui = ui.copy(selectedContentZone = null) }

    // Mobs carrying a `Group: Section` content tag, in the Content view's own order:
    // declared bosses first, then NMs, then regular; ties by level, then name.
    fun mobsForContent(group: String, section: String): List<Mob> {
        val hit = { t: String ->
            val p = t.split(":").map { it.trim() }
            p.getOrElse(0) { "" } == group && p.getOrElse(1) { "" } == section
        }
        return (mobDb?.all() ?: emptyList()).filter { m -> m.content.any(hit) }
    }

    // Mobs whose name starts with any of the given prefixes (e.g. "Apex ", "Locus ").
    fun mobsByNamePrefix(vararg prefixes: String): List<Mob> =
        (mobDb?.all() ?: emptyList()).filter { m -> prefixes.any { m.name.startsWith(it, ignoreCase = true) } }

    // The third `: Role` segment of a mob's tag for this group/section, or "".
    fun contentRoleOf(mob: Mob, group: String, section: String): String =
        mob.content.map { it.split(":").map { p -> p.trim() } }
            .firstOrNull { it.getOrElse(0) { "" } == group && it.getOrElse(1) { "" } == section }
            ?.getOrElse(2) { "" } ?: ""

    fun selectZone(zone: Zone) { ui = ui.copy(selectedZone = zone, showMap = false) }

    // Jump from a Content area page to that zone's full entry in the Zones tab (where
    // the map, if any, lives). Switches mode so the Zones-tab dispatch picks it up.
    fun openZoneDetailByName(name: String) {
        val z = zoneDb?.all()?.firstOrNull { it.name.equals(name, ignoreCase = true) } ?: return
        ui = ui.copy(mode = "maps", selectedZone = z, showMap = false,
            selectedContent = null, selectedContentZone = null)
    }

    fun hasZone(name: String): Boolean =
        zoneDb?.all()?.any { it.name.equals(name, ignoreCase = true) } == true

    fun selectZoneByName(name: String) {
        zoneDb?.all()?.firstOrNull { it.name.equals(name, ignoreCase = true) }?.let { selectZone(it) }
    }

    fun openMap() { ui = ui.copy(showMap = true) }

    fun closeMap() { ui = ui.copy(showMap = false) }

    // inZone carries the zone the user tapped THROUGH, so the detail header shows that
    // zone's own level rather than the flattened global lv band. Passing null (or a zone
    // the mob has no level for) CLEARS mobLevelCtx — without that, a level from a
    // previously-viewed mob leaks onto this one, since only clearMob()/back() reset it.
    fun selectMob(mob: Mob, inZone: String? = null) {
        val lvl = inZone?.let { z -> mob.zones.firstOrNull { it.first == z }?.second } ?: ""
        ui = ui.copy(selectedMob = mob, selectedSubtype = null, mobLevelCtx = lvl)
    }
    fun setMobView(v: String) { ui = ui.copy(mobView = v) }
    fun setZoneView(v: String) { ui = ui.copy(zoneView = v) }
    fun defaultMobView(): String = prefs.getString("defMobView", "all") ?: "all"
    fun defaultZoneView(): String = prefs.getString("defZoneView", "all") ?: "all"
    fun setDefaultMobView(v: String) { prefs.edit().putString("defMobView", v).apply(); ui = ui.copy(mobView = v) }
    fun setDefaultZoneView(v: String) { prefs.edit().putString("defZoneView", v).apply(); ui = ui.copy(zoneView = v) }
    fun setMobFilter(v: String) { ui = ui.copy(mobFilter = v) }
    fun setZoneFilter(v: String) { ui = ui.copy(zoneFilter = v) }
    fun clearMob() { ui = ui.copy(selectedMob = null, selectedSubtype = null, mobLevelCtx = "") }
    fun selectSubtype(sub: SubType) { ui = ui.copy(selectedSubtype = sub) }
    fun clearSubtype() { ui = ui.copy(selectedSubtype = null) }
    fun selectMobByName(name: String, level: String = "") { mobDb?.get(name.lowercase())?.let { ui = ui.copy(selectedMob = it, mobLevelCtx = level) } }
    fun zoneInfo(slug: String): ZoneInfo? = zoneInfoDb?.forSlug(slug)
    fun zoneType(zone: Zone): String = zoneInfoDb?.forSlug(zone.slug)?.type ?: ""
    fun zoneRegion(zone: Zone): String {
        val ov = zoneInfoDb?.forSlug(zone.slug)?.regionOverride
        return if (!ov.isNullOrBlank()) ov else zone.region.ifBlank { "Miscellaneous" }
    }

    /** Asset path for a family icon, or null. */
    fun mobIconPath(family: String): String? = mobDb?.iconPath(family)

    /** Per-mob user notes, persisted in prefs. */
    fun mobNote(key: String): String = prefs.getString("note_$key", "") ?: ""
    fun setMobNote(key: String, text: String) { prefs.edit().putString("note_$key", text).apply() }

    /** Ability description info, or null. */
    fun ability(name: String): AbilityInfo? = mobDb?.ability(name)
    fun familyNotes(family: String): List<String> = mobDb?.familyNotes(family) ?: emptyList()
    fun subtypes(family: String): List<SubType> = mobDb?.subtypes(family) ?: emptyList()
    fun resistSets(family: String): List<ResistSet> = mobDb?.resistSets(family) ?: emptyList()
    fun subtypeNotes(mob: Mob): List<String> =
        mob.sub?.let { s -> mobDb?.subtypes(mob.family)?.firstOrNull { it.name.equals(s, true) }?.notes } ?: emptyList()
    fun ecosystem(family: String): String? = mobDb?.ecosystem(family)
    fun ecosystemOf(mob: Mob): String? = mobDb?.ecosystemOf(mob)
    fun iconForMob(mob: Mob): String? = mobDb?.iconForMob(mob)

    fun setWorld(world: String) {
        if (world == ui.world) return
        ui = ui.copy(world = world)
        prefs.edit().putString("world", world).apply()
        refreshPopulation()
        ui.selected?.let { select(it) }   // re-pull the open item on the new world
    }

    private fun xsForm(): String = if (ui.filter == "stack") "stack" else "single"

    fun setFilter(f: String) {
        ui = ui.copy(filter = f)
        ui.selected?.let { loadCrossServer(it) }   // ranking follows the toggle
    }

    fun back() { ui = ui.copy(selected = null, selectedMob = null, selectedSubtype = null, mobLevelCtx = "", selectedZone = null, selectedJob = null, selectedSpell = null, selectedPet = null, showMap = false, history = emptyList(), crossRanking = emptyList(), historyNote = null) }

    fun refreshPopulation() {
        val h = host() ?: return
        val token = ++popToken
        ui = ui.copy(population = "\u2026")
        viewModelScope.launch {
            val total = withContext(Dispatchers.IO) {
                runCatching { SearchEngine.queryPopulation(h) }.getOrNull()
            }
            if (token != popToken) return@launch
            ui = ui.copy(population = if (total != null) "%,d online".format(total) else "no reply")
        }
    }

    private var nmToken = 0
    fun refreshNm() {
        val world = ui.world
        val token = ++nmToken
        ui = ui.copy(nmLoading = true, nmError = false)
        viewModelScope.launch {
            val list = withContext(Dispatchers.IO) { runCatching { WhereIsNm.fetch(world) }.getOrNull() }
            if (token != nmToken) return@launch
            ui = ui.copy(nmLoading = false, nm = list ?: emptyList(), nmError = list == null)
        }
    }

    private var seToken = 0
    fun refreshSe() {
        val token = ++seToken
        ui = ui.copy(seLoading = true, seError = false)
        viewModelScope.launch {
            val list = withContext(Dispatchers.IO) { runCatching { SeEvents.fetch() }.getOrNull() }
            if (token != seToken) return@launch
            ui = ui.copy(seLoading = false, se = list ?: emptyList(), seError = list == null)
        }
    }

    private var diToken = 0
    fun refreshDi() {
        val world = ui.world
        val token = ++diToken
        ui = ui.copy(diLoading = true, diError = false)
        viewModelScope.launch {
            val info = withContext(Dispatchers.IO) { runCatching { DomainInvasion.fetch(world) }.getOrNull() }
            if (token != diToken) return@launch
            ui = ui.copy(diLoading = false, di = info, diError = info == null)
        }
    }

    fun select(item: Item) {
        ui = ui.copy(selected = item, filter = "all", history = emptyList(),
            onsaleSingle = null, onsaleStack = null, historyLoading = true, historyNote = null)
        loadHistory(item)
        loadCrossServer(item)
    }

    private fun loadHistory(item: Item) {
        val h = host() ?: run { ui = ui.copy(historyLoading = false, historyNote = "No address for ${ui.world}"); return }
        val token = ++histToken
        viewModelScope.launch {
            val res = withContext(Dispatchers.IO) {
                val rows = ArrayList<SaleRow>()
                var single: Int? = null
                var stack: Int? = null
                var cat = -1
                for (isStack in listOf(false, true)) {
                    val hist = runCatching { SearchEngine.queryHistory(h, item.id, isStack) }.getOrNull()
                    if (hist != null && hist.ok) {
                        if (cat < 0) cat = hist.category
                        hist.sales.forEach { rows.add(SaleRow(it.price, it.date, it.seller, it.buyer, isStack)) }
                    }
                }
                if (cat >= 0) {
                    val listing = runCatching { SearchEngine.queryCategoryCounts(h, cat) }.getOrNull()
                    listing?.get(item.id)?.let { single = it.first; stack = it.second }
                }
                Triple(rows, single, stack)
            }
            if (token != histToken || ui.selected?.id != item.id) return@launch
            ui = ui.copy(
                historyLoading = false,
                history = res.first,
                onsaleSingle = res.second,
                onsaleStack = res.third,
                historyNote = if (res.first.isEmpty()) "No sales history / no answer" else null,
            )
        }
    }

    private fun loadCrossServer(item: Item) {
        val form = xsForm()
        crossCache[item.id]?.get(form)?.let {
            ui = ui.copy(crossRanking = it, crossForm = form, crossLoading = false); return
        }
        val token = ++crossToken
        val stack = form == "stack"
        ui = ui.copy(crossLoading = true, crossRanking = emptyList(), crossForm = form)
        viewModelScope.launch {
            val ranking = withContext(Dispatchers.IO) {
                Worlds.map.entries.map { (name, ip) ->
                    async {
                        val m = runCatching { SearchEngine.medianPrice(ip, item.id, stack) }.getOrNull()
                        if (m != null) name to m else null
                    }
                }.awaitAll().filterNotNull().sortedBy { it.second }
            }
            if (token != crossToken || ui.selected?.id != item.id || xsForm() != form) return@launch
            crossCache.getOrPut(item.id) { HashMap() }[form] = ranking
            ui = ui.copy(crossLoading = false, crossRanking = ranking, crossForm = form)
        }
    }

    // ---- skillchain calculator ----
    fun scSteps(): List<SkillchainResult> = scDb?.chain(ui.scChain) ?: emptyList()

    fun scAddWs(ws: WeaponSkill) { ui = ui.copy(scChain = ui.scChain + ws) }

    fun clearWs() { ui = ui.copy(scChain = emptyList()) }

    /** Another WS can be added unless we've reached a level-4 chain (or a length cap). */
    fun scCanContinue(): Boolean {
        if (ui.scChain.size >= 6) return false
        val steps = scSteps()
        return !(steps.isNotEmpty() && steps.last().level >= 4)
    }

    /** Valid weaponskills to add next: any opener at the start, else only WS that continue the chain. */
    fun scNextOptions(): List<WeaponSkill> {
        val db = scDb ?: return emptyList()
        val chain = ui.scChain
        return when {
            chain.isEmpty() -> db.weaponSkills
            chain.size == 1 -> db.weaponSkills.filter { db.chainsInto(chain[0].props, it.closingProps) }
            else -> {
                val last = scSteps().lastOrNull() ?: return emptyList()
                db.weaponSkills.filter { db.chainsInto(listOf(last.name), it.closingProps) }
            }
        }
    }

    fun slotTypes(): List<String> = scNextOptions().map { it.type }.distinct().sorted()

    fun slotWsOf(type: String): List<WeaponSkill> =
        scNextOptions().filter { it.type == type }.sortedBy { it.name }

    /** Sales filtered by the current single/stack toggle. */
    fun visibleSales(): List<SaleRow> = when (ui.filter) {
        "single" -> ui.history.filter { !it.stack }
        "stack" -> ui.history.filter { it.stack }
        else -> ui.history
    }.sortedByDescending { it.date }
}
