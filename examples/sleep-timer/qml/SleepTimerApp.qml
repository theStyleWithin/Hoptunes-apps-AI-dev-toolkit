// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Sleep timer: an example app from the Hop-tunes apps toolkit. It pauses the music after a time you choose.
// It uses no network and only the player (hop.player), the theme (Theme) and the shared PlainButton.
FocusScope {
    id: root
    objectName: "sleepTimerApp"

    property int remaining: 0           // seconds left; 0 means the timer is not running
    property int chosen: 0              // the minutes picked
    readonly property var choices: [[15, "15 minutes"], [30, "30 minutes"], [60, "an hour"], [90, "an hour and a half"]]

    function start(minutes) { chosen = minutes; remaining = minutes * 60 }
    function cancel() { remaining = 0 }
    function two(n) { return (n < 10 ? "0" : "") + n }
    function clock(s) { return Math.floor(s / 60) + ":" + two(s % 60) }
    function goBack() { return false }          // nothing to step back from inside this app: the host closes it

    Timer {
        id: tick
        interval: 1000; repeat: true; running: root.remaining > 0
        onTriggered: {
            root.remaining -= 1
            if (root.remaining <= 0) { root.remaining = 0; hop.player.pause() }   // time is up: the music pauses
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        width: Math.min(parent.width, 520)
        spacing: 16
        Label {
            Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap
            text: root.remaining > 0 ? "the music pauses in " + root.clock(root.remaining) : "pause the music after…"
            color: Theme.strong; font { family: Theme.font; pixelSize: Theme.fs(34); weight: Font.Light }
            objectName: "sleepTimerState"
        }
        Label {
            Layout.fillWidth: true; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.WordWrap
            visible: hop.player.hasTrack
            text: "now playing: " + hop.player.title
            color: Theme.muted; font { family: Theme.font; pixelSize: Theme.fs(16) }
        }
        Flow {
            Layout.fillWidth: true; Layout.alignment: Qt.AlignHCenter; spacing: 12
            Repeater {
                model: root.choices
                delegate: PlainButton {
                    required property var modelData
                    objectName: "sleepTimerChoice_" + modelData[0]
                    text: modelData[1]
                    primary: root.chosen === modelData[0] && root.remaining > 0
                    focusPolicy: Qt.NoFocus
                    onClicked: root.start(modelData[0])
                }
            }
        }
        PlainButton {
            objectName: "sleepTimerCancel"
            Layout.alignment: Qt.AlignHCenter
            visible: root.remaining > 0
            text: "cancel the timer"; focusPolicy: Qt.NoFocus
            onClicked: root.cancel()
        }
    }
}
