# Offene Fragen

Hier sammelt Claude Fragen, die nur du entscheiden kannst. Antworte einfach unter der jeweiligen
Frage (oder im Chat) – entschiedene Fragen wandern nach unten in „Entschieden“.

Reihenfolge = Dringlichkeit.

## Offen

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

Seit E5 hieße „hell“: ein zweiter Farbblock in der `userChrome.css`, der über „Firefox Hell“ liegt. Der
Simulator erzeugt ihn schon; das Beispiel „neutral hell“ ist in Firefox 157.0 geprüft.

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

### F7 – Name, ID, Lizenz

- Name des Themes (Arbeitstitel `fftheme`)?
- Add-on-ID, z. B. `fftheme@bschoetz` – einmal vergeben, später nicht mehr änderbar, ohne dass es
  als neues Add-on gilt.
- Lizenz für das Repo? Empfehlung: MPL 2.0 (wie Firefox) oder MIT.

Seit E5 gibt es kein signiertes Theme mehr; eine Add-on-ID brauchen wir damit nicht. Offen bleiben
Name und Lizenz.

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

### E3 – Tab-Form zum Ausprobieren (01.10.2026)

Tabs mit nur leichter Eckenrundung (statt ganz eckig, wie in E2 notiert) und erkennbarer Trennung
zwischen inaktiven Tabs. Erste Fassung von Claude: Radius 4 px, Trennlinie in 50 % der Textfarbe.

Zwischenstand von dir, im Simulator eingestellt (01.10.2026): Radius 8 px auch für Adressfeld und
Buttons, kein Abstand über und unter den Tabs, Lücke 2 px, Mindestbreite 68 px, Schrift 15 px,
Trennlinie 18 px hoch. → `userchrome/userChrome.css`, Einzelheiten in `STAND.md`.

### E4 – Farben, erster Stand (01.10.2026)

Im Simulator eingestellt, ausgehend vom Beispiel „neutral dunkel“: Leiste und Navigationsleiste
`#1e1e1e`, aktiver Tab `#472200` mit Rand `#e66100`, Adressfeld `#000000`. Seit E5 im Farbblock der
`userchrome/userChrome.css`.
Berührt F3 (bisher nur dunkel) und F4 (Grau mit Orange als Akzent); beide bleiben offen, bis du den
Stand im echten Browser gesehen hast.

Nachtrag 01.10.2026: Das Orange ist wieder raus. Der aktive Tab ist grau, die Oberfläche damit rein
grau ohne Akzentfarbe.

### E5 – Farben per `userChrome.css` über „Firefox Dunkel“ (ehemals F2, F6, F13; 01.10.2026)

Alles steht in einer Datei, der `userChrome.css`: Form und Farben. Die Farben liegen als eigener
Block über dem eingebauten Theme „Firefox Dunkel“ und gelten nur, solange es ausgewählt ist. Ein
eigenes, signiertes Theme gibt es nicht mehr; für die Weitergabe ist damit nur das CSS zu
installieren.

Grund: Ein unsigniertes Theme hält in Release-Firefox nur bis zum Neustart, und jede Änderung an der
`userChrome.css` braucht einen Neustart. Signieren hätte ein Konto auf addons.mozilla.org verlangt
und zwei Installationswege für andere bedeutet.

Bewusst in Kauf genommen: keine Veröffentlichung auf addons.mozilla.org; die Farben hängen an
Firefox-internen Variablen; was der Block nicht überschreibt, bleibt „Firefox Dunkel“ (Menüs,
Sidebar, Akzentfarbe und Fokusring in Nova-Lila).

`theme/manifest.json` bleibt als geparkter Stand im Repo und wird nicht mehr gepflegt.
