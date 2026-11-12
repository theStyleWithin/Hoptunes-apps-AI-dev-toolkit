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

**C++**
* A header-only class that has `Q_OBJECT` is not run through moc unless it is listed in the target: link error "undefined reference to vtable".
  If the class declares no signals or slots of its own, drop `Q_OBJECT`.
* Never compare iterators taken from two temporary objects (`obj.value(k).toObject().constBegin()` against another `.constEnd()`): crash.
* `QList::first()` on an empty list is undefined behaviour: guard it, including inside `QTRY_COMPARE` where the list may still be empty.
* moc can choke on raw string literals (`R"(...)"`) in test files: use ordinary escaped strings.
* Android builds compile stub versions of some classes (for example `GstVideoPlayer` without GStreamer): when you add a method, add its stub or
  Android fails to link (CI does not build Android).

**libmpv option lists**
* mpv splits `demuxer-lavf-o` at commas, so `protocol_whitelist=https,tls,tcp` becomes just `https`. Give the value its length: `%34%https,tls,tcp,...`.

**Network and privacy**
* QML images and `XMLHttpRequest` bypass the gateway: use the image provider and the data class.
* A user's permission must be checked before the first request, and closing the app must drop late answers.
* Kick's addresses are unofficial and change: expect failures and show them in plain words.
* Thumbnails and avatars are WebP: Qt needs its image-format plugins (`qt6-imageformats`) to show them, otherwise a plain tile appears.

**Process**
* Run the whole suite on both Qt 6.4 and 6.8, twice.
* A test that depends on real time (a game dying, a toast) must pause or wait explicitly.
