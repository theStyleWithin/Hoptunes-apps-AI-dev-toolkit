#!/usr/bin/env python3
"""Checks that an app was added to Hop-tunes the way docs/ADD-AN-APP.md says.

Usage:  python3 check_app.py <app-id> --repo <path to the Hop-tunes source>

It reads source files only (it builds nothing and runs nothing) and prints PASS / FAIL lines. It catches forgotten registrations (registry, host,
qrc), a missing licence header, an app QML file that obviously reaches for the network, an app whose test never opens its tile or never closes it,
and audio analysis that is never released. It is a help, not a judge and not a security boundary: a clean result means "registered and has a test",
NOT "works". The whole `ctest` run is the proof. It cannot see network use outside the app's own QML file (the real guard is the test
`onlyTheGatewayTouchesTheNetwork`).
"""
import argparse
import os
import re
import subprocess
import sys


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app_id")
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    root, app = args.repo, args.app_id
    results = []
    notes = []

    def check(ok, what, hint=""):
        results.append((bool(ok), what, hint))

    if not re.fullmatch(r"[a-z][a-z0-9]{1,30}", app):
        print("FAIL the app id must be lower-case letters and digits (for example: sleeptimer)")
        return 1

    apps_view = read(os.path.join(root, "src/ui/qml/AppsView.qml"))
    host = read(os.path.join(root, "src/ui/qml/AppHost.qml"))
    qrc = read(os.path.join(root, "src/ui/qml.qrc"))
    ui_test = read(os.path.join(root, "tests/test_ui.cpp"))
    if apps_view is None or host is None or qrc is None or ui_test is None:
        print("FAIL this does not look like the Hop-tunes source (src/ui/qml/AppsView.qml, AppHost.qml, qml.qrc or tests/test_ui.cpp missing): check --repo")
        return 1

    # 0. the app belongs in the person's own fork, never in the official repository (docs/YOUR-OWN-BUILD.md)
    try:
        origin = subprocess.run(["git", "-C", root, "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        origin = ""
    if re.search(r"github\.com[:/]+thestylewithin/hop-tunes(\.git)?/?$", origin, re.I):
        print("WARN  origin of this clone is the OFFICIAL Hop-tunes repository (%s). Do not push, open pull requests or tag there:" % origin)
        print("      fork Hop-tunes on GitHub, work in your fork, and keep the app there (docs/YOUR-OWN-BUILD.md).")
        print()

    # 1. the registry entry
    entry = re.search(r'\{\s*id:\s*"%s"\s*,([^}]*)\}' % re.escape(app), apps_view)
    check(entry, "registry: an entry with id \"%s\" in allApps (src/ui/qml/AppsView.qml)" % app, "add it as described in docs/ADD-AN-APP.md step 3")
    body = entry.group(1) if entry else ""
    check(re.search(r'name:\s*"[^"]+"', body), "registry: the entry has a name", 'name: "my app"')
    check(re.search(r'blurb:\s*"[^"]{8,}"', body), "registry: the entry has a one-sentence blurb", 'blurb: "what it does in one plain sentence"')
    uses_net = bool(re.search(r"net:\s*true", body))
    check(re.search(r"net:\s*(true|false)", body), "registry: the entry says whether it uses the internet (net: true or false)", "net: false")

    # 2. the host
    names_map = re.search(r'names:\s*\(\{([^}]*)\}\)', host)
    check(names_map and re.search(r'"%s"\s*:' % re.escape(app), names_map.group(1)),
          "host: the app id is in the `names` map of AppHost.qml", 'names: ({ "kick": "kick", "%s": "my app" })' % app)
    check(re.search(r'appId\s*===\s*"%s"' % re.escape(app), host),
          "host: the sourceComponent chain of AppHost.qml loads a component for this app", 'root.appId === "%s" ? myApp : ...' % app)
    comp_types = re.findall(r'Component\s*\{\s*id:\s*\w+\s*;\s*(\w+)\s*\{', host)
    qml_name = None
    for t in comp_types:
        src = read(os.path.join(root, "src/ui/qml/%s.qml" % t))
        if src and ('objectName: "%s' % app in src.lower() or app in t.lower()):
            qml_name = t
    if qml_name is None and comp_types:
        # fall back: a component whose type name contains the app id
        for t in comp_types:
            if app in t.lower():
                qml_name = t
    check(qml_name, "host: a Component in AppHost.qml loads a QML type for this app", "Component { id: myApp; MyApp { } }")

    # 3. the QML file
    qml_src = None
    if qml_name:
        qml_path = os.path.join(root, "src/ui/qml/%s.qml" % qml_name)
        qml_src = read(qml_path)
        check(qml_src is not None, "file: src/ui/qml/%s.qml exists" % qml_name)
        check(("qml/%s.qml" % qml_name) in qrc, "qrc: qml/%s.qml is listed in src/ui/qml.qrc" % qml_name, "<file>qml/%s.qml</file>" % qml_name)
        if qml_src:
            check("SPDX-License-Identifier: GPL-3.0-or-later" in qml_src, "licence: the file starts with the SPDX GPL-3.0-or-later header")
            check(re.search(r'objectName:\s*"', qml_src), "tests: the app has objectNames a test can find")
            if not uses_net:
                bad = [w for w in ("XMLHttpRequest", "WebSocket", "https://", "http://", "Qt.openUrlExternally", "QtNetwork") if w in qml_src]
                check(not bad, "offline: the app has net: false and its QML uses no network words", "found: " + ", ".join(bad))
            else:
                check(not re.search(r'source:\s*"https?://', qml_src) and "XMLHttpRequest" not in qml_src and "WebSocket" not in qml_src,
                      "network: the QML loads nothing from the internet itself (pictures through the image provider, data through the data class)")
    else:
        check(False, "file: could not find the app's QML file (see the host check above)")

    # 4. a UI test: the function that opens this app's tile must wait for it (QTRY_) and close it with Esc
    tile = ("appTile_%s" % app)
    at = ui_test.find(tile)
    check(at >= 0, "test: tests/test_ui.cpp opens the tile %s" % tile, "see examples/sleep-timer/sleep-timer.patch for a model")
    if at >= 0:
        start = ui_test.rfind("\n    void ", 0, at)
        end = ui_test.find("\n    }\n", at)
        body = ui_test[start:end if end > 0 else len(ui_test)]
        check("QTRY_VERIFY" in body, "test: that test waits for the app to appear with QTRY_VERIFY (never a bare QVERIFY after a click)")
        check("Key_Escape" in body, "test: that test closes the app with Esc", "QTest::keyClick(w, Qt::Key_Escape)")
        if "shot(" not in body:
            notes.append('your test has no shot("name") call, so there is no screenshot to show the person (docs/TESTING.md)')
    # the song analysis is shared: whoever starts it must release it
    if qml_src and re.search(r'hop\.audio\.want\([^)]*true', qml_src):
        check(re.search(r'hop\.audio\.want\([^)]*false', qml_src), "audio: the app releases the song analysis it started (hop.audio.want(..., false))", "do it in Component.onDestruction")
    if qml_src and "Component.onDestruction" not in qml_src:
        notes.append("the app has no Component.onDestruction: fine unless it starts timers, holds the music paused, or asks for the song analysis")

    # 5. a networked app also declares its sites and has gateway tests
    if uses_net:
        net_cpp = read(os.path.join(root, "src/net/AppNet.cpp")) or ""
        net_test = read(os.path.join(root, "tests/test_net.cpp")) or ""
        check(('"%s"' % app) in net_cpp, "network: AppNet.cpp declares this app's sites (hostsFor)", "docs/NETWORK-AND-PRIVACY.md")
        check(('"%s"' % app) in net_test, "network: tests/test_net.cpp tests this app's gateway rules", "copy the cases for the new app id")
        card = any(("kickPermission" in (read(os.path.join(root, "src/ui/qml", f)) or "")) for f in os.listdir(os.path.join(root, "src/ui/qml")) if f.endswith(".qml"))
        check(card, "network: a permission card exists to copy (KickApp.qml)", "")

    failed = 0
    for ok, what, hint in results:
        if ok:
            print("PASS  " + what)
        else:
            failed += 1
            print("FAIL  " + what + (("   -> " + hint) if hint else ""))
    for n in notes:
        print("NOTE  " + n)
    print()
    print("%d checks, %d failed" % (len(results), failed))
    print("(a clean result means registered and has a test, not that it works: run the whole ctest)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
