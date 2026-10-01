# Kompaktmodus (UI-Dichte)

Der Kompaktmodus ist eine Nutzereinstellung, unabhängig vom Theme. Ein Static Theme kann die Dichte
weder setzen noch abfragen. Quellen: Firefox 157.0.1 (`browser/app/profile/firefox.js`,
`browser/themes/shared/tabbrowser/tabs.css`) und die
[Release Notes](https://www.firefox.com/en-US/firefox/157.0/releasenotes/).

## Einstellung

Einstellungen → Erscheinungsbild → Dichte. Dahinter steht dieselbe Pref wie früher:

| Pref | Werte / Standard | Bedeutung |
| --- | --- | --- |
| `browser.uidensity` | `0` normal, `1` kompakt, `2` Touch | Dichte der Browser-Oberfläche; ohne Nutzerwert gilt „Automatisch“ |
| `browser.compactmode.auto.threshold` | `"0.05"` | Im Automatik-Modus schaltet Nova auf kompakt, wenn die Tableiste mehr als 5 % der Fensterhöhe (oder die eingeklappte Sidebar mehr als 5 % der Breite) einnähme. Ein explizit gewählter Wert wird nie überschrieben |
| `browser.compactmode.show` | `false` | Laut Quellkommentar: ob Firefox die Kompakt-Option der UI-Dichte anzeigt |
| `browser.touchmode.auto` | abhängig von Nova | Automatisch auf Touch-Dichte wechseln |
| `browser.nova.enabled` | `true` | Globaler Schalter für das Nova-Design |
| `sidebar.revamp` | `true` | Neue Sidebar; `false` bringt die alte zurück (laut Release Notes bis Ende 2027) |
| `sidebar.verticalTabs` | `false` | Vertikale Tabs |

## Maße

Die Dichte landet als Attribut auf dem Wurzelelement: `:root[uidensity="compact"]` bzw. `"touch"`.

| | Normal | Kompakt | Touch |
| --- | --- | --- | --- |
| `--tab-min-height` (Nova) | 32px | 28px | 41px |
| `--tab-min-height` (vor Nova) | 36px | 29px | 41px |

## Tab-Breite (horizontale Tabs)

Quellen: `browser/app/profile/firefox.js`, `browser/components/tabbrowser/content/tabs.js`,
`browser/themes/shared/tabbrowser/tabs.css` (157.0.1).

| Größe | Wert | Einstellbar über |
| --- | --- | --- |
| Mindestbreite eines Tabs | 76px | Pref `browser.tabs.tabMinWidth`; Firefox begrenzt den Wert nach unten auf **50** |
| Maximalbreite eines Tabs | 225px (`--tab-max-width`) | nur `userChrome.css` |
| Innenabstand links/rechts (kompakt) | 6px (`--tab-inline-padding`) | nur `userChrome.css` |
| Eckenradius des Tabs | `--tab-border-radius` | nur `userChrome.css` |
| Schließen-Knopf auf inaktiven Tabs | verschwindet, sobald die Tableiste überläuft; Schwelle sonst `browser.tabs.tabClipWidth` = 140 | Pref |
| Zuschlag bei Ton-/Notiz-Icon | +20 bis +44px Mindestbreite | nur `userChrome.css` |

Sind alle Tabs auf Mindestbreite geschrumpft, beginnt die Tableiste zu scrollen. Eine kleinere
Mindestbreite heißt also: mehr Tabs gleichzeitig sichtbar.

## Bedeutung für das Projekt

- Mit einem reinen Static Theme können wir die Dichte nicht beeinflussen. Wir testen in „Kompakt“
  und stellen sicher, dass Kontraste und Trennlinien dort funktionieren.
- Mehr Platzersparnis als der eingebaute Kompaktmodus ginge nur über `userChrome.css`
  (`toolkit.legacyUserProfileCustomizations.stylesheets = true`), z. B. mit Regeln unter
  `:root[uidensity="compact"]`. Das ist inoffiziell und kann mit jedem Firefox-Update brechen.
