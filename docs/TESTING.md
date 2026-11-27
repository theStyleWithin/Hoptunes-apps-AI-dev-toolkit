# Building and testing

```sh
# Arch / CachyOS
sudo pacman -S --needed base-devel cmake ninja qt6-base qt6-declarative qt6-imageformats taglib sqlite gstreamer gst-plugins-base gst-plugins-good gst-libav mpv
# Ubuntu / Debian: see the Hop-tunes README ("Building"); also install qt6-image-formats-plugins

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build
# a Qt 6 that is not the system one (for example 6.8 from the Qt installer): add -DCMAKE_PREFIX_PATH=/path/to/Qt/6.8.3/gcc_64 to the first command
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure      # all tests, no display needed
QT_QPA_PLATFORM=offscreen ./build/test_ui                                   # the whole UI suite (see below: not one test alone)
QT_QPA_PLATFORM=offscreen ./build/test_net                                  # the gateway and Kick data tests
```

Without `QT_QPA_PLATFORM=offscreen` the tests need a display and some abort with "no Qt platform plugin".

## UI tests (`tests/test_ui.cpp`)

The real QML UI runs offscreen. Helpers: `item("objectName")` finds an item, `click("objectName")` clicks it, `QTRY_VERIFY(...)` waits up to
5 seconds for a condition. Find things by `objectName` only, so give your controls object names. Never `QVERIFY` something that appears after a
click without `QTRY_`. Layout positions (`x`, `y`) settle a moment after items appear: wait for them with `QTRY_`.

Screenshots (for showing the person what it looks like): `HOPTUNES_UI_SHOTS=/some/dir QT_QPA_PLATFORM=offscreen ./build/test_ui` writes a
PNG for every `shot("name")` call in the tests. `HOPTUNES_FIXTURE_DIR` points at a folder holding `music/` for the richer render tests.

## Time limits, screenshots and timers

* **ctest stops the `ui` test after 300 seconds** (`CMakeLists.txt`). It normally takes about 100 to 180 seconds (about 100 on CI, more on a
  slow machine or with `HOPTUNES_UI_SHOTS` set), and a timeout shows up as "ui (Timeout)" and looks like your app broke something. Take screenshots
  by running `QT_QPA_PLATFORM=offscreen HOPTUNES_UI_SHOTS=/some/dir ./build/test_ui` directly, and run `ctest` without that variable. If ctest still
  times out, add `--timeout 600` before blaming the app.
* **A screenshot only exists if your test calls `shot("name")`** (the sleep-timer example does). Add one when the app is showing.
* **Never wait for real minutes in a test.** Let the test set the app's own remaining/elapsed property to 1 or 2 seconds (the sleep-timer test
  sets `remaining` to 2). Every second a test waits is added to a suite that already takes minutes.

## Checking an app on a phone-sized window

An app with its own screen must fit a phone. The test harness can make the window phone-sized: `window()->setProperty("forceMobile", true)`, then
`w->resize(QSize(412, 892))` (and `QSize(320, 640)` for the narrowest), wait for `w->width()`, open your app and call `shot("...")`; set
`forceMobile` back to `false` and restore the size afterwards. The existing test `phoneScreensFitTheScreen` does this for the main screens and has an
`overflowing()` helper that lists anything running past the screen edge: copy its pattern for your screen, and look at the picture. A control
with a fixed width wider than about 230 dp, or a row of controls that cannot wrap, is the usual culprit (use `Flow` or `Layout.fillWidth`).

## Rules of thumb

* **Run the whole UI suite, not one test name.** Later tests assume the state earlier ones leave, so a single test run alone can crash. Never
  run two copies of the suite at the same time on one machine (they disturb each other's timing).
* **Measure layouts only after a frame was drawn.** Headless runs may not have drawn one yet: call `window()->grabWindow()` before checking a
  size, then `QTRY_`.

* **Run the whole UI suite twice**: timing mistakes show up as one-in-two failures.
* **Test on both Qt versions if you can**: the CI `linux` job uses the distro's Qt 6.4.2; the AppImage job builds with Qt 6.8 and runs the tests
  before packaging; many developers have Qt 6.8. Qt 6.4 is stricter about some layout and property cases (see `LESSONS.md`).
* **Compile the Android build too if your change touches shared C++** (CI does not build it): with the Android SDK, NDK 26 and Qt 6.8 for
  Android (`docs/android.md` in the Hop-tunes repository), both with and without the networked apps.
* **A rare hang is known, and it is not yours:** now and then a music test that stops a song (`Player::stop`) hangs inside GStreamer until the
  300 s limit ("Test function timed out", a stack that ends in `gst_pad_stop_task`). It has passed on every re-run. Re-run the whole suite once; if it
  keeps hanging in the same place after your change, then look. Running the tests with `< /dev/null` (no terminal input) is a good habit.
* Put a new UI test **immediately before** `appsTabHoldsGlassTilesAndAppsOpenInsideTheWindow`, next to the other app tests, not at the end of the
  file: on Qt 6.4 a late-suite crash existed in the grid layout when Now playing was opened after many tests had run (the apps grid is
  paged, so a tile on a later page is not on screen until that page is shown).
* `test_player` can fail in sandboxes without audio; the CI check named `floor` is known to be red and is not caused by apps.
* Tests never use the real network. Use a fake transport.
