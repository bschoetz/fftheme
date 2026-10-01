# Stand und nächste Schritte

Stand: 01.10.2026. Es gibt eine `userChrome.css` (Form) und ein erstes Theme (Farben), beide nach
deinen Einstellungen im Simulator. Das Theme ist noch nicht signiert und hält deshalb nur bis zum
nächsten Neustart (F6). Diese Datei ist der Einstiegspunkt, um weiterzumachen.

## Was wir wollen

Aus deinen Aussagen (→ `OFFENE_FRAGEN.md`, E2):

- **Neutral:** Der Browser ist ein neutrales Fenster, in dem die Inhalte wirken. Keine Farbstiche,
  keine Verläufe.
- **Viele Tabs:** gut lesbar und kompakt. Vor allem horizontal darf nichts unnötig breit sein.
- **Nur leichte Eckenrundung** an den Tabs (E3; zuerst hieß es „keine runden Ecken“).
- **Erkennbare Trennung zwischen inaktiven Tabs** (E3).
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
   Edition – für uns keine Option. In Firefox 157.0 Release getestet: Das Stylesheet wird nicht
   angewendet, auch nicht mit `extensions.experiments.enabled = true`. Es gibt damit keinen Weg, die
   `userChrome.css` als Add-on zu verteilen.
8. **Signatur:** Release-Firefox installiert dauerhaft nur von AMO signierte Themes. Zum Entwickeln
   reicht temporäres Laden über `about:debugging`.
9. **`userChrome.css` funktioniert in 157 und braucht nur Variablen.** Gemessen in Firefox 157.0
   (headless, Wegwerf-Profil): Vier Tab-Variablen plus Mindestbreite machen die Tabs eckig und
   lückenlos, senken die Tableiste von 36 auf 28 px und verdoppeln bei 40 px Mindestbreite die
   sichtbaren Tabs (16 → 32 bei 1400 px Fensterbreite). Sechs Radius-Tokens machen auch Adressleiste
   und Buttons eckig. Jede Deklaration braucht `!important`. Details und Mechanik:
   `docs/firefox-theming/userchrome.md`.
10. **Ein Theme schaltet Nova nicht ab.** Mit unserem Theme bleiben `browser.nova.enabled = true`,
    Tab-Radius 24 px und Leistenhöhe 36 px (gemessen). Es verschwinden nur Novas Farbmerkmale:
    Verlauf im Hintergrund, Verlaufsrahmen am aktiven Tab, lila Akzentfarbe.

## Was es gibt

`theme/manifest.json` – das Theme mit deinen Farben aus dem Simulator (01.10.2026): Leiste und
Navigationsleiste `#1e1e1e`, aktiver Tab `#472200` mit Rand `#e66100`, Adressfeld `#000000`, Text
`#d4d4d4` / `#e6e6e6` / `#ffffff`. Keine Bilder, also kein Verlauf. Nur eine dunkle Variante (F3).
`web-ext lint` ohne Befund; alle Kontraste über den Mindestwerten. Headless mit der
`userChrome.css` zusammen geladen: Farben greifen, der aktive Tab bekommt die Linie in `tab_line`.

**Laden:** `about:debugging#/runtime/this-firefox` → „Temporäres Add-on laden…“ →
`theme/manifest.json`. Das hält bis zum Neustart. Dauerhaft geht es in deinem Firefox nur signiert:
Die Arch-Version verlangt die Signatur fest (`MOZ_REQUIRE_SIGNING`), `xpinstall.signatures.required
= false` ändert daran nichts (getestet). → F6

Nicht gesetzt und damit Firefox überlassen: Sidebar, Menüs/Panels, Icons, Neuer-Tab-Seite,
Trennlinien der Toolbar.

`userchrome/userChrome.css` – dein Zwischenstand vom 01.10.2026, im Simulator eingestellt:

- Radius 8 px für Tabs, Adressfeld und Buttons (Firefox: 24 px).
- Tableiste 28 px hoch statt 36 px: kein Abstand über und unter den Tabs.
- Lücke zwischen Tabs 3 px statt 4 px, Mindestbreite 68 px statt 76 px.
- Schrift der Tab-Titel 15 px, Schließen-Knopf 22 px, Text blendet über 1,5 em aus.
- 1 px breite, 18 px hohe Trennlinie zwischen inaktiven Tabs in 50 % der Textfarbe; keine Linie am
  aktiven und am überfahrenen Tab.
- Zeilenhöhe 1,3. Du hattest 1 eingestellt; damit schneidet Firefox Unterlängen ab (g, p, y). 1,3
  ändert sonst nichts, weil die Tab-Höhe von `--tab-min-height` kommt.

Im Simulator ist das zusammen mit den Theme-Farben die Variante „Aktueller Stand“.

Die Datei ist per Symlink in dein Profil eingehängt (`<Profil>/chrome/userChrome.css`), die Pref
`toolkit.legacyUserProfileCustomizations.stylesheets` steht auf `true`; laut dir greift die Form im
echten Fenster. Änderungen wirken nach einem Neustart. Abschalten: Pref auf `false` und neu starten.

