# How Hop-tunes apps work today

This describes the code as of Hop-tunes 1.15.0. Paths are relative to the Hop-tunes repository. (If a path here does not exist in the Hop-tunes
you have, the docs are older than your Hop-tunes: read the source and trust that.)

## What the person sees

The **apps** tab is the last tab of the collection (music, videos, games, pictures, audiobooks, ebooks, podcasts, **apps**). It is off until the
person switches it on (settings > apps settings > "show the apps tab"), and guests never keep it. It shows the apps as a **grid of glass tiles**:
five across and three down on a computer (15 per page), three across and three down on a phone (9 per page), with page dots on top and a
"custom themes" button (the page is pale in the light theme and dark in the dark theme, or the person lays a picture of their own behind it).

The person arranges their own grid, and **your app does not have to do anything for that**:

* **Drag a tile anywhere** (even to another page: drop on a page dot, or hold at the edge). A mouse can always drag; on a touch screen a long
  press (or the *arrange* button) starts arranging. Dropping on another tile swaps places. The layout is remembered per profile, separately for
  the wide and the phone layouts.
* **Folders**: a clear, glassy tile that apps are dragged into (or filed with *move to a folder...* in an app's right-click menu). Clicking a
  folder opens it inside the grid. A folder can be renamed, coloured, or given a picture from the person's photos.
* A **new app** (one you add to the registry) takes the first free spot by itself the first time the grid is shown, in registry order (so add yours at the end of `allApps`). An app
  that is removed from the registry disappears from the layout (and from any folder); its spot becomes free.
* A short line (the entry's `blurb`) pops up when the pointer rests on a tile (or on a long press), unless the person hid the descriptions in
  settings. Write it for that: what the app is, and that it uses the internet if it does.

## The pieces

| What | Where | Role |
|---|---|---|
| the apps tab | `src/ui/qml/CollectionView.qml` | shows the `apps` tab (desktop) or pill (phone, last) only when `hop.appsEnabled` is true |
| the setting | `App::appsEnabled` (`src/App.cpp`), settings > "apps settings" in `src/ui/qml/SettingsView.qml` | per profile, **off by default**; guests never keep it |
| the registry | `allApps` in `src/ui/qml/AppsView.qml` | one entry per app: `id`, `name`, `blurb`, `icon`, `net` |
| the grid | `src/ui/qml/AppsView.qml` (`AppFace`, `FolderFace`, drag handling, menus, folder view) | draws the tiles and takes the drags; you do not edit it to add an app |
| where things are | `src/core/AppsLayout.{h,cpp}`, `hop.appsLayout`, saved by `App` as the profile setting `appsLayout` | which slot each app and folder is in; folders; `setKnownApps(ids)` is called with the registry's ids |
| the glass | `src/ui/images/app-tile.png` (light look; `qrc:/images/app-tile.png`) and the `DarkGlass` item in `AppsView.qml` (dark look) | the tile's background; the app's icon is drawn on top, centred, 56 % of the tile |
| the host | `src/ui/qml/AppHost.qml` | opens an app full-area inside the Hop-tunes window, with a back button and Esc |
| the app itself | `src/ui/qml/<Name>App.qml` | any QML `Item`; listed in `src/ui/qml.qrc` |
| the network gateway | `src/net/AppNet.{h,cpp}` | the only way an app reaches the internet (see `NETWORK-AND-PRIVACY.md`) |

## Life of an app

1. The person switches apps on (settings > apps settings). The tab appears after podcasts.
2. Tiles come from `allApps`. A tile with `net: true` says "uses the internet" and is left out of builds without networked apps
   (`hop.netAppsBuilt` is false only in builds made without `HOPTUNES_NET_APPS`, and in an Android build made without OpenSSL).
3. Clicking a tile (a tap, never the end of a drag) emits `openApp(id)`; `CollectionView` calls `appHost.open(id)`.
4. `AppHost` sets its `appId`; its `Loader` instantiates the component whose id matches (the `sourceComponent` chain in `AppHost.qml`).
5. **Esc and the back button** call `AppHost.close()`. If your app's root item has `function goBack()` and it returns `true`, the app handled it
   (stepped back inside itself) and stays open; otherwise the host closes the app and the person lands back on the apps grid. Return `false`
   when there is nothing to step back from.
6. Closing destroys the app (the `Loader` becomes inactive): do your cleanup in `Component.onDestruction`.
7. Leaving the collection tab, switching apps off, or taking a network permission back also closes the app.

The music keeps playing while an app is open, and the mini player stays.

### Optional hooks on an app's root item

`AppHost` looks for these on the loaded app (none is required):

* `function goBack()` returning `true` when it stepped back inside itself (Esc and the back button).
* `readonly property string nowPlayingTitle` and `nowPlayingSub`: while no song is playing, the mini player shows these (a stream or a
  video the app is playing, for example).
* `readonly property Item videoSlot`: where the app wants the stream's picture (the main window's stream dock sits over it).
* `readonly property bool collapsible` plus `property bool collapsed` and `function toggleCollapse()`: the round arrow at the top right pulls
  the app's own menu up out of the way (Kick's "curtain").
