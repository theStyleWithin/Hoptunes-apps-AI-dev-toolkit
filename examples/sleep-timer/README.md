# Example: the sleep timer

The smallest complete app: pick 15, 30, 60 or 90 minutes and the music pauses when the time is up. No network, no stored data.

* `SleepTimerApp.qml`: the screen.
* `sleep-timer.patch`: everything needed against Hop-tunes at commit `1523fd4b5d162f2ce25c8018e4b07d379c29b8ff` (`BASE_COMMIT.txt`): the QML file,
  the three registration edits (`qml.qrc`, `AppsView.qml`, `AppHost.qml`) and a UI test. It applies cleanly and the whole UI suite passes with it.

Try it:

```sh
git clone https://github.com/<you>/Hop-tunes && cd Hop-tunes      # your fork (the example is only for trying it out; it is not added to official Hop-tunes)
git checkout 1523fd4b5d162f2ce25c8018e4b07d379c29b8ff
git apply /path/to/toolkit/examples/sleep-timer/sleep-timer.patch
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo && cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
./build/hop-tunes     # settings > apps settings > show the apps tab, then open "sleep timer"
python3 /path/to/toolkit/scripts/check_app.py sleeptimer --repo .
```
