# Adding an app, step by step

The complete, tested example is in `examples/sleep-timer/`. Follow the same five steps. (An app that needs the internet also follows
`NETWORK-AND-PRIVACY.md`; do those parts first.)

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

## 3. Register it in three places

1. `src/ui/qml.qrc`: add `<file>qml/MyApp.qml</file>` next to the other app files.
2. `src/ui/qml/AppsView.qml`: add an entry to `allApps`:
   `{ id: "myapp", name: "my app", blurb: "one plain sentence about what it does", icon: "", net: false }`
   (`icon` is a `qrc:/images/...png` you add to `src/ui/images/` and `qml.qrc`; empty shows the plain glass tile.
   Icons are square, about 256 px, drawn in the purple-to-blue gradient style of the existing ones.)
3. `src/ui/qml/AppHost.qml`: add the title to `names`, a `Component { id: myApp; MyApp { } }`, and extend the `sourceComponent` chain with
   `root.appId === "myapp" ? myApp : (...)`.

## 4. Test it

Add a UI test to `tests/test_ui.cpp`, **immediately before** `appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow` (that is where the apps tests
live; a late-suite crash exists on Qt 6.4, see `docs/TESTING.md`). It enables apps, opens the tile, checks the app is visible, uses it, and closes
it with Esc. Use `examples/sleep-timer/sleep-timer.patch` as the model. Call `shot("myapp-open")` once the app is showing: that is the picture you
show the person (`docs/TESTING.md` says how it is written). If the app counts time, let the test set the app's remaining time to 1 or 2 seconds
instead of waiting minutes (the sleep-timer test does exactly that), because the whole UI suite has a time limit.

## 5. Check and build

```sh
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
python3 path/to/this-toolkit/scripts/check_app.py myapp --repo .      # a PASS only means it is registered and has a test: the whole ctest run is what proves it works
```

Then run `./build/hop-tunes`, switch on settings > apps settings > show the apps tab, and open your tile.

## Common mistakes

* Forgetting `qml.qrc`: the app compiles but the component is "unavailable" at run time (the whole UI fails to load, which shows up as every
  UI test failing at startup).
* Forgetting `objectName`s the test needs.
* A property or function named like a built-in one (`left`, `open`): see `LESSONS.md`.
* Doing network work in QML. Never; use a data class and the gateway.
