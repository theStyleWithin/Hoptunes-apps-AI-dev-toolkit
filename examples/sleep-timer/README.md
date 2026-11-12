# Example: the sleep timer

The smallest complete app: pick 15, 30, 60 or 90 minutes and the music pauses when the time is up. No network, no stored data.

* `SleepTimerApp.qml`: the screen.
* `sleep-timer.patch`: everything needed against Hop-tunes at commit `ed0fb71694ef4497fdbd142165a76b9a50867ab8` (`BASE_COMMIT.txt`): the QML file,
  the three registration edits (`qml.qrc`, `AppsView.qml`, `AppHost.qml`) and a UI test. It applies cleanly and the whole UI suite passes with it.

Try it:

```sh
git clone https://github.com/theStyleWithin/Hop-tunes && cd Hop-tunes
git checkout ed0fb71694ef4497fdbd142165a76b9a50867ab8
git apply /path/to/toolkit/examples/sleep-timer/sleep-timer.patch
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo && cmake --build build
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
./build/hop-tunes     # settings > apps settings > show the apps tab, then open "sleep timer"
python3 /path/to/toolkit/scripts/check_app.py sleeptimer --repo .
```
