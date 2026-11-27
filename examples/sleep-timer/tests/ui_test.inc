    // Sleep timer: pauses the music when its time is up (the toolkit's example app).
    void sleepTimerAppPausesTheMusic()
    {
        auto *w = window();
        w->setProperty("view", QStringLiteral("collection"));
        m_app->playSongs(0);
        QTRY_VERIFY(m_app->player()->isPlaying());
        m_app->setAppsEnabled(true);
        QTRY_VERIFY(item("subTab_apps")->isVisible());
        QVERIFY(click("subTab_apps"));
        QVERIFY(click("appTile_sleeptimer"));
        QTRY_VERIFY(item("sleepTimerApp") && item("sleepTimerApp")->isVisible());
        shot("sleep-timer-open");                                                // (a picture for the person: see HOPTUNES_UI_SHOTS in docs/TESTING.md)
        QVERIFY(click("sleepTimerChoice_15"));
        QTRY_VERIFY(item("sleepTimerCancel")->isVisible());
        QCOMPARE(item("sleepTimerApp")->property("remaining").toInt(), 15 * 60);
        QVERIFY(m_app->player()->isPlaying());                                   // the timer has only started
        item("sleepTimerApp")->setProperty("remaining", 2);                      // (do not wait 15 minutes in a test)
        QTRY_VERIFY_WITH_TIMEOUT(!m_app->player()->isPlaying(), 6000);           // time is up: the music paused
        QCOMPARE(item("sleepTimerApp")->property("remaining").toInt(), 0);
        QVERIFY(click("sleepTimerChoice_30"));                                   // a new timer, then cancelled: the music is not touched
        QVERIFY(click("sleepTimerCancel"));
        QCOMPARE(item("sleepTimerApp")->property("remaining").toInt(), 0);
        QTest::keyClick(w, Qt::Key_Escape);
        QTRY_VERIFY(!item("appHost")->property("active").toBool());
        m_app->setAppsEnabled(false);
        QVERIFY(click("subTab_music"));
    }
