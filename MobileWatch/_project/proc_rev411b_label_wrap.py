#!/usr/bin/env python3
"""
REV 411b — the five labels rev 411 deliberately left weighted.

Rev 411 swapped weight from label to value wherever the label was a plain
caption. These five are different: their `weight(1f)` is doing real layout work,
so it stays. But a weighted child can still be squeezed narrow, and a
single-word label with nowhere to break stacks one letter per line when that
happens. `softWrap = false` makes the worst case a clip instead of a stack.

  Resistances    weight is the spacer that pushes the < label > pager right
  Boarding /     three equal-weight header columns over the transport table
  Departure /
  Arrival
  Select a WS    weight pushes the dropdown arrow to the far right

The transport DATA rows below the header keep wrapping on purpose: those hold
real place names like "Port Bastok" that SHOULD flow onto a second line. The
difference is that a multi-word value breaks at the space; a one-word header
cannot, so only the header needs pinning.
"""
import re
import sys

P = 'app/src/main/kotlin/com/balladofworms/mobilewatch/ui/MobileWatchApp.kt'
text = open(P, encoding='utf-8').read()

TARGETS = [
    ('Text("Resistances", color = TextMuted, fontSize = 12.sp, modifier = Modifier.weight(1f))',
     'spacer for the resist-set pager'),
    ('Text("Boarding", color = TextMuted, fontSize = 12.sp, modifier = Modifier.weight(1f))',
     'transport header column 1'),
    ('Text("Departure", color = TextMuted, fontSize = 12.sp, modifier = Modifier.weight(1f))',
     'transport header column 2'),
    ('Text("Arrival", color = TextMuted, fontSize = 12.sp, modifier = Modifier.weight(1f))',
     'transport header column 3'),
    ('Text("Select a WS", color = TextMuted, fontSize = 14.sp, modifier = Modifier.weight(1f))',
     'spacer for the dropdown arrow'),
]

print('=== REV 411b — weight KEPT, wrapping pinned ===')
for old, why in TARGETS:
    if 'softWrap' in old:
        sys.exit('!! target already patched')
    n = text.count(old)
    if n != 1:
        sys.exit('!! expected exactly 1 match, found %d for: %s' % (n, old[:60]))
    new = old.replace(', modifier = Modifier.weight(1f))',
                      ', maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))')
    text = text.replace(old, new)
    label = re.search(r'"([^"]+)"', old).group(1)
    print('  %-14s %s' % (label, why))

# --- guards ------------------------------------------------------------------
print('\n=== GUARDS ===')
for ch, cl in (('{', '}'), ('(', ')'), ('[', ']')):
    a, b = text.count(ch), text.count(cl)
    print('  %s %d  %s %d  %s' % (ch, a, cl, b, 'balanced' if a == b else '!! UNBALANCED !!'))
    assert a == b

left = re.findall(r'Text\("[^"]+", color = TextMuted, fontSize = \d+\.sp, '
                  r'modifier = Modifier\.weight\(1f\)\)', text)
print('  weighted labels with no wrap guard remaining: %d %s' % (len(left), left))
assert not left

# the transport DATA rows must still be free to wrap
for field in ('r.board', 'r.depart', 'r.arrive'):
    pat = 'Text(%s, color = ' % field
    assert pat in text
    seg = text[text.index(pat):text.index(pat) + 160]
    assert 'softWrap' not in seg, 'data row was pinned by mistake: %s' % field
print('  transport data rows still wrap (correct): r.board, r.depart, r.arrive')

open(P, 'w', encoding='utf-8', newline='\n').write(text)
print('\nwritten: %s' % P)
