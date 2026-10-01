# Stand und nächste Schritte

Stand: 01.10.2026, nach der Recherche zu `userChrome.css`. Es gibt noch kein Theme – nur Doku,
Ziele, Messungen und offene Fragen. Diese Datei ist der Einstiegspunkt, um weiterzumachen.

## Was wir wollen

Aus deinen Aussagen (→ `OFFENE_FRAGEN.md`, E2):

- **Neutral:** Der Browser ist ein neutrales Fenster, in dem die Inhalte wirken. Keine Farbstiche,
  keine Verläufe.
- **Viele Tabs:** gut lesbar und kompakt. Vor allem horizontal darf nichts unnötig breit sein.
- **Keine runden Ecken:** Sie verschwenden Platz.
- **Kompaktmodus** als Grundlage.

## Was wir wissen

Belegt durch Mozillas Doku und den Firefox-157-Quellcode, Details in `docs/firefox-theming/`.

1. **Es gibt keine neue Theming-Engine.** „Nova“ ist nur das neue Design ab Firefox 157. Themes
   sind weiterhin `manifest.json`-Themes mit `theme` (hell) und `dark_theme` (dunkel).
2. **Ein Theme setzt nur Farben, Bilder und Verläufe.** Form, Abstände, Icons, Layout, UI-Dichte
   und die Akzentfarbe von Buttons/Checkboxen erreicht es nicht. Die Akzentfarbe kommt bei jedem
   Fremd-Theme vom Betriebssystem.
3. **Verläufe verschwinden von selbst**, wenn das Theme keine `images` setzt und `frame`/`toolbar`
   deckend einfärbt.
4. **Nova hat einige Keys geändert:** Der aktive Tab hat keinen Schatten mehr (`tab_selected` und
   `tab_line` setzen), die Sidebar teilt sich den Hintergrund mit der Toolbar (`sidebar`,
   `sidebar_text` setzen), `sidebar_highlight*` wirken nicht mehr. Vollständige Liste:
   `docs/firefox-theming/theme-keys.md`.
5. **Kompaktmodus** ist die Pref `browser.uidensity = 1`. Tab-Höhe in Nova: 32 px normal, 28 px
   kompakt.
6. **Tab-Breite:** Mindestbreite 76 px, über `browser.tabs.tabMinWidth` bis minimal 50 px senkbar.
   Erst wenn alle Tabs auf Mindestbreite sind, scrollt die Tableiste. Alles darunter sowie
   Innenabstand (6 px im Kompaktmodus), Maximalbreite (225 px) und Eckenradius gehen nur per
   `userChrome.css`.
7. **`theme_experiment`** (Theme mit eigenem Stylesheet) läuft nur in Nightly und Developer
   Edition – für uns keine Option.
8. **Signatur:** Release-Firefox installiert dauerhaft nur von AMO signierte Themes. Zum Entwickeln
   reicht temporäres Laden über `about:debugging`.
9. **`userChrome.css` funktioniert in 157 und braucht nur Variablen.** Gemessen in Firefox 157.0
   (headless, Wegwerf-Profil): Vier Tab-Variablen plus Mindestbreite machen die Tabs eckig und
   lückenlos, senken die Tableiste von 36 auf 28 px und verdoppeln bei 40 px Mindestbreite die
   sichtbaren Tabs (16 → 32 bei 1400 px Fensterbreite). Sechs Radius-Tokens machen auch Adressleiste
   und Buttons eckig. Jede Deklaration braucht `!important`. Details und Mechanik:
   `docs/firefox-theming/userchrome.md`.

## Was wir noch nicht wissen

- **Niemand hat es bisher angesehen.** Die Theme-Angaben stammen aus Doku und Quellcode. Die
  `userChrome.css`-Werte sind gemessen (berechnete Styles und Layout), aber nicht als Bild geprüft:
  Ob schmale, eckige Tabs lesbar bleiben und der aktive Tab erkennbar ist, zeigt nur der echte
  Browser.
- Wie sich die Variablen auf Menüs, Panels, Sidebar und vertikale Tabs auswirken – nicht gemessen.
- Wie Firefox unter Sway die System-Akzentfarbe bestimmt und ob sie zu einem neutralen Theme passt.
- Ob die Angabe „✓ unverändert“ in `theme-keys.md` für jeden Key stimmt – sie beruht auf Mozillas
  Aussage, die MDN-Referenz war zum Abrufzeitpunkt noch nicht auf Nova aktualisiert.

## Die drei Hebel

