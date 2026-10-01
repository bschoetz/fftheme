# Stand und nächste Schritte

Stand: 01.10.2026. Form und Farben stehen in einer Datei, `userchrome/userChrome.css`, nach deinen
Einstellungen im Simulator. Die Farben liegen über dem eingebauten Theme „Firefox Dunkel“ (E5). Die
Datei ist in dein Profil eingehängt und überlebt Neustarts. Diese Datei hier ist der Einstiegspunkt,
um weiterzumachen.

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

11. **Farben gehen auch per `userChrome.css`.** Ein Block mit Firefox' Farbvariablen über „Firefox
    Dunkel“ ergibt headless dasselbe Bild wie ein eigenes Theme mit denselben Farben: Leiste,
    Tabs, Navigationsleiste, Adressfeld, Icons und Hover stimmen überein. Unterschiede: keine 1 px
    dunkle Linie zwischen Tableiste und Navigationsleiste; Menüs, Sidebar, Akzentfarbe und Fokusring
    bleiben die von „Firefox Dunkel“.

## Was es gibt

`userchrome/userChrome.css` – dein Stand vom 01.10.2026, im Simulator eingestellt.

Form:

- Radius 8 px für Tabs, Adressfeld und Buttons (Firefox: 24 px).
- Tableiste 28 px hoch statt 36 px: kein Abstand über und unter den Tabs.
- Lücke zwischen Tabs 3 px statt 4 px, Mindestbreite 68 px statt 76 px.
- Schrift der Tab-Titel 15 px, Schließen-Knopf 22 px, Text blendet über 1,5 em aus.
- 1 px breite, 18 px hohe Trennlinie zwischen inaktiven Tabs in 50 % der Textfarbe; keine Linie am
  aktiven und am überfahrenen Tab.
- Fokusring 1 px statt 2 px: Rahmen des fokussierten Adressfelds und Tastaturfokus an Buttons.
- Tab-Vorschau beim Überfahren 3 px unter dem Tab (`#tab-preview-panel`); ohne das klebt sie am Tab,
  weil der Abstand über und unter den Tabs fehlt.
- Zeilenhöhe 1,3. Du hattest 1 eingestellt; damit schneidet Firefox Unterlängen ab (g, p, y). 1,3
  ändert sonst nichts, weil die Tab-Höhe von `--tab-min-height` kommt.

Farben (eigener Block am Ende der Datei, gilt nur mit „Firefox Dunkel“):

- Leiste und Navigationsleiste `#1e1e1e`, kein Verlauf.
- Aktiver Tab `#391b00` mit Rand `#c64600`, Text `#ffffff`; inaktive Tabs Text `#d4d4d4`.
- Adressfeld `#000000`, Rahmen `#5a5a5a`, Text `#e6e6e6`.
- Fokusring neutral `#d4d4d4` (Adressfeld beim Tippen, Buttons bei Tastaturbedienung), Kontrast 11,2.
  Orange markiert damit nur den aktiven Tab.
- Icons, Schließen-Kreuz, Hover und Plaketten im Adressfeld neutral statt lila getönt.
- Kontraste: Text 11,2 und 15,8; Rand des aktiven Tabs 3,4; Trennlinie 3,8. Der Rahmen des
  Adressfelds liegt mit 2,4 unter dem Mindestwert von 3 – von dir so gewählt (01.10.2026); mit Fokus
  wird er hell (11,2).

Nicht überschrieben und damit weiter „Firefox Dunkel“: Menüs und Panels, Sidebar, Neuer-Tab-Seite
und die Akzentfarbe (Nova-Lila, z. B. Checkboxen, Schalter, Ladeanzeige).

Im Simulator ist das die Variante „Aktueller Stand“; sie erzeugt exakt diese Datei.

Die Datei ist per Symlink in dein Profil eingehängt (`<Profil>/chrome/userChrome.css`), die Pref
`toolkit.legacyUserProfileCustomizations.stylesheets` steht auf `true`. Voraussetzung für die
Farben: unter Add-ons und Themes ist „Dunkel“ ausgewählt. Änderungen wirken nach einem Neustart.
Abschalten: Pref auf `false` und neu starten.

`theme/manifest.json` – geparkt. Ein eigenes Theme mit denselben Farben; es wird seit E5 nicht mehr
benutzt und nicht mehr gepflegt, weil es unsigniert nur bis zum Neustart hält.

`userchrome/simulator.html` – Tab-Simulator zum Durchspielen von Varianten. Eine einzelne
HTML-Datei, die du im Browser öffnest: links eine nachgebaute Tableiste, rechts Regler für alles,
was wir ansteuern können, Form wie Farben. Sie erzeugt die passende `userChrome.css` zum Kopieren
und merkt sich benannte Varianten. Tab-Maße und Farben stimmen mit Firefox 157.0 überein
(`userchrome-test/simulator.py`: 0 Abweichungen, Standard und ein Stil mit allen Reglern und Farben
verändert, je 6, 12 und 40 Tabs). Nicht gegen Firefox geprüft: Hover, Dichte „normal“.