`userchrome/simulator.html` – Tab-Simulator zum Durchspielen von Varianten. Eine einzelne
HTML-Datei, die du im Browser öffnest: links eine nachgebaute Tableiste, rechts Regler für alles,
was wir per `userChrome.css` und Theme ansteuern können. Sie erzeugt die passende `userChrome.css`
und die Theme-Farben zum Kopieren und merkt sich benannte Varianten. Tab-Maße stimmen mit Firefox
157.0 überein (`userchrome-test/simulator.py`: 0 Abweichungen über 0,6 px, Standard und ein Stil
mit allen Reglern verändert, je 6, 12 und 40 Tabs). Nicht gegen Firefox geprüft: die Farben eigener
Themes, Hover, Dichte „normal“.

Die `userChrome.css` selbst ist nur headless geprüft (Screenshots mit dunklem Firefox-Theme, 12
und 40 Tabs). Nicht
geprüft: dein echtes Fenster unter Sway, angeheftete Tabs, Tab-Gruppen, Tabs beim Ziehen,
vertikale Tabs (die Regeln greifen dort absichtlich nicht).

## Was wir noch nicht wissen

- **Wie das Theme in deinem echten Fenster aussieht.** Geprüft ist es nur headless. Die Form
  (`userChrome.css`) hast du gesehen, die Farben noch nicht.
- Wie Theme und CSS unter Windows und macOS aussehen (Fensterknöpfe in der Tableiste, andere
  Systemschrift) – nicht getestet.
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

Wir arbeiten mit Theme plus `userChrome.css` (Variante C in F2; von dir benutzt, aber noch nicht
ausdrücklich entschieden).

## Offene Entscheidungen

Vollständig in `OFFENE_FRAGEN.md`.

| Frage | Blockiert |
| --- | --- |
| **F7** – Name, ID, Lizenz | Signatur, Weitergabe |
| **F6** – Theme signieren (AMO-Konto nötig)? | dauerhafte Nutzung des Themes |
| **F13** – Wie geben wir Theme und CSS weiter? | Installationsskript, Releases |
| **F3** – hell, dunkel oder beides? | Weitergabe (bisher nur dunkel) |
| **F2** – Theme plus `userChrome.css` bestätigen | nichts, nur festhalten |

Später: F4 (Farbrichtung, vorläufig E4), F5 (Nutzung), F12 (was bei schmalen Tabs wegfallen darf),
F8–F11.

## Nächste Schritte

1. **Du: Theme ansehen.** `about:debugging#/runtime/this-firefox` → „Temporäres Add-on laden…“ →
   `theme/manifest.json`. Im Alltag mit vielen Tabs ansehen, auch Menüs, Sidebar, angeheftete Tabs.
   Was stört, im Simulator ändern oder mir sagen.
2. **Du: F7 und F6 entscheiden.** Name, ID und Lizenz festlegen, AMO-Konto mit API-Schlüssel
   anlegen. Danach signiere ich das Theme „unlisted“; erst dann bleibt es nach einem Neustart.
3. **Claude, ohne weitere Entscheidung möglich: Theme vervollständigen.** Vorschlag für die Bereiche,
   die bisher Firefox überlassen sind (Sidebar, Menüs/Panels, Icons, Hover der Buttons,
   Neuer-Tab-Seite, Trennlinien), abgeleitet aus deinen zehn Farben; Kontraste rechnen, headless
   laden, Checkliste aus `nova-aenderungen.md`. Außerdem prüfen, dass das Theme ohne CSS ordentlich
   aussieht.
4. **Helle Variante** (F3), sobald die dunkle steht – nötig für die Weitergabe.
5. **Weitergabe vorbereiten** (F13): CSS nach `chrome/fftheme/fftheme.css` mit `@import`-Zeile
   umbauen, Installationsskript für Linux, Optionen über Prefs, Anleitung ins README. Danach
   PowerShell-Skript für Windows und die Messskripte in GitHub Actions.
6. **Erstes Release:** signierte `.xpi`, CSS-Paket und Skripte auf GitHub.

## Wo was steht

| Datei | Inhalt |
| --- | --- |
| `README.md` | Projektziel (englisch) |
| `CLAUDE.md` | Arbeitsregeln: Commit + Push auf `main` nach jeder bedeutsamen Änderung |
| `OFFENE_FRAGEN.md` | Offene und entschiedene Fragen |
| `theme/manifest.json` | Das Theme: Farben |
| `userchrome/userChrome.css` | Form der Tabs, Trennlinien, Radius von Adressfeld und Buttons |
| `userchrome/simulator.html` | Tab-Simulator: Varianten durchspielen, CSS und Theme-Farben erzeugen |
| `docs/firefox-theming/README.md` | Index der Doku, Quellen, Lizenzen |
| `docs/firefox-theming/theme-keys.md` | Alle Theme-Keys mit Nova-Status |
| `docs/firefox-theming/nova-aenderungen.md` | Nova-Änderungen, Test-Checkliste |
| `docs/firefox-theming/kompaktmodus.md` | Dichte, Tab-Breite, Prefs |
| `docs/firefox-theming/userchrome.md` | Wie `userChrome.css` funktioniert, Variablen, Messwerte |
| `docs/firefox-theming/userchrome-test/` | Skripte, die Firefox headless starten und nachmessen |
| `docs/firefox-theming/upstream/` | Unveränderte Kopien von MDN und Firefox-Quellcode |

Hinweis: Claude am besten in `~/Github/fftheme/fftheme/` starten, nicht im Ordner darüber – sonst
wird die `CLAUDE.md` nicht automatisch geladen (F11).
