package com.balladofworms.mobilewatch.ui

import android.widget.Toast
import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.clickable
import androidx.compose.foundation.basicMarquee
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.LibraryMusic
import androidx.compose.material.icons.filled.PlaylistAdd
import androidx.compose.material.icons.filled.QueueMusic
import androidx.compose.material.icons.filled.RadioButtonUnchecked
import androidx.compose.material.icons.filled.SelectAll
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.FolderOpen
import androidx.compose.material.icons.filled.MusicNote
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Shuffle
import androidx.compose.material.icons.filled.SkipNext
import androidx.compose.material.icons.filled.SkipPrevious
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.balladofworms.mobilewatch.music.MusicPlayer
import com.balladofworms.mobilewatch.music.MusicTrack
import com.balladofworms.mobilewatch.ui.theme.*
import kotlinx.coroutines.delay

// The music player screen, opened from the note button in the header. Pick a folder once (your
// copied FFXI sound folders, and/or exported MP3/FLAC files) and every track in it is listed,
// named from OmniPlayer's catalogue. Music keeps playing when you leave this screen.

/** The header button: a note that lights up gold while music is playing. */
@Composable
internal fun MusicHeaderButton(onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(Icons.Filled.MusicNote, "Music",
            tint = if (MusicPlayer.playing) AccentGold else TextPrimary)
    }
}

/** The now-playing bar's colour -- blue, so it stands apart from the gold of the playing row. */
private val NowBlue = androidx.compose.ui.graphics.Color(0xFF4FA3FF)

private fun fmtTime(ms: Long): String {
    val s = (ms / 1000).coerceAtLeast(0)
    return "%d:%02d".format(s / 60, s % 60)
}

