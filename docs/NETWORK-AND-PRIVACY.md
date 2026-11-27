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
9. **There is no sign-in, and the gateway can only GET.** Apps are local viewing experiences: they never sign in to, follow, subscribe to, like or
   post on the outside service for the person. Kick used to have an optional sign-in (first an unofficial TV code, then the official OAuth); both
   were removed on purpose (a security scanner flagged the first, and neither was needed), and a test (`thereIsNoSignInAndTheGatewayOnlyEverGets` in
   `tests/test_net.cpp`) now pins that the gateway only ever asks for pages. `NetLimits` carries no method and no body. **One narrow exception
   exists, and it is the model for any other:** the game shelf's optional SteamGridDB cover picker sends the *person's own free API key* as an
   `Authorization` header (`NetLimits::authorization`). It is allowed for exactly one app id (`AppNet::mayAuthorize("steamgriddb")`), it is sent
   **only to that app's API host** (`www.steamgriddb.com`, never to a picture server and never on to a redirect target), it is never logged or
   listed under "contacted", and the person types it in themselves (no key is built into Hop-tunes). The key lives in a file of its own in the
   profile (`<profile>/steamgriddb.key`, 0600), never in `settings.json` and never in an exported profile. Tests pin all of it
   (`steamGridDbHostsAndTheKeyGoOnlyWhereTheyShould`). A new app that needs a key must follow the same shape, name the exact host, add the app id
   to `mayAuthorize` and add the same tests; never ship a key or client secret in the source or in a release, and never ask for a password.
10. **Say what is not guaranteed.** If the app uses an unofficial interface that can change, say so in its docs and show failures as plain
    sentences, never as a silent blank.

## How a networked app is built (copy the Internet Archive or DeviantArt app; Kick is the biggest)

* **Data class** in `src/apps/<App>Client.{h,cpp}`, a `QObject` that takes the `AppNet*`: `open()` calls `m_net->open("<app>")`, `close()`
  drops everything, every request is `m_net->get("<app>", url, callback)`, results are parsed by plain static functions (unit-tested with JSON
  or RSS fixtures) and failures end as a plain sentence in an `error` or `message` property. Read `src/apps/ArchiveClient.{h,cpp}` first (small and
  clean), then `DeviantArtClient`, then `KickClient`.
* **Pictures** come through an image provider that fetches via the gateway (`src/apps/KickImages.h`; it is generic: `new KickImageProvider(&m_appNet,
  "<app>")`, registered in `App::installImageProviders`, and QML uses `image://<app>/<escaped url>` with `cache: false`). Never
  `Image { source: "https://..." }`. A picture host the app uses is declared in `AppNet::streamSuffixesFor` (the domain and its subdomains).
* **Big files** (downloads, recordings) still go through the gateway, one slice at a time with HTTP Range requests and a per-request size
  and time limit (`NetLimits::rangeStart/rangeLength/maxBody`); fetching a whole video in one request was a real mistake (a clip came to
  973 MB). See `src/apps/OfflineDownloads.cpp` and `src/apps/Hls.cpp`; they respect the person's storage limit (`OfflineStore`).
* **Video** is fetched by the video engine, not the gateway: give it a stream address only through `openStream(url, app)` (libmpv:
  `MpvCore::openStream`, GStreamer: `GstVideoPlayer::openStream`); it accepts only https addresses of the app's declared video host
  (`AppNet::streamSuffixesFor`) and sets a generic user agent, no referrer, no cookies and a protocol whitelist. Honest limit: inside the engine
  the host cannot be enforced further.
* **Permission** is `hop.appNetAllowed("<app>")` / `hop.setAppNetAllowed("<app>", on)`; the card is in the app's own QML (`ArchiveApp.qml` has a
  compact one, `KickApp.qml` has `kickPermission`), and each app has a row in settings > apps settings (`SettingsView.qml`, for example
  `archiveNetRow`).
* **Profile lists** (follows, blocklists, favourites) are saved by `App::saveProfileSettings` (see how `kick`, `deviantart`, `archive` and
  `appsNet` are written and read in `src/App.cpp`).
* **Builds without networked apps**: everything above is behind `HOPTUNES_NET_APPS` (CMake option, on by default; an Android build without OpenSSL
  has it off too). Keep it that way, and keep a tile's `net: true` so it is left out of such builds. **CI does not build Android**: compile
  the Android build both with and without the networked apps (a member declared inside `#ifdef HOPTUNES_NET_APPS` once broke the no-network build).

### The places to touch for a new networked app

There is no table to add a row to yet: each networked app is wired by hand in the same few places. Search the source for `"archive"` (or
`m_archive`) to see every one, then do the same for your app id:

1. `src/net/AppNet.cpp`: `hostsFor("<app>")` (exact API hosts) and `streamSuffixesFor("<app>")` (picture or video hosts, as a domain whose
   subdomains are included).
2. `CMakeLists.txt`: the `src/apps/<App>Client.{h,cpp}` files in the `if(HOPTUNES_NET_APPS_ON)` source list.
3. `src/App.h` and `src/App.cpp`: the client member (`m_<app>{&m_appNet}`, inside `#ifdef HOPTUNES_NET_APPS`), a `Q_PROPERTY(QObject *<app>
   READ <app>Object CONSTANT)` so QML can reach it, the app id in the allow-list of `App::setAppNetAllowed` (and what closing it does), the
   close in `App::setAppsEnabled(false)`, `m_appNet.setAllowed("<app>", ...)` when a profile opens and `false` when it closes, the profile
   lists (load and save), and the image provider in `App::installImageProviders`.
4. `src/ui/qml/SettingsView.qml`: the permission row (`<app>NetRow`) and the line naming the sites.
5. The three registration places in `ADD-AN-APP.md`, with `net: true`.
6. Tests (below).

## Tests every networked app needs

* gateway rules: copy the cases in `tests/test_net.cpp` (`addressRules`, `nothingGoesOutUnlessAllowedAndOpen`, `redirectsStayOnTheList`,
  `closingDropsLateAnswers`, `thereIsNoSignInAndTheGatewayOnlyEverGets`) for the new app id;
* data class: fixtures through a fake transport (`FakeTransport` in `tests/test_net.cpp`), including empty, malformed and error replies;
* UI: the permission card appears first and nothing was sent before "allow"; "not now" sends nothing; taking the permission back cuts everything;
  nothing plays before a pick (`FakeKick`, `FakeArchive`, `FakeDeviantArt` in `tests/test_ui.cpp` are models); if the app sends a key (the
  SteamGridDB model): the key goes to the API host only, not to a picture server, not through a redirect, and is in no profile setting or export.
No test may touch the real network.
