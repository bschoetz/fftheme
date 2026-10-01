# Nova: Was sich für Themes ändert

Sinngemäße Zusammenfassung von
[„Nova is here: what changes for your Firefox theme“](https://blog.mozilla.org/addons/2026/09/29/nova-is-here-what-changes-for-your-firefox-theme/)
(Mozilla Add-ons Blog, 29.09.2026), ergänzt um Angaben aus MDN. Nova ist seit Firefox 157 das
Standarddesign und die größte Überarbeitung seit Proton (2021).

Grundsatz: Die meisten Farb- und Bild-Properties funktionieren wie bisher. Geändert hat sich,
**wo** sie erscheinen, wie sie nebeneinander wirken, und einige Properties haben keine sichtbare
Wirkung mehr.

## Browser-Rahmen

| Bereich | Proton | Nova (157) |
| --- | --- | --- |
| Horizontale Tabs | Theme-Hintergrund auf der Tableiste | unverändert |
| Vertikale Tabs | Tableisten-Farbe auf der Tableiste | Tableisten-Farbe erscheint zusätzlich auf der Toolbar |
| Sidebar | eigenes Panel | teilt sich den Theme-Hintergrund mit dem Toolbar-Bereich |

Toolbar und Sidebar liegen bündig am Fensterrand, ohne Lücken oder schwebende Rahmen.

## Farben, Akzent, Tabs

- **Akzentfarbe:** Nur das Standard-Theme benutzt Novas Lila. Jedes andere Theme bekommt für
  Buttons und akzentuierte Controls die Akzentfarbe des Betriebssystems. Per Manifest nicht setzbar.
- **Fokus- und Linkfarben:** Bei aktivem Fremd-Theme setzt Firefox eigenes Blau/Cyan für Fokusringe
  und manche Links.
- **Aktiver Tab:** Der Schatten unter dem aktiven Tab ist weg. `tab_selected` und `tab_line` setzen,
  damit er sich abhebt.
- **Button-Hover:** `button_background_hover` / `button_background_active` gelten jetzt auch für
  Buttons auf der Tableiste und (bei vertikalen Tabs) auf dem Frame-Hintergrund. Halbtransparente
  Werte wie `rgba(0, 0, 0, 0.15)` (Hover) und `rgba(0, 0, 0, 0.3)` (gedrückt) funktionieren auf
  beiden Untergründen.

## Sidebar und vertikale Tabs

- Der Theme-Hintergrund läuft unter der Sidebar weiter – Sidebar und Toolbar wirken wie eine Fläche.
- `sidebar` und `sidebar_text` explizit setzen; fehlen sie, wählt Firefox passende Farben selbst.
- `sidebar_border` färbt jetzt die Trennlinie zwischen Sidebar und Seite (der Splitter ist weg).
- Buttons und Icons in der Sidebar leiten sich aus der Textfarbe ab, nicht mehr aus den
  Toolbar-Button-Farben.
- Bei vertikalen Tabs gilt die Tableisten-Farbe (`frame`) auch für die Toolbar – Kontrast prüfen.
- Bekannter Fehler in 157: Bei „Sidebar beim Hovern ausklappen“ fehlt u. U. der Theme-Hintergrund.
  Behoben in Firefox 158 (13.10.2026).

## Properties mit geänderter oder ohne Wirkung

| Property | In Nova |
| --- | --- |
| `ntp_text` | färbt das Suchfeld der Neuer-Tab-Seite nicht mehr |
| `popup_text` | färbt das Adressleisten-Dropdown nicht mehr; andere Popups weiterhin |
| `sidebar_highlight` | keine sichtbare Wirkung, Standard-Highlight wird benutzt |
| `sidebar_highlight_text` | keine sichtbare Wirkung |
| `toolbar_bottom_separator` | Trennlinie neben/unter der Toolbar und rund um die Seite |

## Hintergrundbilder und Verläufe

Bilder können jetzt hinter Sidebar und vertikalen Tabs erscheinen. Steuerung über
`properties.backgrounds_area` (ab Firefox 156):

| Wert | Wirkung |
| --- | --- |
| `"auto"` (Standard) | Firefox entscheidet anhand von `additional_backgrounds_alignment`: Ist ein Bild vertikal mittig oder unten ausgerichtet, bleiben die Bilder in den oberen Toolbars, sonst füllen sie das ganze Fenster |
| `"window"` | ganzes Fenster, auch hinter Sidebar und vertikalen Tabs |
| `"top_toolbars"` | nur Menüleiste, Tableiste, Navigations- und Lesezeichenleiste; die Sidebar nimmt `frame` |

Zusätzlich eine `toolbar`-Farbe setzen (auch halbtransparent), damit Benachrichtigungsleisten lesbar
bleiben.

**Verläufe** (ab Firefox 153): `theme_frame` und Einträge in `additional_backgrounds` dürfen statt
eines Bildpfads ein Objekt `{ "linear-gradient": "…" }` sein (auch `radial-`, `conic-` und die
`repeating-`-Varianten). `backgrounds_area` gilt für Verläufe genauso. Ältere Firefox-Versionen
ignorieren Unbekanntes; wer darauf angewiesen ist, setzt `strict_min_version`.

So nutzen es die offiziellen Nova-Themes (Muster aus `upstream/unlicensed/acorn-themes`):

```json
"images": {
  "additional_backgrounds": [
    { "linear-gradient": "135deg, #FFF9F6 0%, #FBF4EE 60%, #E3DBD7 100%" }
  ]
},
"properties": {
  "additional_backgrounds_tiling": ["no-repeat"],
  "additional_backgrounds_size": ["auto"],
  "backgrounds_area": "window"
}
```

Dazu `toolbar` halbtransparent (`#FFFFFF66` hell, `#00000033` dunkel), damit der Verlauf
durchscheint. Für ein minimalistisches Theme heißt das umgekehrt: **keine** `images`, deckende
`frame`/`toolbar`-Farben – dann gibt es keinen Verlauf.

## Test-Checkliste

Theme in Firefox 157 laden und in diesen Zuständen ansehen:

1. Horizontale und vertikale Tabs
2. Sidebar geschlossen, offen, per Hover ausgeklappt; dabei „Sidebar anpassen“ umschalten
3. Kompakte Dichte (Einstellungen → Erscheinungsbild)
4. Privates Fenster
5. Helles und dunkles System-Farbschema (Akzentfarbe folgt dem System)
6. Hover über die Buttons auf der Tableiste

## Angekündigt, noch ohne Termin

- Fokus- und Linkfarben, die zum Theme passen statt festem Blau/Cyan
- `popup_icons` für Icons in Menüs und Panels, getrennt von den Toolbar-Icons
- Theme-Farben für Hover- und Auswahlzustände in Sidebar-Panels
- Bessere Hover-Zustände für Tableisten-Buttons

## Sonstiges

- Mozilla bietet ein Theme [Firefox Proton](https://addons.mozilla.org/en-US/firefox/addon/firefox-proton/)
  an, das die alten Proton-Farben zurückbringt (nur Farben, nicht das Layout).
- Probleme mit Themes meldet man im [Add-ons-Discourse](https://discourse.mozilla.org/c/add-ons/35).