@Composable
internal fun MusicScreen(onBack: () -> Unit) {
    val ctx = LocalContext.current
    LaunchedEffect(Unit) { MusicPlayer.init(ctx) }
    // Android 13+: ask once to show notifications, for the player controls in the shade.
    val askNotify = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { }
    LaunchedEffect(Unit) {
        if (android.os.Build.VERSION.SDK_INT >= 33 &&
            ctx.checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) !=
                android.content.pm.PackageManager.PERMISSION_GRANTED)
            askNotify.launch(android.Manifest.permission.POST_NOTIFICATIONS)
    }
    val pickFolder = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri ->
        if (uri != null) MusicPlayer.addFolder(uri)
    }
    val msg = MusicPlayer.message
    LaunchedEffect(msg) {
        if (msg != null) { Toast.makeText(ctx, msg, Toast.LENGTH_SHORT).show(); MusicPlayer.message = null }
    }
    var query by rememberSaveable { mutableStateOf("") }
    var favOnly by rememberSaveable { mutableStateOf(false) }
    // Selection: long-press a track to start, then tap to add or remove; "select all" takes every
    // track in the list as shown (so after a search or the favourites filter, just those).
    var selectedList by rememberSaveable { mutableStateOf(listOf<String>()) }
    val selected = selectedList.toSet()
    val selecting = selected.isNotEmpty()
    fun toggleSel(t: MusicTrack) {
        selectedList = if (t.uri in selected) selectedList - t.uri else selectedList + t.uri
    }
    BackHandler(enabled = selecting) { selectedList = emptyList() }

    val all = MusicPlayer.tracks
    val favs = MusicPlayer.favourites
    val playlist = MusicPlayer.activePlaylist
    val lists = MusicPlayer.playlists
    // Name prompt for new / renamed playlists: (title, starting text, what to do with the name).
    var namePrompt by remember { mutableStateOf<Triple<String, String, (String) -> Boolean>?>(null) }
    val shown = remember(all, query, favOnly, favs, playlist, lists) {
        val q = query.trim().lowercase()
        // A playlist keeps its own order; the library is A-Z.
        val base = if (playlist != null) MusicPlayer.playlistTracks(playlist).asSequence()
                   else all.asSequence().sortedWith(compareBy({ it.title.lowercase() }, { it.fileName }))
        base.filter { !favOnly || MusicPlayer.isFav(it) }
            .filter {
                q.isEmpty() || it.title.lowercase().contains(q) || it.expansion.lowercase().contains(q) ||
                    it.composer.lowercase().contains(q) || it.fileName.lowercase().contains(q)
            }
            .toList()
    }

    Scaffold(
        containerColor = Charcoal,
        topBar = {
            if (selecting) {
                val chosen = shown.filter { it.uri in selected }
                val allFav = chosen.isNotEmpty() && chosen.all { MusicPlayer.isFav(it) }
                GradientTopBar("${selected.size} selected", onBack = { selectedList = emptyList() }, actions = {
                    IconButton(onClick = { selectedList = shown.map { it.uri } }) {
                        Icon(Icons.Filled.SelectAll, "Select all", tint = TextPrimary)
                    }
                    IconButton(onClick = { MusicPlayer.setFavs(chosen, !allFav) }) {
                        Icon(if (allFav) Icons.Filled.Favorite else Icons.Filled.FavoriteBorder,
                            if (allFav) "Remove from favourites" else "Add to favourites",
                            tint = if (allFav) AccentGold else TextPrimary)
                    }
                    Box {
                        var addMenu by remember { mutableStateOf(false) }
                        IconButton(onClick = { addMenu = true }) {
                            Icon(Icons.Filled.PlaylistAdd, "Add to playlist", tint = TextPrimary)
                        }
                        DropdownMenu(expanded = addMenu, onDismissRequest = { addMenu = false },
                            modifier = Modifier.background(CharcoalDark)) {
                            DropdownMenuItem(
                                text = { Text("New playlist\u2026", color = AccentGold) },
                                leadingIcon = { Icon(Icons.Filled.Add, null, tint = AccentGold) },
                                onClick = {
                                    addMenu = false
                                    val pick = chosen
                                    namePrompt = Triple<String, String, (String) -> Boolean>("New playlist", "") { n ->
                                        MusicPlayer.createPlaylist(n, pick).also { if (it) selectedList = emptyList() }
                                    }
                                })
                            lists.keys.filter { it != playlist }.forEach { name ->
                                DropdownMenuItem(
                                    text = { Text(name, color = TextPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                    leadingIcon = { Icon(Icons.Filled.QueueMusic, null, tint = TextMuted) },
                                    onClick = { addMenu = false; MusicPlayer.addToPlaylist(name, chosen); selectedList = emptyList() })
                            }
                        }
                    }
                    IconButton(onClick = {
                        // In a playlist: take them out of it. In the library: off the list.
                        if (playlist != null) MusicPlayer.removeFromPlaylist(playlist, chosen)
                        else MusicPlayer.removeTracks(chosen)
                        selectedList = emptyList()
                    }) {
                        Icon(Icons.Filled.Delete, if (playlist != null) "Remove from playlist" else "Remove from list",
                            tint = TextPrimary)
                    }
                    IconButton(onClick = {
                        // Play the selection as its own queue, in list order.
                        if (chosen.isNotEmpty()) MusicPlayer.play(chosen.first(), chosen)
                        selectedList = emptyList()
                    }) {
                        Icon(Icons.Filled.PlayArrow, "Play selected", tint = AccentGold)
                    }
                })
            } else GradientTopBar(playlist ?: "Music", onBack = onBack, actions = {
                if (shown.isNotEmpty()) IconButton(onClick = { selectedList = shown.map { it.uri } }) {
                    Icon(Icons.Filled.SelectAll, "Select all", tint = TextMuted)
                }
                IconButton(onClick = { favOnly = !favOnly }) {
                    Icon(if (favOnly) Icons.Filled.Favorite else Icons.Filled.FavoriteBorder,
                        "Favourites only", tint = if (favOnly) AccentGold else TextMuted)
                }
                if (MusicPlayer.hasFolder) Box {
                    var listMenu by remember { mutableStateOf(false) }
                    IconButton(onClick = { listMenu = true }) {
                        Icon(Icons.Filled.QueueMusic, "Playlists",
                            tint = if (playlist != null) AccentGold else TextMuted)
                    }
                    DropdownMenu(expanded = listMenu, onDismissRequest = { listMenu = false },
                        modifier = Modifier.background(CharcoalDark)) {
                        DropdownMenuItem(
                            text = { Text("All tracks", color = TextPrimary) },
                            leadingIcon = { Icon(Icons.Filled.LibraryMusic, null, tint = TextMuted) },
                            trailingIcon = { if (playlist == null) Icon(Icons.Filled.Check, null, tint = AccentGold) },
                            onClick = { listMenu = false; MusicPlayer.activePlaylist = null; selectedList = emptyList() })
                        lists.forEach { (name, keys) ->
                            DropdownMenuItem(
                                text = { Text("$name  (${keys.size})", color = TextPrimary, maxLines = 1,
                                    overflow = TextOverflow.Ellipsis) },
                                leadingIcon = { Icon(Icons.Filled.QueueMusic, null, tint = TextMuted) },
                                trailingIcon = { if (playlist == name) Icon(Icons.Filled.Check, null, tint = AccentGold) },
                                onClick = { listMenu = false; MusicPlayer.activePlaylist = name; selectedList = emptyList() })
                        }
                        HorizontalDivider(color = Selection)
                        DropdownMenuItem(
                            text = { Text("New playlist\u2026", color = AccentGold) },
                            leadingIcon = { Icon(Icons.Filled.Add, null, tint = AccentGold) },
                            onClick = {
                                listMenu = false
                                namePrompt = Triple<String, String, (String) -> Boolean>("New playlist", "") { n ->
                                    MusicPlayer.createPlaylist(n).also { if (it) MusicPlayer.activePlaylist = n.trim() }
                                }
                            })
                        if (playlist != null) {
                            DropdownMenuItem(
                                text = { Text("Rename \"$playlist\"\u2026", color = TextPrimary, maxLines = 1,
                                    overflow = TextOverflow.Ellipsis) },
                                leadingIcon = { Icon(Icons.Filled.Edit, null, tint = TextMuted) },
                                onClick = {
                                    listMenu = false
                                    namePrompt = Triple<String, String, (String) -> Boolean>("Rename playlist", playlist) { n -> MusicPlayer.renamePlaylist(playlist, n) }
                                })
                            DropdownMenuItem(
                                text = { Text("Delete \"$playlist\"", color = TextPrimary, maxLines = 1,
                                    overflow = TextOverflow.Ellipsis) },
                                leadingIcon = { Icon(Icons.Filled.Delete, null, tint = TextMuted) },
                                onClick = { listMenu = false; MusicPlayer.deletePlaylist(playlist) })
                        }
                    }
                }
                Box {
                    var folderMenu by remember { mutableStateOf(false) }
                    IconButton(onClick = {
                        // No folders yet: go straight to the picker; otherwise show the folders.
                        if (MusicPlayer.folders.isEmpty()) pickFolder.launch(null) else folderMenu = true
                    }) {
                        Icon(Icons.Filled.FolderOpen, "Music folders", tint = TextMuted)
                    }
                    DropdownMenu(expanded = folderMenu, onDismissRequest = { folderMenu = false },
                        modifier = Modifier.background(CharcoalDark)) {
                        DropdownMenuItem(
                            text = { Text("Add a folder\u2026", color = AccentGold) },
                            leadingIcon = { Icon(Icons.Filled.Add, null, tint = AccentGold) },
                            onClick = { folderMenu = false; pickFolder.launch(null) })
                        DropdownMenuItem(
                            text = { Text("Rescan folders", color = TextPrimary) },
                            leadingIcon = { Icon(Icons.Filled.Refresh, null, tint = TextMuted) },
                            onClick = { folderMenu = false; MusicPlayer.rescan() })
                        MusicPlayer.folders.forEach { f ->
                            DropdownMenuItem(
                                text = { Text(com.balladofworms.mobilewatch.music.MusicLibrary.treeLabel(f),
                                    color = TextPrimary, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                leadingIcon = { Icon(Icons.Filled.FolderOpen, null, tint = TextMuted) },
                                trailingIcon = {
                                    IconButton(onClick = { folderMenu = false; MusicPlayer.removeFolder(f) }) {
                                        Icon(Icons.Filled.Close, "Remove this folder", tint = TextMuted)
                                    }
                                },
                                onClick = { })
                        }
                    }
                }
            })
        },
        bottomBar = { if (MusicPlayer.current != null) NowPlayingBar() }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            when {
                !MusicPlayer.hasFolder -> EmptyMusic(onPick = { pickFolder.launch(null) })
                else -> {
                    CompactSearchField(
                        value = query, onValueChange = { query = it },
                        placeholder = "Search track, expansion or composer",
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 6.dp)
                    )
                    if (MusicPlayer.scanning) {
                        Row(Modifier.padding(horizontal = 16.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically) {
                            CircularProgressIndicator(Modifier.size(14.dp), strokeWidth = 2.dp, color = AccentGold)
                            Spacer(Modifier.width(8.dp))
                            Text("Reading the folder\u2026", color = TextMuted, fontSize = 12.sp)
                        }
                    }
                    if (shown.isEmpty() && !MusicPlayer.scanning) {
                        Text(if (playlist != null && query.isEmpty() && !favOnly)
                                 "This playlist is empty. Select tracks in All tracks, then add them with the playlist button."
                             else if (favOnly) "No favourites yet \u2014 tap a heart to add one."
                             else if (all.isEmpty()) "No music found. Tap the folder button to choose another folder."
                             else "Nothing matches.",
                            color = TextMuted, fontSize = 13.sp, modifier = Modifier.padding(16.dp))
                    }
                    LazyColumn(Modifier.fillMaxSize()) {
                        items(shown, key = { it.uri }) { t ->
                            TrackRow(t, shown, selecting, t.uri in selected, onSelect = { toggleSel(t) })
                        }
                    }
                }
            }
        }
    }
    namePrompt?.let { (title, start, action) ->
        NameDialog(title, start, onDismiss = { namePrompt = null }) { name ->
            if (action(name)) namePrompt = null
            else MusicPlayer.message = "That name is empty or already used"
        }
    }
}

@Composable
private fun NameDialog(title: String, start: String, onDismiss: () -> Unit, onOk: (String) -> Unit) {
    var text by remember { mutableStateOf(start) }
    AlertDialog(
        onDismissRequest = onDismiss,
        containerColor = CharcoalDark,
        title = { Text(title, color = AccentGold) },
        text = {
            OutlinedTextField(value = text, onValueChange = { text = it }, singleLine = true,
                placeholder = { Text("Playlist name") })
        },
        confirmButton = { TextButton(onClick = { onOk(text) }) { Text("OK", color = AccentGold) } },
        dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel", color = TextMuted) } }
    )
}

@Composable
private fun EmptyMusic(onPick: () -> Unit) {
    Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally) {
        Icon(Icons.Filled.MusicNote, null, tint = AccentGold, modifier = Modifier.size(48.dp))
        Spacer(Modifier.height(12.dp))
        Text("FINAL FANTASY XI music", color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        Spacer(Modifier.height(8.dp))
        Text("Copy the game's music onto your phone -- the sound, sound2, sound3 ... folders from your " +
             "FINAL FANTASY XI install (or just their win\\music\\data folders), or tracks you've " +
             "exported as MP3 or FLAC -- then add that folder here (add as many folders as you like). " +
             "Tracks are named automatically and loop the way the game loops them.",
            color = TextSoft, fontSize = 13.sp)
        Spacer(Modifier.height(16.dp))
        Button(onClick = onPick, colors = ButtonDefaults.buttonColors(containerColor = Selection)) {
            Icon(Icons.Filled.FolderOpen, null, tint = TextPrimary)
            Spacer(Modifier.width(8.dp))
            Text("Add a music folder", color = TextPrimary)
        }
        Spacer(Modifier.height(16.dp))
        Text("No music is included with MobileWatch; it plays the files from your own copy of the game.",
            color = TextMuted, fontSize = 11.sp)
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun TrackRow(t: MusicTrack, order: List<MusicTrack>, selecting: Boolean, isSel: Boolean,
                     onSelect: () -> Unit) {
    val isCur = MusicPlayer.current?.uri == t.uri
    val fav = MusicPlayer.isFav(t)
    Row(
        Modifier.fillMaxWidth()
            .background(if (isSel || isCur) Selection else Charcoal)
            .combinedClickable(
                onClick = { if (selecting) onSelect() else MusicPlayer.play(t, order) },
                onLongClick = onSelect)
            .padding(start = 4.dp, end = 14.dp, top = 2.dp, bottom = 2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (selecting) IconButton(onClick = onSelect) {
            Icon(if (isSel) Icons.Filled.CheckCircle else Icons.Filled.RadioButtonUnchecked,
                if (isSel) "Selected" else "Not selected",
                tint = if (isSel) AccentGold else TextMuted, modifier = Modifier.size(20.dp))
        } else IconButton(onClick = { MusicPlayer.toggleFav(t) }) {
            Icon(if (fav) Icons.Filled.Favorite else Icons.Filled.FavoriteBorder,
                if (fav) "Remove from favourites" else "Add to favourites",
                tint = if (fav) AccentGold else TextMuted, modifier = Modifier.size(20.dp))
        }
        Column(Modifier.weight(1f)) {
            Text(t.title, color = if (isCur) AccentGold else if (t.playable) TextPrimary else TextMuted, fontSize = 14.sp,
                fontWeight = if (isCur) FontWeight.Bold else FontWeight.Normal,
                maxLines = 1, overflow = TextOverflow.Ellipsis)
            val sub = if (!t.playable) "Can't play this file"
                else listOf(t.expansion, t.composer).filter { it.isNotBlank() }.joinToString("  \u00b7  ")
                    .ifBlank { t.fileName }
            Text(sub, color = TextMuted, fontSize = 11.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
        }
        Text(fmtTime((t.seconds * 1000).toLong()), color = TextMuted, fontSize = 12.sp,
            modifier = Modifier.padding(start = 8.dp))
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
private fun NowPlayingBar() {
    val t = MusicPlayer.current ?: return
    var pos by remember { mutableLongStateOf(0L) }
    var dragging by remember { mutableStateOf<Float?>(null) }
    LaunchedEffect(t.uri) {
        while (true) { if (dragging == null) pos = MusicPlayer.positionMs(); delay(250) }
    }
    val dur = MusicPlayer.durationMs().coerceAtLeast(1L)
    // A looping track's clock folds back into its loop section, so the bar stays in range.
    val shownPos = pos.coerceIn(0L, dur)
    Surface(color = CharcoalDark, tonalElevation = 0.dp) {
        Column(Modifier.fillMaxWidth().navigationBarsPadding().padding(horizontal = 16.dp, vertical = 10.dp)) {
            // Long titles slide sideways instead of being cut off.
            Text(t.title, color = NowBlue, fontWeight = FontWeight.Bold, fontSize = 16.sp,
                maxLines = 1, modifier = Modifier.basicMarquee(iterations = Int.MAX_VALUE))
            val sub = buildList {
                if (t.expansion.isNotBlank()) add(t.expansion)
                if (t.heard.isNotBlank()) add(t.heard)
            }.joinToString("  \u00b7  ")
            if (sub.isNotBlank()) Text(sub, color = TextMuted, fontSize = 11.sp, maxLines = 1,
                modifier = Modifier.basicMarquee(iterations = Int.MAX_VALUE))
            Slider(
                value = dragging ?: (shownPos.toFloat() / dur),
                onValueChange = { dragging = it },
                onValueChangeFinished = {
                    dragging?.let { MusicPlayer.seekTo((it * dur).toLong()); pos = (it * dur).toLong() }
                    dragging = null
                },
                colors = SliderDefaults.colors(thumbColor = NowBlue, activeTrackColor = NowBlue,
                    inactiveTrackColor = Selection),
                modifier = Modifier.fillMaxWidth().height(28.dp)
            )
            Row(Modifier.fillMaxWidth()) {
                val p = dragging?.let { (it * dur).toLong() } ?: shownPos
                Text(fmtTime(p), color = TextMuted, fontSize = 11.sp)
                Spacer(Modifier.weight(1f))
                Text(fmtTime(dur) + if (MusicPlayer.repeat && t.loops) "  \u221e" else "",
                    color = TextMuted, fontSize = 11.sp)
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = { MusicPlayer.changeRepeat(!MusicPlayer.repeat) }) {
                    Icon(Icons.Filled.Repeat, if (MusicPlayer.repeat) "Repeat on" else "Repeat off",
                        tint = if (MusicPlayer.repeat) NowBlue else TextMuted)
                }
                IconButton(onClick = { MusicPlayer.previous() }) {
                    Icon(Icons.Filled.SkipPrevious, "Previous", tint = TextPrimary, modifier = Modifier.size(30.dp))
                }
                Box(
                    Modifier.size(56.dp).clip(CircleShape).background(NowBlue)
                        .clickable { MusicPlayer.togglePause() },
                    contentAlignment = Alignment.Center
                ) {
                    if (MusicPlayer.loading) CircularProgressIndicator(Modifier.size(24.dp),
                        strokeWidth = 2.dp, color = Charcoal)
                    else Icon(if (MusicPlayer.playing) Icons.Filled.Pause else Icons.Filled.PlayArrow,
                        if (MusicPlayer.playing) "Pause" else "Play", tint = Charcoal,
                        modifier = Modifier.size(32.dp))
                }
                IconButton(onClick = { MusicPlayer.next() }) {
                    Icon(Icons.Filled.SkipNext, "Next", tint = TextPrimary, modifier = Modifier.size(30.dp))
                }
                IconButton(onClick = { MusicPlayer.changeShuffle(!MusicPlayer.shuffle) }) {
                    Icon(Icons.Filled.Shuffle, if (MusicPlayer.shuffle) "Shuffle on" else "Shuffle off",
                        tint = if (MusicPlayer.shuffle) NowBlue else TextMuted)
                }
            }
        }
    }
}
