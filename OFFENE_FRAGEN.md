# Offene Fragen

Hier sammelt Claude Fragen, die nur du entscheiden kannst. Antworte einfach unter der jeweiligen
Frage (oder im Chat) – entschiedene Fragen wandern nach unten in „Entschieden“.

Reihenfolge = Dringlichkeit. F2 und F12 bestimmen, was wir überhaupt bauen.

## Offen

### F2 – Reines Theme oder auch `userChrome.css`?

| Variante | Kann | Preis |
| --- | --- | --- |
| **A: Static Theme** (`manifest.json`) | Farben, Verläufe, Bilder; hell + dunkel | offiziell, update-fest, auf AMO veröffentlichbar |
| **B: `userChrome.css`** | alles: Ecken, Abstände, Höhen, Icons, Elemente ausblenden | inoffiziell, kann mit jedem Firefox-Update brechen, manuelle Installation ins Profil, nicht über AMO verteilbar |
| **C: beides** | Theme für Farben, CSS für Form und Dichte | zwei Dinge zu pflegen |

Dazu kommen `about:config`-Einstellungen, die ohne Theme und ohne CSS wirken:
`browser.uidensity = 1` (kompakt) und `browser.tabs.tabMinWidth` (Standard 76 px, Untergrenze 50 px).

`theme_experiment` (Theme mit eigenem Stylesheet) scheidet aus: läuft nur in Nightly und Developer
Edition.

Nach deiner Antwort auf F1 (→ E2) deckt **A** nur die neutralen Farben ab. Eckige, lückenlose und
schmalere Tabs gehen nur mit `userChrome.css`.

Empfehlung: **C**. Das Theme bleibt für sich allein nutzbar und robust; das CSS ist ein kleiner,
dokumentierter Zusatz für Form und Tab-Breite, den wir nach Firefox-Updates prüfen.

Antwort:

### F12 – „Horizontale Breite“: was genau?

Ich habe es so verstanden: Die **einzelnen Tabs** sollen schmal sein, damit viele nebeneinander
passen, bevor die Tableiste scrollt. Richtig? Oder ging es (auch) darum, dass keine Sidebar bzw.
vertikale Tableiste dem Seiteninhalt Breite wegnimmt?

Daran anschließend: Was darf bei schmalen Tabs wegfallen – der Schließen-Knopf auf inaktiven Tabs
(Schließen per Mittelklick / Strg+W), die Lücken zwischen Tabs, der Innenabstand?

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

### E2 – Was am neuen Design stört (ehemals F1, 01.10.2026)

- **Farben:** Ein Browser soll ein neutrales Fenster sein, in dem die Inhalte wirken.
- **Tabs:** Sehr viele Tabs offen; sie sollen gut lesbar und kompakt sein. Vor allem die
  horizontale Breite zählt – nichts darf unnötig breit sein.
- **Runde Ecken:** das Gegenteil von platzökonomisch.

→ Leitlinien im README ergänzt. Folgefragen: F2 (Ansatz), F12 (Breite genau).
