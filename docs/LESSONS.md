# Lessons: mistakes already made once

Each of these cost real time while the Kick app was built. Check this list when something odd happens.

**QML**
* Property and function names must not clash with built-ins: a `readonly property bool left` inside an item failed with "Cannot override FINAL
  property"; a C++ `Q_PROPERTY` named `open` hid the method `open()` ("is not a function"). Pick specific names.
* Property names cannot start with an upper-case letter.
* A QML component used in `qml.qrc` must be listed there, or the whole UI fails to load (every UI test then fails at startup).
* `import HopTunes.Video 1.0` is needed to use `VideoSurface`.
* Items that appear and disappear inside a `RowLayout`/`GridLayout` can crash Qt 6.4: prefer a constant model and `visible:`.
* Round pictures: Qt Quick cannot clip to a rounded rectangle without extra effects; the Kick app paints the corners over the picture instead.
* A clicked button keeps keyboard focus: Space then "clicks" it again. Use `focusPolicy: Qt.NoFocus` on buttons in screens that use keys.
* The default `ComboBox` is white and clashes with the theme: use a small `Menu` instead.
* Only one `Component.onDestruction` per item (a second one is an error that breaks the whole page).
* Do not animate `Layout.*` attached properties (Qt 6.4 clipped controls): animate a plain `real` (a `reveal`) and bind the layout to it.
* An item whose `visible` flips inside a layout can stay 0x0 on a slow or headless run. Give it a size that changes with it
  (`Layout.minimumHeight: visible ? 120 : 0`), and in tests draw a frame first (`window()->grabWindow()`).
* `ApplicationWindow.contentItem` is not the `QQuickWindow` root; code that reparents an item into "the window" must use the right one.
* **A stray `;` after a property group's closing brace** (`anchors { ... };` or `font { ... };` on one line) is a parse error that stops the whole
  page loading: write the group's `}` and the next property on separate lines, or leave the `;` out.
* **A plain integer as a `Repeater` or `ListView` `model` resets every delegate whenever the number changes** (the apps grid destroyed the very tile
  being dragged when a page was added). Use a `ListModel` and change it incrementally, or keep the model constant.
* **Statements after a call that changes a model, inside a delegate's own handler, may never run**, because the delegate was rebuilt by the change:
  clear the state that hides the control first, then change the model.
* A property named `data` clashes with the built-in `Item.data`; name it something specific.
* A `delegate:` (or any `Component` property) of an **inline `component X: ComboBox`** must be written as `delegate: Component { ... }`; a bare item is
  "neither the same as the latter nor a sub-class of it". And `Component.onCompleted: for (...) ...` needs braces: `{ for (...) ... }`.
* **A control with a fixed width wider than the phone widens everything around it** (a 360 wide settings button pushed the whole page past the edge of a
  320 dp phone and failed the "fits the screen" test). Keep fixed widths to about 230 or less, and wrap rows in a `Flow`.
* **Qt 6.4 `GridLayout` can crash when items come and go**, and a rare local crash was seen in `phoneCollectionStaysCompactWhileScanning`: for a grid
  whose contents change, use `GridView`, a `Flow` or a `ListView`.
* Moving a playing `VideoOutput` into another parent (full screen, pop-out) can leave it black on some Android phones. Kick rebuilds the
  picture once the window settles (`KickPlayer.refreshPicture`); try video features on a real phone, the desktop tests cannot show this.

**C++**
* A header-only class that has `Q_OBJECT` is not run through moc unless it is listed in the target: link error "undefined reference to vtable".
  If the class declares no signals or slots of its own, drop `Q_OBJECT`.
* Never compare iterators taken from two temporary objects (`obj.value(k).toObject().constBegin()` against another `.constEnd()`): crash.
* The `QTRY_*` test macros `return` void: do not use them inside a lambda that returns a value.
* In a test class, helper structs need `private:` / `private slots:` markers around them or moc loses track.
* `QList::first()` on an empty list is undefined behaviour: guard it, including inside `QTRY_COMPARE` where the list may still be empty.
* moc (really CMake's AUTOMOC scan) chokes on raw string literals (`R"(...)"`) in test files, above all ones that contain `//` (any URL) or
  unbalanced quotes: the symptom is "No relevant classes found" and then a link error "undefined reference to vtable for Test...". Use ordinary
  escaped strings, or build JSON with `QJsonObject`.
* **Android: `slots` is a Qt macro** (do not name a C++ variable `slots`), and a class member declared inside `#ifdef HOPTUNES_NET_APPS` that code
  outside it uses breaks the Android build without networked apps. CI does not build Android: compile it yourself, both ways.
* `QUrl::toString()` shows `%20` as a space: compare `QUrl` objects (`QCOMPARE(url, QUrl(expected))`), not strings, when a test checks an address.
* Android builds compile stub versions of some classes (for example `GstVideoPlayer` without GStreamer): when you add a method, add its stub or
  Android fails to link (CI does not build Android).

**libmpv option lists**
* mpv splits `demuxer-lavf-o` at commas, so `protocol_whitelist=https,tls,tcp` becomes just `https`. Give the value its length: `%34%https,tls,tcp,...`.

**Network and privacy**
* QML images and `XMLHttpRequest` bypass the gateway: use the image provider and the data class.
* A user's permission must be checked before the first request, and closing the app must drop late answers.
* Kick's addresses are unofficial and change: expect failures and show them in plain words.
* A security scanner flagged Kick's unofficial TV-code sign-in link (one engine of ninety-odd, and the same engine also flagged kick.com itself).
  Whether or not it was right, the lesson was not "do the sign-in the official way" but "the apps do not need one": Kick's sign-in (the TV code first,
  then the official OAuth) was removed completely, and the gateway now only ever GETs. Do not bring a sign-in back; if a feature truly needs the
  person's own key, follow rule 9 of `NETWORK-AND-PRIVACY.md` (one host, typed in by the person, kept outside the profile settings and exports).
* Never fetch a whole video in one request (a clip came to 973 MB): use HTTP Range slices and the storage limit.
* Thumbnails and avatars are WebP: Qt needs its image-format plugins (`qt6-imageformats`) to show them, otherwise a plain tile appears.

**Process**
* A new app's registry entry goes at the **end** of `allApps`: the first entry takes the first grid slot, and Hop-tunes' grid test expects Kick
  there (the first version of the sleep-timer example for the new grid failed that test exactly this way).
* Run the whole suite on both Qt 6.4 and 6.8, twice.
* A failure in an old, unrelated test can be a real race (a count read before an asynchronous update): make it wait (`QTRY_`), never skip it.
* Say plainly what you could not try (a phone, a real account, a real server) in the pull request and in the docs.
* **Do not trust "it passed once".** Hop-tunes had a flaky drive test in the library that turned out to be a real bug (a folder that vanished between
  two calls made an empty path match every row, so a scan forgot the whole library): find the cause before re-running.
* A test that exercises `positionViewAtEnd` or a model reset can be thrown back by a *later* rebuild that was already queued (a `Timer` or
  `Qt.callLater`): wait for the final state (`QTRY_VERIFY(list.count >= n)`) before you act, and keep the scroll position across a rebuild in the app.
* A test that depends on real time (a game dying, a toast) must pause or wait explicitly.
