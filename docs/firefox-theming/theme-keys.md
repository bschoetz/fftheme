# Theme-Keys: Arbeitsreferenz

Verdichtet aus dem Firefox-Schema (`upstream/firefox-source/theme.schema.json`, Stand 157.0.1), den
Variablen-Maps (`ThemeVariableMap.sys.mjs`, `LightweightThemeConsumer.sys.mjs`), der
[Acorn-Farbliste](https://acorn.firefox.com/latest/desktop/styles/theming/colors-PLEhOJ5C) und dem
Nova-Blogpost. Ausführliche Beschreibungen mit Beispielen: `upstream/mdn/manifest-theme.md`.

## Aufbau

```json
{
  "manifest_version": 3,
  "name": "…",
  "version": "1.0",
  "browser_specific_settings": { "gecko": { "id": "…@…", "strict_min_version": "157.0" } },
  "theme":      { "colors": {}, "images": {}, "properties": {} },
  "dark_theme": { "colors": {}, "images": {}, "properties": {} }
}
```

- `theme` allein gilt für hell **und** dunkel. Mit `dark_theme` gilt `theme` für das helle,
  `dark_theme` für das dunkle Farbschema.
- Alle Farb-Keys sind optional; für fehlende gibt es Fallbacks.
- Farbwerte: CSS-Farbstring (`"#RRGGBB"`, `"#RRGGBBAA"`, `"rgb(…)"`, Farbname), `[r, g, b]` oder
  `[r, g, b, a]`.
- Ein Theme-Paket darf keinen Extension-Code enthalten. Dynamische Themes gehen nur über die
  `theme`-API einer normalen Extension.

## colors

Spalte „Nova“: ✓ = laut Mozilla unverändert (von uns noch nicht im Browser nachgeprüft), sonst
Hinweis. CSS-Variable = worauf Firefox den Key intern
abbildet (hilfreich im Browser-Werkzeugkasten).

### Rahmen und Tableiste

| Key | Wirkung | Nova | CSS-Variable |
| --- | --- | --- | --- |
| `frame` | Hintergrund der Tableiste / des Fensterrahmens | ✓ – bei vertikalen Tabs auch auf der Toolbar; Sidebar-Bereich bei `backgrounds_area: "top_toolbars"` | `--lwt-accent-color` |
| `frame_inactive` | wie `frame`, wenn das Fenster nicht fokussiert ist | ✓ | `--lwt-accent-color-inactive` |
| `tab_background_text` | Text nicht aktiver Tabs; Fallback für `tab_text` | ✓ | `--lwt-text-color` |
| `tab_selected` | Hintergrund des aktiven Tabs | ✓ – **setzen**, der Schatten ist weg | `--tab-background-color-selected` |
| `tab_text` | Text des aktiven Tabs | ✓ | `--tab-text-color-selected` |
| `tab_line` | Umrandung des aktiven Tabs | ✓ – **setzen** | `--lwt-tab-line-color` |
| `tab_loading` | Ladeindikator im Tab | ✓ | `--tab-loading-fill` |
| `tab_background_separator` | Trenner zwischen Hintergrund-Tabs | laut MDN seit Firefox 89 ohne Wirkung; die Nova-Themes setzen ihn trotzdem | `--lwt-background-tab-separator-color` |

### Toolbar und Adressleiste

| Key | Wirkung | Nova | CSS-Variable |
| --- | --- | --- | --- |
| `toolbar` | Hintergrund von Navigations-/Lesezeichenleiste und Suchleiste („In Seite suchen“) | ✓ – auch bei Bild/Verlauf setzen | `--toolbar-background-color` |
| `toolbar_text` | Text in Toolbars und Suchleiste | ✓ | `--toolbar-text-color` |
| `bookmark_text` | Text der Lesezeichenleiste (Alias für `toolbar_text`) | ✓ | – |
| `icons` | Toolbar-Icons | ✓ – Sidebar-Icons folgen jetzt der Textfarbe | `--toolbarbutton-icon-fill` |
| `icons_attention` | Icons im Aufmerksamkeitszustand (Lesezeichen-Stern gefüllt, Download fertig) | ✓ | `--toolbarbutton-icon-fill-attention` |
| `button_background_hover` | Hover-Hintergrund von Toolbar-Buttons | ✓ – jetzt auch auf Tableiste/Frame; halbtransparent wählen | `--toolbarbutton-background-color-hover` |
| `button_background_active` | Hintergrund gedrückter/aktiver Toolbar-Buttons | ✓ – wie oben | `--toolbarbutton-background-color-active` |
| `toolbar_top_separator` | Linie zwischen Tableiste und Toolbar | ✓ – voll transparent = Linie nimmt keinen Platz ein | `--tabs-navbar-separator-color` |
| `toolbar_bottom_separator` | Linie zwischen Toolbar und Seite | geändert: Trenner neben/unter der Toolbar und rund um die Seite | `--chrome-content-separator-color` |
| `toolbar_vertical_separator` | senkrechte Trenner in der Lesezeichenleiste | ✓ | `--toolbarseparator-color` |
| `toolbar_field` | Hintergrund von Adress- und Suchfeld | ✓ | `--toolbar-field-background-color` |
| `toolbar_field_text` | Text im Adressfeld | ✓ | `--toolbar-field-text-color` |
| `toolbar_field_border` | Rahmen des Adressfelds | ✓ | `--toolbar-field-border-color` |
| `toolbar_field_focus` | Hintergrund des fokussierten Adressfelds | ✓ | `--toolbar-field-background-color-focus` |
| `toolbar_field_text_focus` | Text im fokussierten Adressfeld | ✓ | `--toolbar-field-text-color-focus` |
| `toolbar_field_border_focus` | Rahmen des fokussierten Adressfelds | ✓ | `--toolbar-field-border-color-focus` |
| `toolbar_field_highlight` | Hintergrund markierten Texts im Adressfeld | ✓ | `--lwt-toolbar-field-highlight` |
| `toolbar_field_highlight_text` | Farbe markierten Texts im Adressfeld | ✓ | `--lwt-toolbar-field-highlight-text` |

### Popups und Panels

| Key | Wirkung | Nova | CSS-Variable |
| --- | --- | --- | --- |
| `popup` | Hintergrund von Panels (Menü, Adressleisten-Dropdown …) | ✓ | `--panel-background-color` |
| `popup_text` | Text in Panels | geändert: nicht mehr im Adressleisten-Dropdown | `--panel-text-color` |
| `popup_border` | Rahmen von Panels | ✓ | `--panel-border-color` |
| `popup_highlight` | Hintergrund des ausgewählten Eintrags im Adressleisten-Dropdown | ✓ | `--urlbarview-background-color-selected` |
| `popup_highlight_text` | Text des ausgewählten Eintrags | ✓ | `--urlbarview-text-color-selected` |

### Sidebar

| Key | Wirkung | Nova | CSS-Variable |
| --- | --- | --- | --- |
| `sidebar` | Hintergrund der Sidebar-Panels (Alpha wird verworfen) | ✓ – **setzen**, sonst wählt Firefox selbst | `--sidebar-background-color` |
| `sidebar_text` | Text in der Sidebar; Icons/Buttons leiten sich davon ab | ✓ – **setzen** | `--sidebar-text-color` |
| `sidebar_border` | Linie zwischen Sidebar und Seite | geändert: Trennlinie statt Splitter | `--sidebar-border-color` |
| `sidebar_highlight` | Auswahl in Sidebar-Bäumen | **ohne Wirkung** | – |
| `sidebar_highlight_text` | Text der Auswahl | **ohne Wirkung** | – |

### Neuer Tab / Firefox View

| Key | Wirkung | Nova | CSS-Variable |
| --- | --- | --- | --- |
| `ntp_background` | Seitenhintergrund | ✓ | `--newtab-background-color` |
| `ntp_card_background` | Kartenhintergrund | ✓ | `--newtab-background-color-secondary` |
| `ntp_text` | Text | geändert: nicht mehr im Suchfeld | – |

### Veraltet (nicht benutzen)

`accentcolor` (→ `frame`), `textcolor` (→ `tab_background_text`), `toolbar_field_separator`,
`images.headerURL` (→ `theme_frame`).

## images

| Key | Wirkung |
| --- | --- |
| `theme_frame` | Bild oder Verlauf im Kopfbereich, oben rechts verankert. Ist es ein Verlauf, werden `additional_backgrounds` verdeckt |
| `additional_backgrounds` | Array aus Bildpfaden und/oder Verlaufsobjekten, erster Eintrag liegt oben |

Formate: JPEG, PNG, APNG, SVG, GIF (nicht animiert). Pfade relativ zur `manifest.json`, keine
externen URLs. Verlaufssyntax: `{ "linear-gradient": "<Parameter>" }`, ebenso `radial-gradient`,
`conic-gradient` und die `repeating-`-Varianten (ab Firefox 153).

## properties

| Key | Werte | Wirkung |
| --- | --- | --- |
| `color_scheme` | `auto` (Standard), `light`, `dark`, `system` | Farbschema für Chrome (z. B. Kontextmenüs) und Inhalte (interne Seiten, `prefers-color-scheme` der Webseiten) |
| `content_color_scheme` | wie oben | Nur für Inhalte; überschreibt `color_scheme` |
| `backgrounds_area` | `auto` (Standard), `window`, `top_toolbars` | Wo Bilder/Verläufe gezeichnet werden (ab 156), siehe `nova-aenderungen.md` |
| `additional_backgrounds_alignment` | Array, z. B. `"right top"` | Ausrichtung je Hintergrund |
| `additional_backgrounds_tiling` | Array: `no-repeat`, `repeat`, `repeat-x`, `repeat-y` | Kachelung je Hintergrund |
| `additional_backgrounds_size` | Array, Standard `"auto"` | Größe je Hintergrund |

## Was ein Static Theme nicht kann

- Akzentfarbe, Fokusring- und Linkfarben setzen
- Formen, Eckenradien, Abstände, Höhen, Schriftgrößen, Icons, Reihenfolge von UI-Elementen ändern
- Die UI-Dichte setzen oder abfragen
- Einstellungs- und Add-ons-Seite themen (bewusst gesperrt)
- Eigene Keys definieren – das ginge nur mit `theme_experiment` (Nightly/Developer Edition,
  `extensions.experiments.enabled`)

## Kontrast (Acorn-Vorgaben)

- Text: mindestens 4,5 : 1 (unter 18 pt bzw. 14 pt fett)
- UI-Elemente wie Rahmen und Icons: mindestens 3 : 1
- Paare, die zusammenpassen müssen: `frame` ↔ `tab_background_text`/`icons`;
  `tab_selected` ↔ `tab_text`; `toolbar` ↔ `toolbar_text`/`icons`/`toolbar_field_border`;
  `toolbar_field` ↔ `toolbar_field_text`; `popup` ↔ `popup_text`; `sidebar` ↔ `sidebar_text`.
  Hover-Zustände mischen die Textfarbe transparent ein – auch dort Kontrast prüfen.
