# How Hop-tunes apps work today

This describes the code as of Hop-tunes 1.10.0. Paths are relative to the Hop-tunes repository.

## The pieces

| What | Where | Role |
|---|---|---|
| the apps tab | `src/ui/qml/CollectionView.qml` | shows an `apps` tab (desktop) or pill (phone, after podcasts) only when `hop.appsEnabled` is true |
| the setting | `App::appsEnabled` (`src/App.cpp`), settings > "apps settings" in `src/ui/qml/SettingsView.qml` | per profile, **off by default**; guests never keep it |
| the registry | `allApps` in `src/ui/qml/AppsView.qml` | one entry per app: `id`, `name`, `blurb`, `icon`, `net` |
| the glass tile | `src/ui/images/app-tile.png` (registered in `src/ui/qml.qrc` as `qrc:/images/app-tile.png`) | every app's tile; the app's icon is drawn on top |
| the host | `src/ui/qml/AppHost.qml` | opens an app full-area inside the Hop-tunes window, with a back button and Esc |
| the app itself | `src/ui/qml/<Name>App.qml` | any QML `Item`; listed in `src/ui/qml.qrc` |
| the network gateway | `src/net/AppNet.{h,cpp}` | the only way an app reaches the internet (see `NETWORK-AND-PRIVACY.md`) |

## Life of an app

1. The person switches apps on (settings > apps settings). The tab appears after podcasts.
2. Tiles come from `allApps`. A tile with `net: true` says "uses the internet" and is left out of builds without networked apps
   (`hop.netAppsBuilt` is false only in builds made without `HOPTUNES_NET_APPS`; the Android app has networked apps since 1.10.0).
3. Clicking a tile emits `openApp(id)`; `CollectionView` calls `appHost.open(id)`.
4. `AppHost` sets its `appId`; its `Loader` instantiates the component whose id matches (`sourceComponent` chain in `AppHost.qml`).
5. **Esc and the back button** call `AppHost.close()`. If your app's root item has `function goBack()` and it returns `true`, the app handled it
   (stepped back inside itself) and stays open; otherwise the host closes the app. Return `false` when there is nothing to step back from.
6. Closing destroys the app (the `Loader` becomes inactive): do your cleanup in `Component.onDestruction`.
7. Leaving the collection tab, switching apps off, or taking a network permission back also closes the app.

The music keeps playing while an app is open, and the mini player stays.

### Optional hooks on an app's root item

`AppHost` looks for these on the loaded app (none is required):

* `function goBack()` returning `true` when it stepped back inside itself (Esc and the back button).
* `readonly property bool collapsible` plus `property bool collapsed` and `function toggleCollapse()`: the round arrow at the top right pulls
  the app's own menu up out of the way (Kick's "curtain").
* `function openSearch()` returning `true` and `readonly property bool searchActive`: on a phone the bottom **search** button searches inside the
  app while it is open instead of searching the music.
* `readonly property bool theatre`: when `true` the host hides its title bar and the window's own bars (navigation, mini player), so the app
  has the whole window. Kick uses it for a sideways phone watching a stream.

## What an app's QML may use

* **`Theme`** (singleton): colours (`Theme.bg`, `Theme.panel`, `Theme.text`, `Theme.text2`, `Theme.muted`, `Theme.dim`, `Theme.strong`,
  `Theme.accent`, `Theme.ink`, `Theme.line`, `Theme.border`, `Theme.hover`, `Theme.danger`), `Theme.font`, `Theme.fs(px)` for scaled font sizes,
  `Theme.pad` for page padding, `Theme.reduceMotion`. Use these instead of hard-coded colours so light and dark themes both work.
* **Shared components** in `src/ui/qml/`: `PlainButton` (outlined button; `primary: true` fills it), `AlbumArt`, `LiveChat` (the pretend chat),
  `Visualizer`, and the video surfaces (`VideoSurface`, import `HopTunes.Video 1.0`). Kick also has reusable pieces worth copying or reusing:
  `KickPlayer.qml` (a stream or a local file with a seek meter, full screen and pop-out) and `SeekMeter.qml`. Look at the file list before
  writing a new widget.
* **`hop`** (the `App` object, context property): the player (`hop.player`: `title`, `artist`, `album`, `playing`, `hasTrack`, `position`, and the
  slots `play()`, `pause()`, `toggle()`, `stop()`, `next()`, `previous()`), the profile (`hop.profile`, `hop.guest`), settings, the song analysis
  (`hop.audio.want("my-app", true)` starts it and `false` releases it; never leave it on after closing), the game controller (`hop.gamepad`), the
  scores (`hop.submitScore(game, score, extra)` and `hop.gameScores(game)`).
* **Pausing and resuming the music.** `hop.player.play()` does nothing when there is no current track (`hop.player.hasTrack` is false), and
  `pause()` is harmless on a paused player. An app that pauses the music should remember whether it was `hop.player.playing` first, resume only
  music it paused itself (never start music the person did not have on), and give the music back in `Component.onDestruction` if it closes
  while it is holding it paused.
* Keep to lower-case, plain sentences in the UI, like the rest of Hop-tunes.

## Style conventions

* Object names for everything a test must find: `objectName: "myAppButton"`. Tests look items up by `objectName` only.
* Buttons inside an app use `focusPolicy: Qt.NoFocus` when the app handles keys itself (a focused button would steal Space).
* Pictures and data from the internet never come from QML directly (`Image { source: "https://..." }` is forbidden); see `NETWORK-AND-PRIVACY.md`.
* Every new source file starts with `// SPDX-License-Identifier: GPL-3.0-or-later`.
