# CLAUDE.md

## Projekt

Minimalistisches, gut benutzbares Firefox-Theme für das Nova-Design (Firefox 157+), ausgelegt auf
den Kompaktmodus. Das Theme entsteht gemeinsam mit dem Nutzer: Gestaltungsentscheidungen trifft er,
nicht Claude.

Stand: Setup-Phase. Es gibt noch kein Theme, nur Doku und offene Fragen.

## Arbeitsregeln

- **Commit und Push nach jeder bedeutsamen Änderung.** Nicht sammeln, nicht auf Nachfrage warten.
- **Direkt auf `main`.** Branches nur in Ausnahmefällen (Experimente). In der ersten Phase – bis das
  erste Theme abgeschlossen ist – geht alles auf `main`.
- **Offene Fragen gehören in [`OFFENE_FRAGEN.md`](OFFENE_FRAGEN.md).** Bei Gestaltungs- und
  Richtungsfragen nicht raten: Frage dort eintragen, mit Empfehlung, und an allem weiterarbeiten,
  was nicht davon abhängt. Beantwortete Fragen in den Abschnitt „Entschieden“ verschieben und die
  Entscheidung dort umsetzen, wo sie hingehört (README, Theme, diese Datei).
- Kommunikation mit dem Nutzer auf Deutsch.

## Technische Leitplanken

- Theme-Keys nicht aus dem Gedächtnis verwenden. Nova hat Wirkung und Bedeutung einiger Keys
  geändert. Zuerst nachsehen:
  - [`docs/firefox-theming/theme-keys.md`](docs/firefox-theming/theme-keys.md) – alle Keys mit
    Nova-Status
  - [`docs/firefox-theming/nova-aenderungen.md`](docs/firefox-theming/nova-aenderungen.md) –
    Änderungen und Test-Checkliste
  - `docs/firefox-theming/upstream/firefox-source/theme.schema.json` – was Firefox tatsächlich
    akzeptiert
- Ein Static Theme setzt nur Farben, Bilder und Verläufe. Form, Abstände, Icons, Akzentfarbe und
  UI-Dichte sind nicht erreichbar. Wünsche, die das brauchen, nicht stillschweigend über
  `userChrome.css` lösen, sondern als Frage aufnehmen.
- Kontrast: Text mindestens 4,5 : 1, UI-Elemente (Rahmen, Icons) mindestens 3 : 1. Bei jeder
  Farbänderung nachrechnen.

## Doku-Ablage

- `docs/firefox-theming/upstream/` sind unveränderte Upstream-Kopien – nicht von Hand editieren,
  sondern mit `docs/firefox-theming/fetch-docs.sh` neu laden.
- `docs/firefox-theming/upstream/unlicensed/` (offizielle Nova-Theme-Manifeste u. a.) ist per
  `.gitignore` ausgeschlossen, weil die Quell-Repos keine Lizenz haben. Fehlt der Ordner lokal:
  `fetch-docs.sh` ausführen. Nichts daraus einchecken.
- Eigene Notizen (deutsch) liegen direkt in `docs/firefox-theming/`. Was dort steht, muss durch
  eine Upstream-Quelle gedeckt sein; Unbelegtes als solches kennzeichnen.

## Testen

Themes müssen für Release-Firefox signiert sein; zum Entwickeln temporär laden:

- `about:debugging#/runtime/this-firefox` → „Temporäres Add-on laden“ → `manifest.json` wählen.
  Hält bis zum Neustart.
- `npx web-ext lint` und `npx web-ext run` im Theme-Ordner (`web-ext` ist nicht global installiert).

Vor jedem Commit, der Farben ändert, die Checkliste in `nova-aenderungen.md` durchgehen. Was nicht
selbst im Browser angesehen wurde, dem Nutzer ausdrücklich zum Prüfen nennen.
