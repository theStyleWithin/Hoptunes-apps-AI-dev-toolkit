# Building and testing

```sh
# Arch / CachyOS
sudo pacman -S --needed base-devel cmake ninja qt6-base qt6-declarative qt6-imageformats taglib sqlite gstreamer gst-plugins-base gst-plugins-good gst-libav mpv
# Ubuntu / Debian: see the Hop-tunes README ("Building"); also install qt6-image-formats-plugins

cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure      # all tests, no display needed
QT_QPA_PLATFORM=offscreen ./build/test_ui                                   # the UI tests alone
QT_QPA_PLATFORM=offscreen ./build/test_net                                  # the gateway and Kick data tests
```

Without `QT_QPA_PLATFORM=offscreen` the tests need a display and some abort with "no Qt platform plugin".

## UI tests (`tests/test_ui.cpp`)

The real QML UI runs offscreen. Helpers: `item("objectName")` finds an item, `click("objectName")` clicks it, `QTRY_VERIFY(...)` waits up to
5 seconds for a condition. Find things by `objectName` only, so give your controls object names. Never `QVERIFY` something that appears after a
click without `QTRY_`. Layout positions (`x`, `y`) settle a moment after items appear: wait for them with `QTRY_`.

Screenshots (for showing the person what it looks like): `HOPTUNES_UI_SHOTS=/some/dir QT_QPA_PLATFORM=offscreen ./build/test_ui` writes a
PNG for every `shot("name")` call in the tests. `HOPTUNES_FIXTURE_DIR` points at a folder holding `music/` for the richer render tests.

## Rules of thumb

* **Run the whole UI suite twice**: timing mistakes show up as one-in-two failures.
* **Test on both Qt versions if you can**: CI uses the distro's Qt 6.4; many developers have Qt 6.8. Qt 6.4 is stricter about some layout and
  property cases (see `LESSONS.md`).
* Put a new UI test **early** in the file, next to the other app tests: on Qt 6.4 a late-suite crash existed in the grid layout when Now playing
  was opened after many tests had run.
* `test_player` can fail in sandboxes without audio; the CI check named `floor` is known to be red and is not caused by apps.
* Tests never use the real network. Use a fake transport.
