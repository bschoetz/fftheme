# Firefox-Theming-Doku (Nova, Firefox 157+)

Lokale Ablage der Theming-Dokumentation, auf die sich dieses Projekt stützt.
Stand der Upstream-Kopien: siehe [`upstream/STAND.txt`](upstream/STAND.txt).
Neu laden mit [`./fetch-docs.sh`](fetch-docs.sh).

## Kurzfazit

- Es gibt **keine neue Theme-API**. „Nova“ ist das neue Firefox-Design (ab 157); Themes sind
  weiterhin WebExtension-**Static-Themes**: eine `manifest.json` mit `theme` (hell) und optional
  `dark_theme` (dunkel), jeweils mit `colors`, `images`, `properties`.
- Ein Static Theme kann **nur Farben, Hintergrundbilder und Verläufe** setzen. Form (Eckenradien),
  Abstände, Icons, Schriftgrößen und Layout sind damit **nicht** änderbar – das ginge nur über
  `userChrome.css` (inoffiziell, keine API-Garantie) oder `theme_experiment` (nur Nightly/Developer
  Edition).
- Neu bzw. für Nova relevant: CSS-Verläufe in `theme_frame`/`additional_backgrounds` (ab 153),
  `backgrounds_area` (ab 156), Sidebar teilt sich den Hintergrund mit dem Toolbar-Bereich,
  kein Schatten mehr unter dem aktiven Tab (→ `tab_selected` + `tab_line` setzen).
- Die **Akzentfarbe** (Buttons, Checkboxen, Toggles) kann ein Theme nicht setzen; bei jedem
  Nicht-Standard-Theme nimmt Firefox die Akzentfarbe des Betriebssystems.
- **Kompaktmodus** ist eine Nutzereinstellung (`browser.uidensity = 1`), kein Theme-Feature.
  Ein Theme kann ihn weder erzwingen noch erkennen – wir müssen nur darin gut aussehen.

## Eigene Zusammenfassungen (deutsch)

| Datei | Inhalt |
| --- | --- |
| [`theme-keys.md`](theme-keys.md) | Arbeitsreferenz: alle `colors`/`images`/`properties`-Keys mit Wirkung, Nova-Status und CSS-Variable |
| [`nova-aenderungen.md`](nova-aenderungen.md) | Was sich mit Nova für Theme-Autoren ändert, inkl. Test-Checkliste |
| [`kompaktmodus.md`](kompaktmodus.md) | Dichte-Einstellung, Prefs und Maße laut Firefox-Quellcode |

Die Zusammenfassungen sind sinngemäß, nicht wörtlich. Im Zweifel gilt die Upstream-Quelle.

## Upstream-Kopien (englisch, unverändert)

### `upstream/mdn/` – MDN Web Docs

Quelle: <https://github.com/mdn/content> (`files/en-us/mozilla/…`), Autoren: Mozilla Contributors.
Lizenz der Texte: [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/), Codebeispiele CC0.
Die Dateien sind MDN-Markdown inkl. Makros (`{{…}}`); die eingebetteten Screenshots sind nicht
mitkopiert – dafür die Online-Seite öffnen.

| Datei | Online |
| --- | --- |
| `manifest-theme.md` | [manifest.json/theme](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/theme) – **die** Referenz |
| `manifest-dark_theme.md` | [manifest.json/dark_theme](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/dark_theme) |
| `manifest-theme_experiment.md` | [manifest.json/theme_experiment](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/theme_experiment) |
| `manifest-browser_specific_settings.md` | [manifest.json/browser_specific_settings](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/browser_specific_settings) |
| `api-theme*.md` | [theme-API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/theme) (dynamische Themes aus einer Extension heraus) |
| `firefox-157-for-developers.md` | [Firefox 157 for developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/157) |

### `upstream/firefox-source/` – Firefox-Quellcode

Quelle: <https://github.com/mozilla-firefox/firefox> (Branch `release`), Lizenz:
[MPL 2.0](https://www.mozilla.org/MPL/2.0/).

| Datei | Pfad im Firefox-Repo | Wozu |
| --- | --- | --- |
| `theme.schema.json` | `toolkit/components/extensions/schemas/theme.json` | Maßgebliches Schema: welche Keys Firefox überhaupt akzeptiert |
| `ThemeVariableMap.sys.mjs` | `browser/themes/ThemeVariableMap.sys.mjs` | Theme-Key → CSS-Variable (Browser-Chrome) |
| `LightweightThemeConsumer.sys.mjs` | `toolkit/modules/LightweightThemeConsumer.sys.mjs` | Theme-Key → CSS-Variable (Toolkit), Fallback- und Farbschema-Logik |
| `default-theme.manifest.json` | `toolkit/mozapps/extensions/default-theme/manifest.json` | Das Standard-Theme (leeres `theme`-Objekt) |
| `design-tokens.md` | `toolkit/themes/shared/design-system/docs/README.design-tokens.stories.md` | Design-Token-System (nur für `userChrome.css` relevant) |

### `upstream/unlicensed/` – nur lokal, nicht im Repo

Per `.gitignore` ausgeschlossen, weil die Quell-Repos keine Lizenzdatei haben. `./fetch-docs.sh`
legt sie lokal ab:

- `acorn-themes/` – <https://github.com/FirefoxUX/acorn-themes>: die Manifeste der elf offiziellen
  Nova-Themes (`themes/nova/*/manifest.json`), das alte Proton-Theme und ein JSON-Schema für
  Static-Theme-Manifeste. Beste Praxisvorlage dafür, wie Mozilla selbst Nova themt.
- `extension-workshop/static-themes.md` – Quelle von
  <https://extensionworkshop.com/documentation/themes/static-themes/>.

## Weitere Quellen (nur verlinkt)

- [Nova is here: what changes for your Firefox theme](https://blog.mozilla.org/addons/2026/09/29/nova-is-here-what-changes-for-your-firefox-theme/) – Mozilla Add-ons Blog, 29.09.2026 → zusammengefasst in `nova-aenderungen.md`
- [Acorn Design System – Theming Overview](https://acorn.firefox.com/latest/desktop/styles/theming/overview-QX5apkK4) und [Theming Colors](https://acorn.firefox.com/latest/desktop/styles/theming/colors-PLEhOJ5C) → eingearbeitet in `theme-keys.md`
- [Firefox 157.0 Release Notes](https://www.firefox.com/en-US/firefox/157.0/releasenotes/)
- [Firefox Color](https://color.firefox.com/) – Theme-Farben live ausprobieren
- [Signing and distribution overview](https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/) – Themes müssen signiert sein
- [searchfox](https://searchfox.org/firefox-main/source/browser/themes/shared) – Chrome-CSS von Firefox durchsuchen
