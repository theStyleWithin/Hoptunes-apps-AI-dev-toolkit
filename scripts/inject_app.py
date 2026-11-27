#!/usr/bin/env python3
"""Injects an app that lives in its own repository into a person's FORK of Hop-tunes.

Usage:  python3 inject_app.py <app repository folder> --fork <your fork of Hop-tunes> [--dry-run]

The app repository has the layout described in docs/APP-REPOSITORY.md (an `app.json`, the app's QML in `qml/`, an optional icon in `images/`, a UI test in
`tests/ui_test.inc`, and for a networked app extra new files in `files/` and edits as `patches/*.patch`). This script copies the files into the fork and makes
the registration edits by hand-free, repeatable steps: src/ui/qml.qrc, the registry in AppsView.qml (appended at the END), AppHost.qml, and the UI test (placed
immediately before the apps-tab test). Running it again updates the app in place. It never touches git history, never pushes, and it REFUSES to run in a
clone whose origin is the official theStyleWithin/Hop-tunes repository: apps are only ever put into the person's own fork (docs/YOUR-OWN-BUILD.md).

It reads and writes files only (it builds nothing). Afterwards it runs scripts/check_app.py on the fork. A clean result means "registered and has a test", NOT
"works": build Hop-tunes and run the whole ctest suite (docs/TESTING.md). Undo an injection with git in your fork (`git checkout -- . && git clean -fd` on a
branch you made for it, or just delete the branch).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OFFICIAL = re.compile(r"github\.com[:/]+thestylewithin/hop-tunes(\.git)?/?$", re.I)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text, dry):
    if not dry:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


def die(msg):
    print("FAIL  " + msg)
    sys.exit(1)


def load_manifest(repo):
    path = os.path.join(repo, "app.json")
    if not os.path.exists(path):
        die("%s has no app.json (is this an app repository? see docs/APP-REPOSITORY.md)" % repo)
    try:
        m = json.loads(read(path))
    except ValueError as e:
        die("app.json is not valid JSON: %s" % e)
    problems = []
    if not re.fullmatch(r"[a-z][a-z0-9]{1,30}", str(m.get("id", ""))):
        problems.append('"id": lower-case letters and digits, starting with a letter (for example "sleeptimer")')
    name = str(m.get("name", ""))
    if not name or name != name.lower() or len(name) > 30 or '"' in name or "\\" in name:
        problems.append('"name": a short lower-case name for the tile (no quotes)')
    blurb = str(m.get("blurb", ""))
    if len(blurb) < 8 or '"' in blurb or "\\" in blurb or "\n" in blurb:
        problems.append('"blurb": one plain sentence for the tile\'s pop-up (no double quotes, no backslashes)')
    if not isinstance(m.get("net"), bool):
        problems.append('"net": true if the app uses the internet, else false')
    q = str(m.get("qml", ""))
    if not re.fullmatch(r"[A-Z][A-Za-z0-9]*App\.qml", q):
        problems.append('"qml": the file name in qml/, like "SleepTimerApp.qml" (a type name ending in App)')
    elif not os.path.exists(os.path.join(repo, "qml", q)):
        problems.append("qml/%s does not exist" % q)
    icon = str(m.get("icon", ""))
    if icon and (not re.fullmatch(r"[A-Za-z0-9_-]+\.png", icon) or not os.path.exists(os.path.join(repo, "images", icon))):
        problems.append('"icon": a PNG file name that exists in images/ (or "" for the plain glass tile)')
    if not os.path.exists(os.path.join(repo, "tests", "ui_test.inc")):
        problems.append("tests/ui_test.inc is missing (every app needs a UI test)")
    if problems:
        print("FAIL  app.json / layout problems:")
        for p in problems:
            print("      - " + p)
        sys.exit(1)
    return m


def check_repo_files(repo, m):
    """Warnings about the app repository itself (not blockers)."""
    warn = []
    qml = read(os.path.join(repo, "qml", m["qml"]))
    if "SPDX-License-Identifier: GPL-3.0-or-later" not in qml:
        warn.append("qml/%s has no SPDX GPL-3.0-or-later header (every file in Hop-tunes has one)" % m["qml"])
    if not re.search(r'objectName:\s*"', qml):
        warn.append("the app's QML has no objectName for the test to find")
    if not m["net"]:
        bad = [w for w in ("XMLHttpRequest", "WebSocket", "https://", "http://", "QtNetwork") if w in qml]
        if bad:
            warn.append("net is false but the QML uses network words: " + ", ".join(bad))
    test = read(os.path.join(repo, "tests", "ui_test.inc"))
    if ('appTile_%s' % m["id"]) not in test:
        warn.append('the UI test never opens the tile ("appTile_%s")' % m["id"])
    if "QTRY_VERIFY" not in test:
        warn.append("the UI test never waits with QTRY_VERIFY")
    if "Key_Escape" not in test:
        warn.append("the UI test never closes the app with Esc")
    return warn


def git_origin(fork):
    try:
        return subprocess.run(["git", "-C", fork, "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app_repo")
    ap.add_argument("--fork", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    repo, fork, dry = os.path.abspath(args.app_repo), os.path.abspath(args.fork), args.dry_run

    m = load_manifest(repo)
    for w in check_repo_files(repo, m):
        print("WARN  " + w)

    qrc_p = os.path.join(fork, "src/ui/qml.qrc")
    view_p = os.path.join(fork, "src/ui/qml/AppsView.qml")
    host_p = os.path.join(fork, "src/ui/qml/AppHost.qml")
    test_p = os.path.join(fork, "tests/test_ui.cpp")
    for p in (qrc_p, view_p, host_p, test_p):
        if not os.path.exists(p):
            die("this does not look like a Hop-tunes source (missing %s): check --fork" % os.path.relpath(p, fork))
    origin = git_origin(fork)
    if OFFICIAL.search(origin):
        die("the origin of %s is the OFFICIAL Hop-tunes repository (%s). Apps are only ever put into the person's own FORK: ask them to fork Hop-tunes on GitHub, "
            "clone the fork, and run this again there (docs/YOUR-OWN-BUILD.md)." % (fork, origin))
    if not origin:
        print("WARN  could not read the git origin of the fork: make sure it is the person's own fork, never the official repository")

    app, name, blurb, typ = m["id"], m["name"], m["blurb"], m["qml"][:-4]
    comp = typ[0].lower() + typ[1:]
    out = []

    # 1. copy the files
    def copy(src, dst):
        out.append("copy   %s -> %s" % (os.path.relpath(src, repo), os.path.relpath(dst, fork)))
        if not dry:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    copy(os.path.join(repo, "qml", m["qml"]), os.path.join(fork, "src/ui/qml", m["qml"]))
    if m.get("icon"):
        copy(os.path.join(repo, "images", m["icon"]), os.path.join(fork, "src/ui/images", m["icon"]))
    files_root = os.path.join(repo, "files")
    if os.path.isdir(files_root):
        for d, _, fs in os.walk(files_root):
            for f in sorted(fs):
                src = os.path.join(d, f)
                rel = os.path.relpath(src, files_root)
                if rel.startswith("..") or os.path.isabs(rel):
                    die("bad path in files/: " + rel)
                copy(src, os.path.join(fork, rel))

    # 2. qml.qrc
    qrc = read(qrc_p)
    new_files = ["    <file>qml/%s</file>" % m["qml"]]
    if m.get("icon"):
        new_files.append('    <file alias="images/%s">images/%s</file>' % (m["icon"], m["icon"]))
    for line in new_files:
        if line.strip() in qrc:
            continue
        anchor = "    <file>qml/KickApp.qml</file>" if line.startswith("    <file>qml/") else None
        if line.startswith("    <file alias"):
            mm = re.search(r'^[ \t]*<file alias="images/app-kick.png">.*$', qrc, re.M)
            anchor = mm.group(0) if mm else None
        if not anchor or anchor not in qrc:
            die("could not find where to add %s in src/ui/qml.qrc (is this Hop-tunes 1.15 or newer?). Add it by hand next to the other app files." % line.strip())
        qrc = qrc.replace(anchor, anchor + "\n" + line, 1)
        out.append("edit   src/ui/qml.qrc: " + line.strip())
    write(qrc_p, qrc, dry)

    # 3. the registry: an entry at the END of allApps (replaced in place when it is already there)
    view = read(view_p)
    icon_url = ('"qrc:/images/%s"' % m["icon"]) if m.get("icon") else '""'
    entry = '        { id: "%s", name: "%s", blurb: "%s", icon: %s, net: %s }' % (app, name, blurb, icon_url, "true" if m["net"] else "false")
    mm = re.search(r'readonly property var allApps: \[\n(.*?)\n    \]', view, re.S)
    if not mm:
        die("could not find `allApps` in src/ui/qml/AppsView.qml: this Hop-tunes is not the shape the toolkit expects. Add the entry by hand (docs/ADD-AN-APP.md).")
    lines = mm.group(1).split("\n")
    idx = [i for i, l in enumerate(lines) if re.search(r'\{\s*id:\s*"%s"\s*,' % re.escape(app), l)]
    if idx:
        trailing = "," if lines[idx[0]].rstrip().endswith(",") else ""
        lines[idx[0]] = entry + trailing
        out.append("edit   src/ui/qml/AppsView.qml: updated the registry entry for %s" % app)
    else:
        lines[-1] = lines[-1].rstrip().rstrip(",") + ","
        lines.append(entry)
        out.append("edit   src/ui/qml/AppsView.qml: appended the registry entry for %s (at the end)" % app)
    view = view[:mm.start(1)] + "\n".join(lines) + view[mm.end(1):]
    write(view_p, view, dry)

    # 4. the host
    host = read(host_p)
    nm = re.search(r'readonly property var names: \(\{(.*?)\}\)', host, re.S)
    if not nm:
        die("could not find the `names` map in src/ui/qml/AppHost.qml. Edit AppHost.qml by hand (docs/ADD-AN-APP.md step 3).")
    if not re.search(r'"%s"\s*:' % re.escape(app), nm.group(1)):
        inner = nm.group(1)
        stripped = inner.rstrip()
        inner2 = (stripped + ", " if stripped else " ") + '"%s": "%s"' % (app, name) + inner[len(stripped):]
        host = host[:nm.start(1)] + inner2 + host[nm.end(1):]
        out.append('edit   src/ui/qml/AppHost.qml: added "%s" to names' % app)
    chain = re.search(r'(sourceComponent:[^\n]*?) : null', host)
    if not chain:
        die("could not find the `sourceComponent` chain in src/ui/qml/AppHost.qml. Edit it by hand (docs/ADD-AN-APP.md step 3).")
    if not re.search(r'appId\s*===\s*"%s"' % re.escape(app), host):
        host = host.replace(chain.group(0), '%s : root.appId === "%s" ? %s : null' % (chain.group(1), app, comp), 1)
        out.append("edit   src/ui/qml/AppHost.qml: the sourceComponent chain loads %s" % comp)
    if not re.search(r'Component\s*\{\s*id:\s*%s\s*;' % re.escape(comp), host):
        body = "%s { onLeave: { root.appId = \"\"; root.leave() } }" % typ if m.get("leaves") else "%s { }" % typ
        first = re.search(r'^[ \t]*Component \{ id: \w+;', host, re.M)
        if not first:
            die("could not find the Component lines in src/ui/qml/AppHost.qml. Edit it by hand (docs/ADD-AN-APP.md step 3).")
        host = host[:first.start()] + "    Component { id: %s; %s }\n" % (comp, body) + host[first.start():]
        out.append("edit   src/ui/qml/AppHost.qml: added the Component for %s" % typ)
    write(host_p, host, dry)

    # 5. the UI test, between markers, immediately before the apps-tab test
    test = read(test_p)
    inc = read(os.path.join(repo, "tests", "ui_test.inc")).strip("\n")
    begin, end = "    // BEGIN hoptunes-app:%s (from the app repository: edit it there, then inject again)" % app, "    // END hoptunes-app:%s" % app
    block = begin + "\n" + inc + "\n" + end + "\n\n"
    old = re.search(r'^[ \t]*// BEGIN hoptunes-app:%s\b.*?^[ \t]*// END hoptunes-app:%s\n\n?' % (re.escape(app), re.escape(app)), test, re.S | re.M)
    if old:
        test = test[:old.start()] + block + test[old.end():]
        out.append("edit   tests/test_ui.cpp: updated the UI test for %s" % app)
    else:
        fn = re.search(r'^[ \t]*void appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow\(\)', test, re.M)
        if not fn:
            die("could not find the test appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow in tests/test_ui.cpp. Put the test in by hand, before the other apps tests.")
        pos = fn.start()
        ls = test[:pos].split("\n")
        k = len(ls) - 1                       # walk back over the comment lines that belong to that test
        while k > 0 and ls[k - 1].strip().startswith("//"):
            k -= 1
        pos = len("\n".join(ls[:k])) + (1 if k > 0 else 0)
        test = test[:pos] + block + test[pos:]
        out.append("edit   tests/test_ui.cpp: added the UI test for %s before the apps-tab test" % app)
    write(test_p, test, dry)

    # 6. extra edits for a networked app (or anything else that touches existing files)
    pdir = os.path.join(repo, "patches")
    if os.path.isdir(pdir):
        for p in sorted(os.listdir(pdir)):
            if not p.endswith(".patch"):
                continue
            full = os.path.join(pdir, p)
            fwd = subprocess.run(["git", "-C", fork, "apply", "--check", full], capture_output=True, text=True)
            rev = subprocess.run(["git", "-C", fork, "apply", "--check", "-R", full], capture_output=True, text=True)
            if fwd.returncode == 0:
                out.append("patch  %s" % p)
                if not dry:
                    r = subprocess.run(["git", "-C", fork, "apply", full], capture_output=True, text=True)
                    if r.returncode != 0:
                        die("could not apply patches/%s: %s" % (p, r.stderr.strip()))
            elif rev.returncode == 0:
                out.append("patch  %s (already applied)" % p)
            else:
                die("patches/%s does not apply to this fork (%s). The fork's Hop-tunes differs from the one the patch was made against: regenerate the patch against it." % (p, fwd.stderr.strip().split("\n")[0]))

    print(("DRY RUN: would do:" if dry else "Done:"))
    for o in out:
        print("  " + o)
    if not dry:
        print()
        print("Now build Hop-tunes and run the WHOLE test suite (docs/TESTING.md). Checking the registration:")
        r = subprocess.run([sys.executable, os.path.join(HERE, "check_app.py"), app, "--repo", fork])
        return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
