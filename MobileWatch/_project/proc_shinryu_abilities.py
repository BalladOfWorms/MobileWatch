#!/usr/bin/env python3
"""Shinryu — abilities fleshed out and two errors corrected (rev 261). USER: "shinyru needs some
attention. i know shinyrus abilities need fleshed out a bit more, for example, mighty guard only
speaks of regain but it does more than that"

Source: the Shinryu BCNM page (Abyssea - Empyreal Paradox) — the ability block, the Physical and
Magical Qualities columns, and the Further Notes list.

TWO OUTRIGHT CORRECTIONS, both flagged in the handoff:
  * Protostar reset the WRONG SUBJECT. The def said it resets "its unused abilities"; the page says
    it resets every READY JOB ABILITY on its targets to full recast. That is a player-facing wipe,
    not a self-buff, and it is the single most important thing to know about the move.
  * Mighty Guard's Regain was 100 TP/tick in the file and is 10 TP/tick on the page, and the
    "nullifies any damage under 300" clause is not what the page describes at all.
"""
import json, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/src/main/assets/mobs.json'
d = json.load(open(P, encoding='utf-8'))
M, A = d['mobs'], d['abilities']
before = {k: json.dumps(A.get(k), ensure_ascii=False) for k in list(A)}

DEFS = {
    'Draw-In': {
        'd': "Pulls its current target, and every party member holding hate, to the user.",
        'r': "AoE", 'tgt': "AoE", 'fx': ["Draw-In"],
        'notes': "Players who have taken no action are not on its hate list and are not drawn in. It also draws the party in at random while readying a TP move or casting an area spell, so the whole alliance eats the follow-up.",
    },
    'Cataclysmic Vortex': {
        'd': "AoE magical damage that tries to reduce every target to 1 HP, and resets the enmity of whoever holds the most hate.",
        't': "Magical", 'tgt': "AoE",
        'notes': "Shell and -MDT% gear both cut the damage. The enmity reset frequently pulls a Draw-In straight afterwards, which can interrupt the cures you need right then.",
    },
    'Mighty Guard': {
        'd': "Restores roughly 15% of its own HP and raises two separate buffs: a one-minute damage shield and a dispellable 10 TP/tick Regain.",
        'tgt': "Self", 'fx': ["Regain", "Damage Shield"],
        'notes': "The shield completely nullifies spell damage and standard melee hits; weapon skills and the occasional critical hit punch through it. The Regain can be dispelled, the shield cannot. With its wings spread it will still absorb damage from attacks landed while it is casting or using TP, shield or no shield.",
    },
    'Cosmic Breath': {
        'd': "Front conal breath for moderate damage with Plague and Attack Down.",
        't': "Breath", 'r': "Front cone", 'tgt': "Cone AoE",
        'fx': ["Plague", "Attack Down", "Magic Attack Down", "Frost"],
        'notes': "Fires even with nobody in range. Standing to its sides avoids it outright, the same trick that lessens Wyrm breath.",
    },
    'Gyre Charge': {
        'd': "AoE physical damage with Paralysis and knockback.",
        't': "Physical", 'tgt': "AoE", 'fx': ["Paralysis", "Knockback"],
    },
    'Atomic Ray': {
        'd': "AoE magical damage and -50% to all attributes. Prevented by cruor buffs.",
        't': "Magical", 'el': "Fire", 'tgt': "AoE", 'fx': ["All Attributes Down"],
        'notes': "Unlocked at mid HP (66%-). Used while its wings are spread.",
    },
    'Dark Matter': {
        'd': "20' AoE magical damage with Terror (15+ seconds).",
        't': "Magical", 'tgt': "AoE", 'fx': ["Terror"],
        'notes': "Unlocked at mid HP (66%-).",
    },
    'Protostar': {
        'd': "20' AoE magical damage that resets every ready job ability on its targets to full recast — a whole-party ability wipe, not a self-buff.",
        't': "Magical", 'tgt': "AoE",
        'notes': "Unlocked at low HP (33%-). Used while its wings are spread, and it may also reset its current target's hate.",
    },
    'Supernova': {
        'd': "20' AoE magical damage with a 10-count Doom.",
        't': "Magical", 'tgt': "AoE", 'fx': ["Doom"],
        'notes': "Unlocked at low HP (33%-). Used while its wings are down; not used on Very Easy or Easy. Any Doom still running is removed on leaving the battlefield.",
    },
    'HP Cloak': {
        'd': "Its health bar stays hidden for the whole fight.",
        't': "Special", 'tgt': "Self",
        'notes': "Certain TP moves make the bar briefly visible — that is the only read you get on its HP.",
    },
    'Battle Stances': {
        'd': "Alternates between spread and folded wings, which changes how it takes damage.",
        't': "Special", 'tgt': "Self",
        'notes': "Wings spread: absorbs damage from any source if the hit lands during a TP move or a cast. Wings folded: absorbs nothing, but takes reduced damage from everything. It switches roughly every three minutes while active and always opens the fight with wings spread, however long you wait to engage.",
    },
}

