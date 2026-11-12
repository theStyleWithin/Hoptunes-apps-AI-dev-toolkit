# Networked apps and Hop-tunes' privacy rules

Hop-tunes promises: **no accounts required, no telemetry, nothing phoned home, fully offline by default.** The only reason an app may use the
internet is that the person opened it, allowed it, and it says exactly what it contacts. Everything below exists to keep that promise true.
An app that does not need the internet should skip this file and never touch the network.

## The rules an agent must follow

1. **One gateway.** Only `src/net/` and `src/apps/` may use QtNetwork, sockets, `XMLHttpRequest` or `WebSocket`, and `src/apps/` code only
   through `AppNet`. The test `onlyTheGatewayTouchesTheNetwork` (`tests/test_net.cpp`) scans every source and fails otherwise.
2. **Declared sites only.** Each app lists its sites in `AppNet::hostsFor("<app>")` (exact host names). The gateway refuses anything else:
   not https, not port 443, a user name in the address, another host, a redirect to another host, more than 3 redirects.
3. **Nothing identifying.** No cookies (a jar that keeps nothing), no disk cache, no referrer, the generic user agent `Mozilla/5.0`, replies
   limited to 8 MB and 15 s. Never send Hop-tunes' version, the person's name, their profile, their library or anything else about them.
4. **It asks first.** A permission card lists the exact sites and what is sent, and offers "not now". The permission is per profile
   (guests: this session only) and can be taken back in settings > apps settings. Without it the gateway refuses every request.
5. **Only while open.** The app opens the gateway when it opens and closes it when it closes (closing drops everything still on the way and
   no late answer is ever delivered). There is a visible bar naming what is connected, with a disconnect button.
6. **User-driven.** Nothing polls in the background. Lists load when the app opens or a button is pressed; "show more" is a button.
7. **Nothing plays by itself.** A video or stream starts only after the person picked it.
8. **Local lists stay local.** Anything the person keeps (a follow list, a block list, a setting) is saved in their profile settings and
   never uploaded. An app never follows, subscribes, likes or posts on the person's behalf on the outside service.
9. **Sign-in is optional**, never needed for the app's core use, and never stored anywhere but the profile.
10. **Say what is not guaranteed.** If the app uses an unofficial interface that can change, say so in its docs and show failures as plain
    sentences, never as a silent blank.

## How a networked app is built (copy the Kick app)

* **Data class** in `src/apps/<App>Client.{h,cpp}`, a `QObject` that takes the `AppNet*`: `open()` calls `m_net->open("<app>")`, `close()`
  drops everything, every request is `m_net->get("<app>", url, callback)`, results are parsed by plain static functions (unit-tested with JSON
  fixtures) and failures end as a plain sentence in an `error` property. See `src/apps/KickClient.{h,cpp}`.
* **Pictures** come through an image provider that fetches via the gateway (`src/apps/KickImages.h`, QML uses `image://kick/<escaped url>` with
  `cache: false`). Never `Image { source: "https://..." }`.
* **Video** is fetched by the video engine, not the gateway: give it a stream address only through `openStream` (libmpv: `MpvCore::openStream`,
  GStreamer: `GstVideoPlayer::openStream`); it accepts only https addresses of the app's declared video host (`AppNet::streamSuffixesFor`) and
  sets a generic user agent, no referrer, no cookies and a protocol whitelist. Honest limit: inside the engine the host cannot be enforced further.
* **Permission** is `hop.appNetAllowed("<app>")` / `hop.setAppNetAllowed("<app>", on)`; the card is in `src/ui/qml/KickApp.qml` (`kickPermission`),
  the settings row in `SettingsView.qml` (`kickNetRow`).
* **Profile lists** are saved by `App::saveProfileSettings` (see how `kick` and `appsNet` are written and read in `src/App.cpp`).
* **Builds without networked apps**: everything above is behind `HOPTUNES_NET_APPS` (CMake option, on by default, off on Android). Keep it that
  way, and keep a tile's `net: true` so it is left out of such builds.

### Places that still assume Kick (change them when you add a second networked app)

`App::setAppNetAllowed` accepts only `"kick"`; `AppNet::hostsFor` and `streamSuffixesFor` know only `"kick"`; `MpvCore::openStream` and
`GstVideoPlayer::openStream` validate against `"kick"`; `installImageProviders` registers only `image://kick`. Generalise these deliberately
(a small table keyed by app id) rather than copy-pasting.

## Tests every networked app needs

* gateway rules: copy the cases in `tests/test_net.cpp` (`addressRules`, `nothingGoesOutUnlessAllowedAndOpen`, `redirectsStayOnTheList`,
  `closingDropsLateAnswers`) for the new app id;
* data class: fixtures through a fake transport (`FakeTransport` in `tests/test_net.cpp`), including empty, malformed and error replies;
* UI: the permission card appears first and nothing was sent before "allow"; "not now" sends nothing; disconnect cuts everything;
  nothing plays before a pick (`FakeKick` in `tests/test_ui.cpp`).
No test may touch the real network.
