# Adding an app directly to your fork, step by step

This is the manual way: the edits are made by hand on a branch of **your fork of Hop-tunes** (never the official repository). The recommended way keeps the app in a
repository of its own and does steps 3 and 4's edits for you with `scripts/inject_app.py` (`APP-REPOSITORY.md`); read these steps anyway, because they say what the
script does and why.

The complete, tested example is in `examples/sleep-timer/`. Follow the same five steps. (An app that needs the internet also follows
`NETWORK-AND-PRIVACY.md`; do those parts first. It is a longer job: it touches `src/net`, `src/apps` and `App.cpp` too.)

## 1. Pick an id and a name

The `id` is lower-case letters and digits (`sleeptimer`). It appears in the registry, in the host, in object names (`appTile_<id>`) and in the test.
The tile name is lower-case, one or two words.

## 2. Write the screen: `src/ui/qml/<Name>App.qml`

```qml
// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

FocusScope {
    id: root
    objectName: "myApp"
    function goBack() { return false }      // nothing to step back from: the host closes the app
    Label { anchors.centerIn: parent; text: "hello"; color: Theme.strong; font { family: Theme.font; pixelSize: Theme.fs(34) } }
}
```

Make it fit a phone-sized window as well as a computer's (`HOW-APPS-WORK.md`, "Phones").

## 3. Register it in three places

1. `src/ui/qml.qrc`: add `<file>qml/MyApp.qml</file>` next to the other app files.
2. `src/ui/qml/AppsView.qml`: add an entry **at the end** of `allApps` (after the existing apps: a new app takes the first free grid spot in registry
   order, and Hop-tunes' own grid tests expect the first app, Kick, in the first slot):
   `{ id: "myapp", name: "my app", blurb: "one plain sentence about what it does", icon: "", net: false }`
   * `blurb` is the line that pops up over the tile: say what it is and, for `net: true`, that it uses the internet.
   * `icon` is a `qrc:/images/...png` you add to `src/ui/images/` and register in `qml.qrc` (`<file alias="images/app-myapp.png">images/app-myapp.png</file>`).
     A square PNG with a transparent background, 128 to 256 px, works (the existing icons are 128 px and 256 px). It is drawn centred on the
     glass at 56 % of the tile, so keep a little empty margin; it must read on both the pale and the dark glass. Empty (`""`) shows the plain glass tile.
   * `net: true` marks an app that uses the internet: its tile says so and it is left out of builds without networked apps.
3. `src/ui/qml/AppHost.qml`: add the title to `names`, a `Component { id: myApp; MyApp { } }`, and extend the `sourceComponent` chain with
   `root.appId === "myapp" ? myApp : (...)`. (An app that leaves by itself also connects `onLeave: { root.appId = ""; root.leave() }`, like Kick.)

That is all the grid needs: the new app takes the first free spot in the person's layout the next time the grid is shown, and from then on the
person can drag it anywhere or file it in a folder. Do not edit the layout code. (The grid holds 15 tiles per page on a computer and 9 on a
phone; the existing test `appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow` expects everything on one page, so a fork with more than 15 apps updates
its `appsDot_1` expectation.)

## 4. Test it

Add a UI test to `tests/test_ui.cpp`, **immediately before** `appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow` (that is where the apps tests
live; a late-suite crash exists on Qt 6.4, see `docs/TESTING.md`). It enables apps, opens the tile (`click("appTile_myapp")`), checks the app is
visible, uses it, and closes it with Esc. Use `examples/sleep-timer/sleep-timer.patch` as the model. Call `shot("myapp-open")` once the app is
showing: that is the picture you show the person (`docs/TESTING.md` says how it is written). If the app counts time, let the test set the app's
remaining time to 1 or 2 seconds instead of waiting minutes (the sleep-timer test does exactly that), because the whole UI suite has a time limit.
If the app has its own screen, also open it in the phone-size check (`docs/TESTING.md`) and look at that picture too.

## 5. Check and build

```sh
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
python3 path/to/this-toolkit/scripts/check_app.py myapp --repo .      # a PASS only means it is registered and has a test: the whole ctest run is what proves it works
```

Then run `./build/hop-tunes`, switch on settings > apps settings > show the apps tab, and open your tile. Try dragging it to another spot and into
a folder, and close and reopen Hop-tunes: it should still be there.

## Common mistakes

* Forgetting `qml.qrc`: the app compiles but the component is "unavailable" at run time (the whole UI fails to load, which shows up as every
  UI test failing at startup).
* Putting the registry entry at the **front** of `allApps`: it takes the first grid slot and the existing test
  `appsCanBeDraggedFiledInFoldersAndRemembered` (which expects Kick in slot 0) fails. Append it.
* Forgetting the `names` entry in `AppHost.qml`: the title bar shows the raw id.
* Forgetting `objectName`s the test needs.
* A property or function named like a built-in one (`left`, `open`): see `LESSONS.md`.
* Doing network work in QML. Never; use a data class and the gateway.
* A fixed-width button wider than a phone: it widens the whole screen (`LESSONS.md`).