NOTES = [
    "The Wyrm God, an Abyssea Notorious Monster fought in Abyssea-Empyreal Paradox (~65,000 HP; ~800,000 on the Very Difficult \u2605 battlefield). Entry needs 10,000 cruor and a Crimson traverser stone. Title Wyrm God Defier.",
    "Despite the name and the shape, it is NOT a member of the dragon family.",
    "Stances: it opens with wings spread and swaps roughly every three minutes. Spread, it absorbs damage dealt while it readies a weaponskill or casts, and uses -ga spells; folded, it absorbs nothing, takes about 30% less damage from everything, and casts Ancient Magic instantly. The page notes it is likely but UNCONFIRMED that Comet goes with folded wings and Meteor with spread.",
    "HP gates: at 66% it gains Atomic Ray, Dark Matter, tier-2 Ancient Magic and tier-5 -ga. At 33% it gains Protostar, Supernova, Comet and Meteor. It opens the fight with all tier-1 Ancient Magic and tier-4 -ga.",
    "Nearing defeat it may repeat one of Protostar, Supernova, Comet or Meteor up to five times in a row. Meteor spam has a 30-yalm range and is very hard to survive without a Primeval Brew; Fool's Drink and Fool's Powder are the usual answer.",
    "Its standard melee swings count as TP moves, the way an Iron Giant's do, so \"!!\" weaknesses can only be struck by timing your attacks into the gaps between its swings. Those swings are a conal AoE of roughly 10 yalms and are blocked by 1-4 Utsusemi shadows.",
    "It also hits anyone standing at its tail when it attacks, and the tail attacks carry an Additional Effect: Stun — which makes retreating after a Draw-In genuinely dangerous. Triggering a blue weakness stops it meleeing for the duration.",
    "Red, blue and yellow stagger windows key off the time SHINRYU HAS BEEN ENGAGED, not the time you entered the battlefield.",
    "Susceptible to red, blue and yellow \"!!\" staggers, and to Slow, Paralyze, Addle and Blind. Immune to Stun.",
    "The Atma is granted on winning AND on exiting the BCNM if you managed to trigger a red weakness. Any Atma, cruor enhancement and Abyssea temporary item may be used against it.",
    "Solo with a Primeval Brew is possible but has two traps. Supernova's Doom is not covered by the brew and will kill you fast — bring a Doom Screen. And using the brew while its wings are spread, into a TP move or a cast, feeds it a huge heal through Damage Absorption; wait for the wings to fold first.",
    "30-minute battlefield time limit. That is the standard BCNM clock and has nothing to do with Visitant status, which is unlimited in Abyssea - Empyreal Paradox.",
]

for name, defn in DEFS.items():
    A[name] = defn

s = M['shinryu']
s['notes'] = NOTES
ab = list(s.get('ab') or [])
for extra in ('HP Cloak', 'Battle Stances'):
    if extra not in ab:
        ab.append(extra)
s['ab'] = ab

# Empyreal Paradox held the only remaining flat Abyssea tag in the file. Shinryu is the whole zone,
# so it takes the Zone Boss role like the other nine and the screen stops treating it as a plain NM.
s['content'] = [t for t in (s.get('content') or []) if not t.startswith('Abyssea: Abyssea-Empyreal Paradox')] \
    + ['Abyssea: Abyssea-Empyreal Paradox: Zone Boss']

assert not [kk for mm in M.values() for kk, v in mm.items() if v is None]
assert all(A.get(a) for a in s['ab']), [a for a in s['ab'] if not A.get(a)]
json.dump(d, open(P, 'w', encoding='utf-8'), separators=(', ', ': '), ensure_ascii=False)

print('shinryu ab (%d): %s' % (len(s['ab']), ', '.join(s['ab'])))
print('shinryu sp: %s' % ', '.join(s.get('sp') or []))
print('notes: %d lines (was 2)' % len(NOTES))
print('\nability defs written:')
for name in DEFS:
    tag = 'NEW  ' if before.get(name) is None else ('same ' if before[name] == json.dumps(A[name], ensure_ascii=False) else 'REWR ')
    print('  %s %s' % (tag, name))