* `function openSearch()` returning `true` and `readonly property bool searchActive`: on a phone the bottom **search** button searches inside the
  app while it is open instead of searching the music.
* `readonly property bool theatre`: when `true` the host hides its title bar and the window's own bars (navigation, mini player), so the app
  has the whole window. Kick uses it for a sideways phone watching a stream.

## Phones

The same app screen runs on a phone-sized window (`Theme.compact` is true there: the shorter side is under 600 dp), where the grid is three
across and the person can still arrange it. An app that has its own screen must fit at 412 x 892 and 320 x 640 dp (see `TESTING.md` for how the
tests check that): use `Layout` with `fillWidth`, wrap rows that can get long in a `Flow`, and never give a button a fixed width wider than
about 230 (a 320 dp phone is only about 290 wide inside the page padding, and one too-wide control widens everything around it). Use `Theme.compact` for a phone-only variant instead of a second app.

## What an app's QML may use

* **`Theme`** (singleton): colours (`Theme.bg`, `Theme.panel`, `Theme.text`, `Theme.text2`, `Theme.muted`, `Theme.dim`, `Theme.strong`,
  `Theme.accent`, `Theme.ink`, `Theme.line`, `Theme.border`, `Theme.hover`, `Theme.danger`), `Theme.font`, `Theme.fs(px)` for scaled font sizes,
  `Theme.pad` for page padding, `Theme.reduceMotion`, `Theme.compact` (phone-sized window), `Theme.light` (the light theme). Use these instead of
  hard-coded colours so light and dark themes both work.
* **Shared components** in `src/ui/qml/`: `PlainButton` (outlined button; `primary: true` fills it), `AlbumArt`, `Icon`, `LiveChat` (the pretend
  chat), `Visualizer`, and the video surface (`VideoSurface`, a C++ item: `import HopTunes.Video 1.0`; the Android app plays video through Qt
  Multimedia instead, see `AndroidVideoSurface.qml`). Kick also has reusable pieces worth copying or reusing: `KickPlayer.qml` (a stream or a
  local file with a seek meter, full screen and pop-out) and `SeekMeter.qml`. Look at the file list before writing a new widget.
* **`hop`** (the `App` object, context property): the player (`hop.player`: `title`, `artist`, `album`, `playing`, `hasTrack`, `position`, and the
  slots `play()`, `pause()`, `toggle()`, `stop()`, `next()`, `previous()`), the profile (`hop.profile`, `hop.guest`), settings, the song analysis
  (`hop.audio.want("my-app", true)` starts it and `false` releases it; never leave it on after closing), the game controller (`hop.gamepad`), the
  scores (`hop.submitScore(game, score, extra)` and `hop.gameScores(game)`).
* **Pausing and resuming the music.** `hop.player.play()` does nothing when there is no current track (`hop.player.hasTrack` is false), and
  `pause()` is harmless on a paused player. An app that pauses the music should remember whether it was `hop.player.playing` first, resume only
  music it paused itself (never start music the person did not have on), and give the music back in `Component.onDestruction` if it closes
  while it is holding it paused.
* Keep to lower-case, plain sentences in the UI, like the rest of Hop-tunes.

## The apps that exist today (good ones to read)

| App | Network | What to learn from it |
|---|---|---|
| **Kick** (`KickApp.qml`, `src/apps/KickClient.*`) | yes | the biggest: browse and watch live streams, downloads and recordings, a pretend chat, the permission card, the stream dock, the phone pop-out |
| **Internet Archive** (`ArchiveApp.qml`, `src/apps/ArchiveClient.*`) | yes | search and details through plain JSON, playing music and video, reading a book from a temporary copy, a curator shown first, the permission card |
| **DeviantArt** (`DeviantArtApp.qml`, `src/apps/DeviantArtClient.*`) | yes | public RSS feeds, an image grid, local favourites and blocklists, an 18+ switch that starts off |
| **neko cafe** (`NekoCafeApp.qml`, `src/game/`) | no | an offline game: its own sprites, score handling, no data leaving the profile |
| **sleep timer** (this toolkit, `examples/sleep-timer/`) | no | the smallest complete app |

## Style conventions

* Object names for everything a test must find: `objectName: "myAppButton"`. Tests look items up by `objectName` only. Tiles are always
  `appTile_<id>`.
* Buttons inside an app use `focusPolicy: Qt.NoFocus` when the app handles keys itself (a focused button would steal Space).
* Pictures and data from the internet never come from QML directly (`Image { source: "https://..." }` is forbidden); see `NETWORK-AND-PRIVACY.md`.
* Every new source file starts with `// SPDX-License-Identifier: GPL-3.0-or-later`.
