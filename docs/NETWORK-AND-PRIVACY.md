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
   no late answer is ever delivered). There is a visible bar naming what is connected (Kick's also shows a green / yellow / red health light).
   It has **no disconnect button on purpose**: a stray tap must not cut the connection. The permission is taken back in settings.
6. **User-driven.** Nothing polls in the background without being said. Lists load when the app opens or a button is pressed; "show more"
   is a button. The one declared exception is Kick's health light (two tiny requests about once a minute while the app is open), which the
   permission card names. A new app that polls must name that on its permission card too.
7. **Nothing plays by itself.** A video or stream starts only after the person picked it.
8. **Local lists stay local.** Anything the person keeps (a follow list, a block list, a setting) is saved in their profile settings and
   never uploaded. An app never follows, subscribes, likes or posts on the person's behalf on the outside service.
9. **Sign-in is optional**, never needed for the app's core use, and never stored anywhere but the profile. Use the service's **official**
   sign-in (OAuth with PKCE), never an unofficial "TV code" or session-token trick: Kick's first sign-in did that, scanners flagged its link,
   and it was removed. Never ship a client secret in the source or in a release: let each person register their own app on the service and
   enter its ID and secret (Kick: `docs/kick-sign-in.md` in the Hop-tunes repo, `src/apps/KickAuth.{h,cpp}`).
   **The gateway can only GET.** `NetLimits` carries no method, body or headers. The only requests that may carry a body or a token are the
   three exact sign-in requests in `AppNet::authUrlAllowed` (token POST, revoke POST, user GET with a bearer token), on the hosts in
   `AppNet::authHostsFor`; redirects are never followed for them and a test (`onlyThreeSignInRequestsMayCarryABodyOrAToken`) pins them.
   A new app with a sign-in must add its own exact requests there, with tests, and nothing broader.
10. **Say what is not guaranteed.** If the app uses an unofficial interface that can change, say so in its docs and show failures as plain
    sentences, never as a silent blank.

## How a networked app is built (copy the Kick app)

* **Data class** in `src/apps/<App>Client.{h,cpp}`, a `QObject` that takes the `AppNet*`: `open()` calls `m_net->open("<app>")`, `close()`
  drops everything, every request is `m_net->get("<app>", url, callback)`, results are parsed by plain static functions (unit-tested with JSON
  fixtures) and failures end as a plain sentence in an `error` property. See `src/apps/KickClient.{h,cpp}`.
* **Pictures** come through an image provider that fetches via the gateway (`src/apps/KickImages.h`, QML uses `image://kick/<escaped url>` with
  `cache: false`). Never `Image { source: "https://..." }`.
* **Big files** (downloads, recordings) still go through the gateway, one slice at a time with HTTP Range requests and a per-request size
  and time limit (`NetLimits::rangeStart/rangeLength/maxBody`); fetching a whole video in one request was a real mistake (a clip came to
  973 MB). See `src/apps/OfflineDownloads.cpp` and `src/apps/Hls.cpp`; they respect the person's storage limit (`OfflineStore`).
* **Video** is fetched by the video engine, not the gateway: give it a stream address only through `openStream` (libmpv: `MpvCore::openStream`,
  GStreamer: `GstVideoPlayer::openStream`); it accepts only https addresses of the app's declared video host (`AppNet::streamSuffixesFor`) and
  sets a generic user agent, no referrer, no cookies and a protocol whitelist. Honest limit: inside the engine the host cannot be enforced further.
* **Permission** is `hop.appNetAllowed("<app>")` / `hop.setAppNetAllowed("<app>", on)`; the card is in `src/ui/qml/KickApp.qml` (`kickPermission`),
  the settings row in `SettingsView.qml` (`kickNetRow`).
* **Profile lists** are saved by `App::saveProfileSettings` (see how `kick` and `appsNet` are written and read in `src/App.cpp`).
* **Builds without networked apps**: everything above is behind `HOPTUNES_NET_APPS` (CMake option, on by default, off on Android). Keep it that
  way, and keep a tile's `net: true` so it is left out of such builds.

### Places that still assume Kick (change them when you add a second networked app)

`App::setAppNetAllowed` accepts only `"kick"`; `AppNet::hostsFor`, `streamSuffixesFor`, `authHostsFor` and `authUrlAllowed` know only `"kick"`; `MpvCore::openStream` and
`GstVideoPlayer::openStream` validate against `"kick"`; `installImageProviders` registers only `image://kick`. Generalise these deliberately
(a small table keyed by app id) rather than copy-pasting.

## Tests every networked app needs

* gateway rules: copy the cases in `tests/test_net.cpp` (`addressRules`, `nothingGoesOutUnlessAllowedAndOpen`, `redirectsStayOnTheList`,
  `closingDropsLateAnswers`) for the new app id;
* data class: fixtures through a fake transport (`FakeTransport` in `tests/test_net.cpp`), including empty, malformed and error replies;
* UI: the permission card appears first and nothing was sent before "allow"; "not now" sends nothing; taking the permission back cuts everything;
  nothing plays before a pick (`FakeKick` in `tests/test_ui.cpp`); if the app has a sign-in: the gateway matrix, the flow against a fake
  transport (a plain socket plays the browser), refresh and failure paths, and that signing out forgets the tokens.
No test may touch the real network.