| Wunsch | Theme | `about:config` | `userChrome.css` |
| --- | --- | --- | --- |
| Neutrale Farben, keine Verläufe | ja | – | – |
| Aktiver Tab erkennbar, Text lesbar | ja | – | ja (Schriftgröße) |
| Geringere Höhe | – | `browser.uidensity = 1` | ja, weiter |
| Schmalere Tabs | – | `browser.tabs.tabMinWidth` ≥ 50 | ja, auch darunter |
| Eckige Tabs ohne Lücken | – | – | nur hier |
| Eckige Adressleiste und Buttons | – | – | nur hier |

Empfehlung: **Theme plus `userChrome.css`** (Variante C in F2). Das Theme bleibt allein nutzbar und
update-fest; das CSS ist ein kleiner Zusatz, der nach Firefox-Updates geprüft werden muss.

## Offene Entscheidungen

Vollständig in `OFFENE_FRAGEN.md`. Für den Start nötig:

| Frage | Blockiert |
| --- | --- |
| **F2** – Theme allein oder plus `userChrome.css`? | Schritt 3 |
| **F12** – Was heißt „horizontale Breite“ genau, was darf bei schmalen Tabs wegfallen? | Schritt 3 |
| **F3** – hell, dunkel oder beides? | Schritt 2 |
| **F4** – Farbrichtung: reines Grau, warm, kühl; mit oder ohne Akzent? | Schritt 2 |

Später: F5 (Nutzung), F6 (Signierung), F7 (Name, ID, Lizenz), F8 (Mindestversion), F9–F11
(Organisatorisches).

## Vorschlag für die nächsten Schritte

1. **Sofort, ohne Risiko – selbst ausprobieren:** in `about:config` `browser.uidensity` auf `1` und
   `browser.tabs.tabMinWidth` auf `50` setzen. Zeigt in zwei Minuten, wie weit die eingebauten
   Mittel tragen und was danach noch stört. Rückgängig per Rechtsklick → Zurücksetzen.
2. **Theme-Grundgerüst** (`theme/manifest.json`): neutrale Graupalette, hell und dunkel, keine
   Bilder, deckende Flächen, klar abgesetzter aktiver Tab. Kontraste nachrechnen, temporär laden,
   mit der Checkliste aus `nova-aenderungen.md` durchgehen. Braucht F3 und F4 – notfalls beginne
   ich mit reinem Grau in beiden Varianten als Diskussionsgrundlage.
3. **`userChrome.css`-Prototyp** (`userchrome/userChrome.css`): Eckenradius 0, Lücken zwischen Tabs
   entfernen, Innenabstand und Mindestbreite senken – nach `userchrome.md` allein über Variablen.
   Werte nach dem Schreiben mit `userchrome-test/variablen.py` nachmessen. Voraussetzung: `toolkit.legacyUserProfileCustomizations.stylesheets = true` und ein
   `chrome/`-Ordner im Profil. Braucht F2 und F12.
4. **Gemeinsam iterieren:** Du schaust es dir im Alltag mit vielen Tabs an, wir justieren Farben,
   Breiten und Lesbarkeit.
5. **Abschluss des ersten Themes:** Name, ID und Lizenz festlegen (F7), unlisted bei AMO signieren
   (F6), Installationsanleitung für Theme, Prefs und CSS ins README.

## Wo was steht

| Datei | Inhalt |
| --- | --- |
| `README.md` | Projektziel (englisch) |
| `CLAUDE.md` | Arbeitsregeln: Commit + Push auf `main` nach jeder bedeutsamen Änderung |
| `OFFENE_FRAGEN.md` | Offene und entschiedene Fragen |
| `docs/firefox-theming/README.md` | Index der Doku, Quellen, Lizenzen |
| `docs/firefox-theming/theme-keys.md` | Alle Theme-Keys mit Nova-Status |
| `docs/firefox-theming/nova-aenderungen.md` | Nova-Änderungen, Test-Checkliste |
| `docs/firefox-theming/kompaktmodus.md` | Dichte, Tab-Breite, Prefs |
| `docs/firefox-theming/userchrome.md` | Wie `userChrome.css` funktioniert, Variablen, Messwerte |
| `docs/firefox-theming/userchrome-test/` | Skripte, die Firefox headless starten und nachmessen |
| `docs/firefox-theming/upstream/` | Unveränderte Kopien von MDN und Firefox-Quellcode |

Hinweis: Claude am besten in `~/Github/fftheme/fftheme/` starten, nicht im Ordner darüber – sonst
wird die `CLAUDE.md` nicht automatisch geladen (F11).
