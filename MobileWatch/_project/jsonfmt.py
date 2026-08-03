#!/usr/bin/env python3
"""
jsonfmt — the ONE writer for every asset JSON in this project.

WHY THIS EXISTS
---------------
mobs.json was written as a single 4.68 MB line. That is unreadable, unsearchable
and impossible to hand-edit: no editor gives you a useful cursor position, and a
git diff of a one-line file is the whole file.

Full pretty-printing is not the answer either — `indent=1` turns mobs.json into
471,454 lines and 6.71 MB. You then scroll through 40 lines to see one monster.

THE FORMAT: ONE RECORD PER LINE.
Each entry of a big dictionary (mobs, abilities, families...) gets exactly one
line, compact inside. mobs.json becomes 9,025 lines and 4.70 MB — 0.4% bigger
than the minified original.

  - Ctrl+F "mountain peiste": lands on the one line that is that monster.
  - Editing a monster changes exactly one line, so git diffs read per-monster.
  - Median line 478 chars; turn word wrap on and a record is a short paragraph.

!! EVERY FUTURE proc_*.py MUST WRITE THROUGH THIS MODULE !!
Older scripts end with:

    json.dump(d, open(P, 'w'), separators=(', ', ': '), ensure_ascii=False)

which re-minifies the file back to one line and undoes the formatting. Replace
that with:

    import jsonfmt; jsonfmt.dump(d, P)

The bytes JSON.parse sees are identical either way — whitespace between tokens
is not data — so MobDb.load and the Android app cannot tell the difference.
`verify()` proves that on every write.
"""
import json
import os

# A container is exploded onto multiple lines only when its compact form is
# longer than this. Below it, a record reads fine as one line. Tuned so a mob
# record (median 478 chars) stays whole while a craft's recipe list does not.
INLINE_LIMIT = 2000

# How deep the exploding may go. Depth 1 is a top-level value like `mobs`;
# depth 2 is one monster. Most files need 2, recipes.json needs 3.
MAX_DEPTH = 4

# Compact but readable inside a record: ", " between items, ": " after keys.
_INLINE = dict(ensure_ascii=False, separators=(', ', ': '))


def _render(value, depth, pad):
    """Return the text for `value`, exploding it only if it is big and shallow."""
    inline = json.dumps(value, **_INLINE)
    if (len(inline) <= INLINE_LIMIT or depth > MAX_DEPTH
            or not isinstance(value, (dict, list)) or not value):
        return inline

    inner = pad + ' '
    if isinstance(value, dict):
        items = list(value.items())
        body = [inner + json.dumps(k, ensure_ascii=False) + ': '
                + _render(v, depth + 1, inner)
                + ('' if i == len(items) - 1 else ',')
                for i, (k, v) in enumerate(items)]
        return '{\n' + '\n'.join(body) + '\n' + pad + '}'
    body = [inner + _render(v, depth + 1, inner)
            + ('' if i == len(value) - 1 else ',')
            for i, v in enumerate(value)]
    return '[\n' + '\n'.join(body) + '\n' + pad + ']'


def dumps(data):
    """Render `data` in the one-record-per-line format."""
    return _render(data, 0, '') + '\n'


def verify(data, text):
    """Reparse the rendered text and assert it is the same object.

    This is the whole safety story: the format is only ever cosmetic, so a
    round-trip failure means the writer is broken and the write must not land.
    """
    if json.loads(text) != data:
        raise AssertionError('jsonfmt round-trip FAILED — refusing to write')


def dump(data, path, quiet=False):
    """Write `data` to `path` in the one-record-per-line format.

    Verifies the round-trip BEFORE touching the file, so a bug leaves the
    existing file intact rather than half-written.
    """
    text = dumps(data)
    verify(data, text)
    before = os.path.getsize(path) if os.path.exists(path) else 0
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    if not quiet:
        print('  %-42s %7.2f -> %7.2f MB, %d lines'
              % (path, before / 1e6, len(text.encode()) / 1e6, text.count('\n')))
    return text


if __name__ == '__main__':
    import sys
    targets = sys.argv[1:]
    if not targets:
        base = 'app/src/main/assets'
        if not os.path.isdir(base):
            base = 'android/' + base
        targets = sorted(os.path.join(base, f) for f in os.listdir(base)
                         if f.endswith('.json'))
    print('reformatting %d file(s) to one-record-per-line:' % len(targets))
    for p in targets:
        dump(json.load(open(p, encoding='utf-8')), p)
