#!/usr/bin/env python3
"""Makes a NEW repository folder for one Hop-tunes app, with a working hello-world app in it.

Usage:  python3 new_app_repo.py <app-id> --name "my app" --dir <where to create it> [--type SleepTimer] [--blurb "one plain sentence"] [--holder "Your Name"]

The folder has the layout docs/APP-REPOSITORY.md describes: app.json, qml/<Name>App.qml, tests/ui_test.inc, README.md, .gitignore. The person makes it a git
repository of their own (`git init`, push to their own GitHub), the agent builds the real app in it, and scripts/inject_app.py puts the app into the
person's fork of Hop-tunes to build and test. Nothing here touches Hop-tunes.
"""
import argparse
import json
import os
import re
import sys
from datetime import date

QML = '''// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright (C) {year} {holder}
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// {name}: an app for Hop-tunes. Replace this with the real screen. It may use the theme (Theme), the player (hop.player) and the shared components
// described in docs/HOW-APPS-WORK.md of the Hop-tunes apps toolkit.
FocusScope {{
    id: root
    objectName: "{id}App"
    function goBack() {{ return false }}      // nothing to step back from inside the app: the host closes it (Esc and the back button)

    ColumnLayout {{
        anchors.centerIn: parent
        width: Math.min(parent.width, 520)
        spacing: 16
        Label {{
            Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap
            text: "hello from {name}"
            color: Theme.strong; font {{ family: Theme.font; pixelSize: Theme.fs(34); weight: Font.Light }}
            objectName: "{id}Hello"
        }}
    }}
}}
'''

TEST = '''    // {name}: opens from its tile in the apps grid and closes with Esc. (Replace this with tests of what the app really does.)
    void {fn}AppOpensAndCloses()
    {{
        auto *w = window();
        w->setProperty("view", QStringLiteral("collection"));
        m_app->setAppsEnabled(true);
        QTRY_VERIFY(item("subTab_apps")->isVisible());
        QVERIFY(click("subTab_apps"));
        QVERIFY(click("appTile_{id}"));
        QTRY_VERIFY(item("{id}App") && item("{id}App")->isVisible());
        shot("{id}-open");                                                       // a picture for the person (HOPTUNES_UI_SHOTS, docs/TESTING.md)
        QTest::keyClick(w, Qt::Key_Escape);
        QTRY_VERIFY(!item("appHost")->property("active").toBool());
        m_app->setAppsEnabled(false);
        QVERIFY(click("subTab_music"));
    }}
'''

README = '''# {name}

An app for [Hop-tunes](https://github.com/theStyleWithin/Hop-tunes) (a local-first music player), made with the
[Hop-tunes apps toolkit](https://github.com/theStyleWithin/Hoptunes-apps-AI-dev-toolkit). This is an independent app and is not made or endorsed by the
author of Hop-tunes.

{blurb}

## Put it into your own Hop-tunes

Fork Hop-tunes on GitHub, clone **your fork**, then (the toolkit is the folder next to this one, or wherever you keep it):

```sh
python3 /path/to/toolkit/scripts/inject_app.py /path/to/this/folder --fork /path/to/your/Hop-tunes-fork
cd /path/to/your/Hop-tunes-fork
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo && cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
./build/hop-tunes        # settings > apps settings > show the apps tab
```

Run the `inject_app.py` line again whenever you change this app: it updates your fork in place.

## Licence

GPL-3.0-or-later, like Hop-tunes (an app that is put into Hop-tunes becomes part of it). Add the licence text as `LICENSE` (copy it from the Hop-tunes
repository) before you publish this repository.
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("app_id")
    ap.add_argument("--name", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--blurb", default="")
    ap.add_argument("--holder", default="the app's author")
    ap.add_argument("--type", default="", help="the QML type name without the App suffix, like SleepTimer (default: made from the id)")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]{1,30}", a.app_id):
        print("FAIL  the app id must be lower-case letters and digits, starting with a letter (for example: sleeptimer)")
        return 1
    name = a.name.strip().lower()
    if not name or len(name) > 30 or '"' in name or "\\" in name:
        print("FAIL  --name: a short lower-case name, no quotes")
        return 1
    blurb = a.blurb.strip() or "an app for Hop-tunes: replace this with one plain sentence about what it does"
    if '"' in blurb or "\\" in blurb or "\n" in blurb:
        print("FAIL  --blurb: one line, no double quotes or backslashes")
        return 1
    if os.path.exists(a.dir) and os.listdir(a.dir):
        print("FAIL  %s already exists and is not empty" % a.dir)
        return 1
    base = a.type.strip()
    if base and not re.fullmatch(r"[A-Z][A-Za-z0-9]*", base):
        print("FAIL  --type: letters and digits, starting with a capital (for example SleepTimer); the file will be <type>App.qml")
        return 1
    if base.endswith("App"):
        base = base[:-3]
    typ = (base or (a.app_id[0].upper() + a.app_id[1:])) + "App"
    fn = a.app_id
    os.makedirs(os.path.join(a.dir, "qml"))
    os.makedirs(os.path.join(a.dir, "tests"))
    os.makedirs(os.path.join(a.dir, "images"))
    manifest = {"id": a.app_id, "name": name, "blurb": blurb, "net": False, "qml": typ + ".qml", "icon": "", "leaves": False}
    with open(os.path.join(a.dir, "app.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    ctx = dict(id=a.app_id, name=name, year=date.today().year, holder=a.holder, fn=fn, blurb=blurb)
    with open(os.path.join(a.dir, "qml", typ + ".qml"), "w", encoding="utf-8") as f:
        f.write(QML.format(**ctx))
    with open(os.path.join(a.dir, "tests", "ui_test.inc"), "w", encoding="utf-8") as f:
        f.write(TEST.format(**ctx))
    with open(os.path.join(a.dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(README.format(**ctx))
    with open(os.path.join(a.dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("build/\n*.user\n")
    with open(os.path.join(a.dir, "images", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write("")
    print("Made %s: app.json, qml/%s.qml, tests/ui_test.inc, README.md" % (a.dir, typ))
    print("Next: build the real app there, then:  python3 scripts/inject_app.py %s --fork <your fork of Hop-tunes>" % a.dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
