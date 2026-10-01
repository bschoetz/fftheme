# `userChrome.css`

`userChrome.css` ist ein Stylesheet im Firefox-Profil, das Firefox auf seine **eigene Oberfläche**
anwendet. Die Firefox-Oberfläche ist selbst ein Dokument aus HTML/XUL und CSS; `userChrome.css`
hängt dort eigene Regeln an. Damit ist alles erreichbar, was CSS kann – Form, Abstände, Größen,
Ausblenden –, also genau das, was ein Static Theme nicht kann.

Es ist **keine API**. Selektoren und Variablen sind Firefox-Interna und können sich mit jedem
Update ändern.

Belege: Firefox-Quellcode (Branch `release`), das CSS aus dem installierten Firefox 157.0
(`/usr/lib/firefox/browser/omni.ja`) und eigene Messungen mit den Skripten in
[`userchrome-test/`](userchrome-test/). Was nur aus Community-Quellen stammt oder ungeprüft ist,
steht unter [Nicht belegt](#nicht-belegt).

## Einrichtung

1. `about:config` → `toolkit.legacyUserProfileCustomizations.stylesheets` auf `true`.
2. Im Profilordner (`about:support` → „Profilordner“) einen Ordner `chrome` anlegen.
3. Darin die Datei `userChrome.css` anlegen (Schreibweise genau so).
4. Firefox neu starten.

Auf diesem System liegt das Profil unter `~/.config/mozilla/firefox/<profil>/`, nicht unter
`~/.mozilla/`.

`about:support` zeigt, ob die Pref aktiv ist und welche der beiden Dateien `userChrome.css` /
`userContent.css` gefunden wurden (`Troubleshoot.sys.mjs`, Feld `legacyUserStylesheets`).

## Wie Firefox die Datei lädt

Quelle: `layout/style/GlobalStyleSheetCache.cpp` (`InitFromProfile`) und `dom/base/Document.cpp`
(`FillStyleSetUserAndUASheets`).

| Verhalten | Beleg |
| --- | --- |
| Ohne die Pref wird die Datei gar nicht gesucht. Standardwert `false` | Quelle; Messung: mit Pref `false` greift keine einzige Regel |
| Gelesen wird `<Profil>/chrome/userChrome.css`, einmal beim Start | Quelle; Messung: eine Änderung an der Datei im laufenden Betrieb wirkt nicht |
| Im Fehlerbehebungsmodus (`firefox --safe-mode`) wird sie nicht geladen | Quelle. Das ist der Notausgang, falls das CSS die Oberfläche unbenutzbar macht |
| Die Datei darf ein Symlink sein | Messung |
| Sie gilt für alle Dokumente der Browser-Oberfläche (Chrome-Docshell). Für alle anderen Dokumente gilt stattdessen `userContent.css` aus demselben Ordner | Quelle |
| Sie wird als **User-Stylesheet** geladen, nicht als Teil von Firefox' eigenem CSS | Quelle (`StyleOrigin::User`) |
| Ein Fehler beim Laden wird in die Browser-Konsole geschrieben | Quelle (`FailureAction::LogToConsole`) |

Die Pref gibt es seit Firefox 69. Grund war die Startzeit: Firefox sollte nicht bei jedem Start
nach Dateien suchen, die fast niemand hat
([Bug 1541233](https://bugzilla.mozilla.org/show_bug.cgi?id=1541233)).

## Kaskade: warum überall `!important` steht

Firefox' eigene Regeln sind Author-Stylesheets, `userChrome.css` ist ein User-Stylesheet. Nach der
CSS-Kaskade verliert eine normale User-Deklaration gegen jede Author-Deklaration – unabhängig von
Spezifität und Reihenfolge. Mit `!important` kehrt sich das um: User-`!important` schlägt Author,
auch Author-`!important` und Inline-Styles.

Gemessen in Firefox 157.0 (`mechanik.py`):

| Regel in `userChrome.css` | Ergebnis |
| --- | --- |
| `.tab-background { border-radius: 0; }` | wirkungslos, bleibt 24px |
| `:root { --tab-inline-padding: 1px; }` | wirkungslos, bleibt 6px |
| `.tab-background { margin-block: 1px !important; }` | wirkt |
| `:root { --tab-overflow-clip-margin: 0px !important; }` | wirkt |
| `#tabbrowser-tabs { --tab-min-width-pref: 30px !important; }` | wirkt, obwohl Firefox den Wert per Inline-Style setzt |

Faustregel: Jede Deklaration, die mit einer Firefox-Regel konkurriert, braucht `!important`.
Cascade Layers (`@layer`), in denen Firefox seine Design-Tokens definiert, spielen dafür keine
Rolle – Origin geht vor Layer.

Ein `@namespace` am Dateianfang, wie es viele alte Anleitungen zeigen, ist nicht nötig: Die
Test-Datei hat keins und trifft XUL- wie HTML-Elemente.

## Variablen statt Selektoren

Firefox steuert Maße und Formen über CSS-Variablen (Design-Tokens). Wer eine Variable überschreibt,
ändert alle Stellen, die sie benutzen, und muss die Struktur der Oberfläche nicht kennen. Das ist
robuster als Regeln auf einzelne Elemente.

Variablen für horizontale Tabs, Nova, kompakt, gemessen in 157.0:

| Variable | Wert | Definiert in | Wirkung |
| --- | --- | --- | --- |
| `--tab-border-radius` | 24px | `tab.tokens.css` | Radius des Tab-Hintergrunds; Schließen-Knopf nimmt Radius − 3px |
| `--tab-margin-block` | 4px (normal: 6px) | `tab.tokens.css`, `tabs.css` | Abstand über und unter dem Tab-Hintergrund |
| `--tab-min-height` | 28px (normal: 32px) | `tabs.css` | Höhe des Tab-Hintergrunds |
| `--tab-overflow-clip-margin` | 2px | `tab.tokens.css` | Innenabstand links/rechts je Tab → 4px Lücke zwischen zwei Tabs |
| `--tab-inline-padding` | 6px (normal: 8px) | `tabs.css`, `tab.tokens.css` | Innenabstand von Icon/Text zum Tab-Rand |
| `--tab-min-width-pref` | 76px | Inline-Style auf `#tabbrowser-tabs`, aus `browser.tabs.tabMinWidth` | Mindestbreite eines Tabs |
| `--tab-max-width` | 225px | `tabs.css`, auf `#tabbrowser-tabs` | Maximalbreite eines Tabs |

Die Tableiste ist `--tab-min-height + 2 × --tab-margin-block` hoch: 28 + 2 × 4 = 36px. Werte für
„normal“ stammen aus der Quelle, nicht aus einer Messung.

Der Tab-Radius ist kein eigener Wert, sondern eine Kette:
`--tab-border-radius` → `--toolbarbutton-border-radius` → `--button-border-radius` →
`--border-radius-xlarge` (Nova: 24px). Adressleiste und Toolbar-Buttons hängen an derselben Kette.
Die Radius-Tokens in Nova (`tokens-shared.css`): `xsmall` 4px, `small` 8px, `medium` 12px,
`large` 16px, `xlarge` 24px, `circle` 9999px.

Eine Variable muss dort überschrieben werden, wo Firefox sie setzt, oder weiter innen. Die meisten
stehen auf `:root`; `--tab-min-width-pref` und `--tab-max-width` stehen auf `#tabbrowser-tabs`.

### Reicht das Überschreiben?

Gemessen mit `variablen.py`: 60 Tabs, Fenster 1400px breit, kompakt.

| Variante | Tab-Radius | Radius Adressleiste, Buttons | Lücke zwischen Tabs | Höhe Tableiste | Tab-Breite | Tabs im sichtbaren Bereich |
| --- | --- | --- | --- | --- | --- | --- |
| ohne CSS | 24px | 24px | 4px | 36px | 76px | 16 |
| Tab-Variablen | 0 | 24px | 0 | 28px | 40px | 32 |
| Radius-Tokens | 0 | 0 | 4px | 36px | 76px | 16 |
| `* { border-radius: 0 !important; }` | 0 | 0 | 4px | 36px | 76px | 16 |

- **Tab-Variablen:** `--tab-border-radius: 0`, `--tab-margin-block: 0px`,
  `--tab-overflow-clip-margin: 0px`, `--tab-inline-padding: 2px` auf `:root` und
  `--tab-min-width-pref: 40px` auf `#tabbrowser-tabs`, alle mit `!important`.
- **Radius-Tokens:** die sechs `--border-radius-*`-Tokens auf `:root` auf `0 !important`.

Ergebnis: Für eckige, lückenlose, schmalere Tabs und eine eckige Adressleiste genügen
Variablen-Überschreibungen. Regeln auf einzelne Elemente sind dafür nicht nötig. Per CSS geht die
Mindestbreite auch unter die 50px, auf die Firefox die Pref begrenzt.

Die Zahlen 40px und 2px sind Testwerte, keine Gestaltungsempfehlung. Gemessen sind berechnete
Styles und Layout, **kein Bild**: Ob Text, Favicon und Schließen-Knopf bei der Breite noch gut
aussehen und ob der aktive Tab erkennbar bleibt, zeigt nur der echte Browser. Nicht gemessen:
Menüs, Panels, Sidebar, vertikale Tabs, Dichte „normal“.

## Farben

Auch Farben lassen sich über Variablen setzen. Wir legen sie über das eingebaute Theme „Firefox
Dunkel“ und binden den Block an dessen Kennung, damit er mit keinem anderen Theme kollidiert:

```css
:root[theme-effective-id="firefox-compact-dark@mozilla.org"] { … }
```

| Fläche | Variable |
| --- | --- |
| Tableiste / Fensterrahmen | `--toolbox-background-color`, `--toolbox-background-color-inactive` |
| Verlauf im Rahmen | `--toolbox-background-image` (auf `none`) |
| Text inaktiver Tabs | `--toolbox-text-color` |
| Aktiver Tab | `--tab-background-color-selected`, `--tab-text-color-selected` |
| Rand des aktiven Tabs | `--tab-border-color-selected-leading` und `-trailing` (beide gleich = einfarbig) |
| Navigationsleiste | `--toolbar-background-color`, `--toolbar-text-color` |
| Adressfeld | `--toolbar-field-background-color` (auch `-focus`), `--toolbar-field-text-color`, `--toolbar-field-border-color` |
| Icons | `--toolbarbutton-icon-fill` |
| Hover der Buttons | `--toolbarbutton-background-color-hover`, `-active` |
| Schließen-Kreuz im Tab | `--tab-close-button-text-color` (auch `-hover`, `-active`) |
| Plaketten im Adressfeld | `--urlbar-box-background-color` (auch `-hover`, `-active`) |

Gemessen in 157.0: Mit diesen Variablen stimmen die berechneten Farben von Leiste, Tabs,
Navigationsleiste, Adressfeld, Icons und Hover mit denen eines eigenen Themes gleicher Farben
überein; „Firefox Hell“ bleibt vom dunklen Block unberührt, und ein entsprechender Block über
„Firefox Hell“ funktioniert ebenso.

Was bei dieser Lösung von „Firefox Dunkel“ bleibt: Menüs und Panels (`--panel-background-color`),
Sidebar, Akzentfarbe und Fokusring (`--color-accent-primary`, `--focus-outline-color`, Nova-Lila)
und die Trennlinie unter der Navigationsleiste. Zwischen Tableiste und Navigationsleiste zeichnen
die eingebauten Themes keine Linie; ein eigenes Theme hätte dort 1 px.

Nicht geprüft: inaktives Fenster, privates Fenster.

## Shadow DOM

Teile der Oberfläche liegen in Shadow-Trees, z. B. die Scroll-Pfeile der Tableiste in
`#tabbrowser-arrowscrollbox`. Gemessen:

| Selektor | Trifft das Element im Shadow-Tree? |
| --- | --- |
| `#scrollbutton-up` | ja |
| `#tabbrowser-arrowscrollbox #scrollbutton-up` | nein |
| `#tabbrowser-arrowscrollbox::part(scrollbutton-up)` | nein |

User-Regeln gelten also auch innerhalb von Shadow-Trees, aber ein Selektor kann die Grenze nicht
überqueren, und `::part()` funktioniert aus `userChrome.css` nicht. Variablen vererben sich durch
die Grenze hindurch – ein weiterer Grund, mit Variablen zu arbeiten.

## Pref-Abfragen und `@import`

- `@media -moz-pref("name") { … }` fragt eine Boolean-Pref ab. Es funktioniert in
  `userChrome.css` mit Firefox-Prefs (`browser.nova.enabled`) und mit selbst angelegten. Eine
  nicht vorhandene Pref gilt als falsch. Damit lassen sich Teile des CSS per `about:config`
  schalten. Firefox selbst benutzt das für Nova: `@media -moz-pref("browser.nova.enabled")`.
- Die ältere Schreibweise `@supports -moz-bool-pref("name")` aus vielen Anleitungen funktioniert in
  157 nicht mehr.
- Die Dichte liegt als Attribut vor: `:root[uidensity="compact"]`.
- `@import` muss vor allen anderen Regeln stehen. Relative Pfade werden vom Ort im Profil aus
  aufgelöst, **nicht** vom Ziel eines Symlinks. Wer nur `userChrome.css` aus einem Repo ins Profil
  verlinkt, erreicht per `@import` keine Nachbardateien im Repo – dann den ganzen Ordner `chrome`
  verlinken oder bei einer Datei bleiben.

## Selektoren und Variablen finden

- **Quelltext lesen.** Das CSS der installierten Version liegt in
  `/usr/lib/firefox/browser/omni.ja` (ZIP; `unzip` meldet eine Warnung, entpackt aber) unter
  `chrome/browser/skin/classic/browser/`, die Tokens in `/usr/lib/firefox/omni.ja` unter
  `chrome/toolkit/skin/classic/global/design-system/`. Online:
  [searchfox](https://searchfox.org/firefox-main/source/browser/themes/shared). Wichtig für Tabs:
  `tabbrowser/tabs.css` und `tabbrowser/tab.tokens.css`.
- **Browser-Werkzeuge (Browser Toolbox).** Die Entwicklerwerkzeuge für die Firefox-Oberfläche
  selbst. In den Einstellungen der Entwicklerwerkzeuge „Debugging-Werkzeuge für Browser-Chrome und
  Add-ons aktivieren“ und „Externes Debugging aktivieren“ einschalten (Prefs
  `devtools.chrome.enabled`, `devtools.debugger.remote-enabled`), dann Strg+Umschalt+Alt+I oder
  Extras → Web-Entwickler → Browser-Werkzeuge. Der Inspektor zeigt Elemente, Regeln und berechnete
  Werte der Oberfläche; Änderungen dort wirken sofort, ohne Neustart. Die Option „Popups nicht
  automatisch ausblenden“ hält Menüs zum Untersuchen offen
  ([Doku](https://firefox-source-docs.mozilla.org/devtools-user/browser_toolbox/index.html)).
- **Simulator.** `userchrome/simulator.html` baut die Tableiste mit Firefox' Regeln und
  Variablennamen nach, zeigt die Wirkung jeder Stellschraube sofort und erzeugt die passende
  `userChrome.css`. `simulator.py` prüft, dass seine Maße mit dem echten Firefox übereinstimmen.
- **Messen ohne Fenster.** Die Skripte in `userchrome-test/` starten Firefox headless mit einem
  Wegwerf-Profil und lesen berechnete Werte aus. Geeignet, um nach einem Firefox-Update zu prüfen,
  ob Variablen noch existieren und wirken.

## Risiken

- **Updates.** Variablen und Selektoren können umbenannt werden oder wegfallen. Beispiel:
  `--proton-tab-block-margin`, das viele Anleitungen im Netz noch nennen, gibt es in 157 nicht
  mehr; es heißt jetzt `--tab-margin-block`. Nach jedem größeren Update prüfen.
- **Keine Zusage.** Die Pref trägt „legacy“ im Namen; eine Stabilitätsgarantie gibt es nicht.
- **Nicht verteilbar wie ein Theme.** Kein AMO, keine Signatur, keine automatische Aktualisierung.
  Installation heißt: Pref setzen, Datei ins Profil legen, neu starten.
- **Neustart für jede Änderung** an der Datei. Zum Ausprobieren die Browser-Werkzeuge nehmen.
- **Fehlbedienung.** Eine Regel kann Bedienelemente verstecken oder überlagern. Notausgang:
  Fehlerbehebungsmodus oder Datei umbenennen.

## Tests

```sh
cd docs/firefox-theming/userchrome-test
./mechanik.py        # Laden, Kaskade, Shadow DOM, Pref-Abfragen
./mechanik.py aus    # Gegenprobe: Pref aus, nichts greift
./variablen.py       # Wirkung der Variablen auf Tabs, Adressleiste, Buttons
./simulator.py       # userchrome/simulator.html gegen den echten Firefox messen
```

Die Skripte brauchen Python 3 und `firefox` im PATH. Sie öffnen kein Fenster, benutzen ein
temporäres Profil und fassen das eigene Profil nicht an. Ein laufender Firefox stört nicht.

Letzter Lauf: 01.10.2026, Firefox 157.0 (Arch Linux, Build 20260929100108).

## Nicht belegt

- Ob es Pläne gibt, die Pref zu entfernen. Gefunden habe ich keine Ankündigung.
- Mozillas Support-Artikel
  [„Contributors guide on Firefox advanced customization with CSS“](https://support.mozilla.org/en-US/kb/contributors-guide-firefox-advanced-customization)
  ließ sich nicht abrufen und ist hier nicht eingearbeitet.
- Welche Fenster und Seiten im Einzelnen zur Chrome-Docshell zählen (Bibliothek, Sidebar-Inhalte,
  `about:`-Seiten). Laut
  [firefox-csshacks](https://github.com/MrOtherGuy/firefox-csshacks) gehören Webseiten und
  eingebaute Seiten zu `userContent.css`.
- Ob die Stilbearbeitung in den Browser-Werkzeugen `userChrome.css` direkt bearbeiten und speichern
  kann (in Anleitungen verbreitet, nicht geprüft).

## Quellen

- Firefox-Quellcode, Branch `release`: `layout/style/GlobalStyleSheetCache.cpp`,
  `dom/base/Document.cpp`, `servo/components/style/parser.rs` (`chrome_rules_enabled`: Chrome-only
  CSS ist in User-Stylesheets erlaubt)
- Firefox 157.0, installiert: `browser/themes/shared/tabbrowser/tabs.css`, `tab.tokens.css`,
  `urlbar/urlbar.tokens.css`, `toolkit/themes/shared/design-system/tokens-shared.css`,
  `browser/components/tabbrowser/content/tabs.js`, `toolkit/modules/Troubleshoot.sys.mjs`
- [Bug 1541233](https://bugzilla.mozilla.org/show_bug.cgi?id=1541233) – Einführung der Pref
- [Browser Toolbox](https://firefox-source-docs.mozilla.org/devtools-user/browser_toolbox/index.html) –
  Firefox Source Docs
- [userchrome.org](https://www.userchrome.org/how-create-userchrome-css.html) – Einrichtung
- [MrOtherGuy/firefox-csshacks](https://github.com/MrOtherGuy/firefox-csshacks) – größte gepflegte
  Sammlung von `userChrome.css`-Bausteinen (MPL 2.0), gut zum Nachschlagen