Die Form hast du im echten Fenster gesehen. Die Farben per CSS sind nur headless geprüft
(Screenshots mit „Firefox Dunkel“, 12 Tabs). Nicht geprüft: inaktives Fenster, privates Fenster,
angeheftete Tabs, Tab-Gruppen, Tabs beim Ziehen, vertikale Tabs (die Tab-Regeln greifen dort
absichtlich nicht).

## Was wir noch nicht wissen

- **Wie die Farben in deinem echten Fenster aussehen.** Geprüft sind sie nur headless.
- Wie das CSS unter Windows und macOS aussieht (Fensterknöpfe in der Tableiste, andere
  Systemschrift) – nicht getestet.
- Wie sich die Variablen auf Menüs, Panels, Sidebar und vertikale Tabs auswirken – nicht gemessen.
- Wie Firefox unter Sway die System-Akzentfarbe bestimmt und ob sie zu einem neutralen Theme passt.
- Ob die Angabe „✓ unverändert“ in `theme-keys.md` für jeden Key stimmt – sie beruht auf Mozillas
  Aussage, die MDN-Referenz war zum Abrufzeitpunkt noch nicht auf Nova aktualisiert.

## Offene Entscheidungen

Vollständig in `OFFENE_FRAGEN.md`.

| Frage | Blockiert |
| --- | --- |
| **F7** – Name und Lizenz | Weitergabe |
| **F3** – auch eine helle Variante (Block über „Firefox Hell“)? | Weitergabe an Leute mit hellem Firefox |
| Akzentfarbe (Checkboxen, Schalter): Nova-Lila lassen oder auf dein Orange setzen? | nichts, Optik |

Später: F4 (Farbrichtung, vorläufig E4), F5 (Nutzung), F12 (was bei schmalen Tabs wegfallen darf),
F8–F11.

## Nächste Schritte

1. **Du: Firefox neu starten und ansehen.** Voraussetzung: Theme „Dunkel“ ausgewählt. Im Alltag mit
   vielen Tabs ansehen, auch Menüs, Sidebar, inaktives und privates Fenster. Was stört, im Simulator
   ändern oder mir sagen.
2. **Restbereiche entscheiden:** Menüs, Sidebar, Neuer-Tab-Seite, Akzentfarbe. Was davon
   neutral oder orange werden soll, kommt als weitere Variablen in den Farbblock; vorher messen.
3. **Weitergabe vorbereiten:** CSS nach `chrome/fftheme/fftheme.css` mit `@import`-Zeile umbauen,
   Installationsskript für Linux (legt die Datei ab, setzt die Pref in `user.js`), Anleitung ins
   README inklusive „Theme Dunkel auswählen“. Danach PowerShell-Skript für Windows.
4. **Optionen über Prefs** (`@media -moz-pref("fftheme.…")`): Farben, Trennlinien, schmale Tabs
   einzeln schaltbar.
5. **Absichern:** Messskripte in GitHub Actions gegen neue Firefox-Versionen laufen lassen; auf
   Windows und macOS ansehen.
6. **Erstes Release** auf GitHub: CSS-Paket und Skripte.

## Wo was steht

| Datei | Inhalt |
| --- | --- |
| `README.md` | Projektziel (englisch) |
| `CLAUDE.md` | Arbeitsregeln: Commit + Push auf `main` nach jeder bedeutsamen Änderung |
| `OFFENE_FRAGEN.md` | Offene und entschiedene Fragen |
| `userchrome/userChrome.css` | Alles: Form der Tabs, Trennlinien, Radien und die Farben |
| `theme/manifest.json` | Geparkt: eigenes Theme mit denselben Farben, nicht mehr benutzt |
| `userchrome/simulator.html` | Tab-Simulator: Varianten durchspielen, die `userChrome.css` erzeugen |
| `docs/firefox-theming/README.md` | Index der Doku, Quellen, Lizenzen |
| `docs/firefox-theming/theme-keys.md` | Alle Theme-Keys mit Nova-Status |
| `docs/firefox-theming/nova-aenderungen.md` | Nova-Änderungen, Test-Checkliste |
| `docs/firefox-theming/kompaktmodus.md` | Dichte, Tab-Breite, Prefs |
| `docs/firefox-theming/userchrome.md` | Wie `userChrome.css` funktioniert, Variablen, Messwerte |
| `docs/firefox-theming/userchrome-test/` | Skripte, die Firefox headless starten und nachmessen |
| `docs/firefox-theming/upstream/` | Unveränderte Kopien von MDN und Firefox-Quellcode |

Hinweis: Claude am besten in `~/Github/fftheme/fftheme/` starten, nicht im Ordner darüber – sonst
wird die `CLAUDE.md` nicht automatisch geladen (F11).
