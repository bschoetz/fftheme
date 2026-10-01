# Offene Fragen

Hier sammelt Claude Fragen, die nur du entscheiden kannst. Antworte einfach unter der jeweiligen
Frage (oder im Chat) – entschiedene Fragen wandern nach unten in „Entschieden“.

Reihenfolge = Dringlichkeit. F1 und F2 bestimmen, was wir überhaupt bauen.

## Offen

### F1 – Was genau stört dich am neuen Design?

Ein Theme kann **nur Farben, Hintergrundbilder und Verläufe** ändern. Welche Punkte treffen zu?

- [ ] Farben allgemein (zu bunt, zu blass, zu wenig Kontrast …)
- [ ] das Lila als Akzentfarbe
- [ ] die Farbverläufe im Fensterrahmen
- [ ] aktiver Tab hebt sich schlecht ab
- [ ] runde Ecken / „Pillen“-Formen von Tabs, Adressleiste, Buttons
- [ ] Abstände und Größen (auch im Kompaktmodus noch zu viel Luft)
- [ ] Icons
- [ ] die neue Sidebar
- [ ] Neuer-Tab-Seite
- [ ] anderes: …

Die ersten vier löst ein normales Theme. Ecken, Abstände, Icons und Layout gehen damit **nicht** –
siehe F2. Ein, zwei Screenshots mit Markierungen würden hier viel helfen.

Antwort:

### F2 – Reines Theme oder auch `userChrome.css`?

| Variante | Kann | Preis |
| --- | --- | --- |
| **A: Static Theme** (`manifest.json`) | Farben, Verläufe, Bilder; hell + dunkel | offiziell, update-fest, auf AMO veröffentlichbar |
| **B: `userChrome.css`** | alles: Ecken, Abstände, Höhen, Icons, Elemente ausblenden | inoffiziell, kann mit jedem Firefox-Update brechen, manuelle Installation ins Profil, nicht über AMO verteilbar |
| **C: beides** | Theme für Farben, optionales CSS für Form und Dichte | zwei Dinge zu pflegen |

`theme_experiment` (Theme mit eigenem Stylesheet) scheidet praktisch aus: läuft nur in Nightly und
Developer Edition.

Empfehlung: mit **A** anfangen. Wenn F1 ergibt, dass dich vor allem Formen und Abstände stören,
auf **C** erweitern – das Theme bleibt dann trotzdem für sich nutzbar.

Antwort:

### F3 – Hell, dunkel oder beides?

Ein Paket kann beide Varianten enthalten und dem System-Farbschema folgen. Welche benutzt du selbst
überwiegend? Soll die andere gleichwertig sein oder erst später kommen?

Empfehlung: beide von Anfang an, deine Hauptvariante zuerst ausarbeiten.

Antwort:

### F4 – Farbrichtung

- Neutral (reine Grautöne), warm, kühl?
- Eine Akzentfarbe für aktiven Tab / Fokus – oder komplett monochrom?
- Gibt es ein Vorbild, das dir gefällt (früheres Firefox-Design wie Photon oder Proton, ein anderes
  Programm, dein Terminal- oder Editor-Farbschema, dein Sway-Setup)?

Hinweis: Die Akzentfarbe von Buttons, Checkboxen und Toggles kommt bei jedem Fremd-Theme vom
Betriebssystem, nicht vom Theme. Unter Sway also aus GTK/Portal-Einstellung.

Antwort:

### F5 – Wie benutzt du Firefox?

Bestimmt, welche Zustände wir zuerst gut machen und testen.

- Horizontale oder vertikale Tabs?
- Sidebar: benutzt, eingeklappt, ganz aus?
- Lesezeichenleiste sichtbar?
- Titelleiste sichtbar oder Tabs in der Titelleiste?
- Neuer-Tab-Seite: Firefox-Startseite oder leer?
- Viele Tabs gleichzeitig (dann zählt die Unterscheidbarkeit schmaler Tabs besonders)?

Antwort:

### F6 – Nur für dich oder veröffentlichen?

Release-Firefox installiert dauerhaft nur **signierte** Themes; ein temporär geladenes Theme ist
nach dem Neustart weg. Für den Alltag brauchen wir also eine Signatur von addons.mozilla.org (AMO):

- **Unlisted:** signiert, aber nicht auf AMO gelistet; Installation per `.xpi`. Braucht ein
  AMO-Konto mit API-Schlüssel.
- **Listed:** öffentlich auf AMO, mit Review, Beschreibung, Screenshots.

Empfehlung: zunächst unlisted signieren, Veröffentlichung später entscheiden.

Antwort:

### F7 – Name, ID, Lizenz

- Name des Themes (Arbeitstitel `fftheme`)?
- Add-on-ID, z. B. `fftheme@bschoetz` – einmal vergeben, später nicht mehr änderbar, ohne dass es
  als neues Add-on gilt.
- Lizenz für das Repo? Empfehlung: MPL 2.0 (wie Firefox) oder MIT.

Antwort:

### F8 – Mindestversion

Nur Firefox 157+ (Nova) unterstützen, oder soll das Theme auch auf ESR/älteren Versionen
brauchbar aussehen?

Empfehlung: `strict_min_version: "157.0"`, nichts Älteres.

Antwort:

### F9 – Offizielle Nova-Manifeste ins Repo?

Mozillas Repo `FirefoxUX/acorn-themes` (die elf Nova-Themes als `manifest.json`) hat keine
Lizenzdatei, ebenso das Extension-Workshop-Repo. Ich habe beides deshalb nur lokal abgelegt
(`docs/firefox-theming/upstream/unlicensed/`, per `.gitignore` ausgeschlossen) und nicht ins
öffentliche Repo gepusht. Soll das so bleiben?

Empfehlung: ja, so lassen. `fetch-docs.sh` holt die Dateien jederzeit wieder.

Antwort:

### F10 – Sprache im Repo

Aktuell: README englisch (wie vorgefunden), `CLAUDE.md`, diese Datei und die Doku-Notizen deutsch.
Passt das, oder alles in einer Sprache? Und Commit-Messages: deutsch oder englisch?

Antwort:

### F11 – Ordnerstruktur

Das Git-Repo liegt in `~/Github/fftheme/fftheme/`, also einen Ordner tiefer als der Ordner, in dem
du Claude gestartet hast. Absicht? Wenn du Claude künftig im äußeren Ordner startest, wird die
`CLAUDE.md` nicht automatisch geladen – besser im inneren Ordner starten oder das Repo eine Ebene
hochziehen.

Antwort:

## Entschieden

### E1 – Git-Arbeitsweise (01.10.2026)

Nach jeder bedeutsamen Änderung committen und pushen. Direkt auf `main`; Branches nur für
Experimente. Bis zum ersten fertigen Theme geht alles auf `main`. → steht in `CLAUDE.md`.
