#!/usr/bin/env python3
"""Misst, was das Überschreiben von CSS-Variablen in userChrome.css bewirkt.

    ./variablen.py                 # alle Varianten
    ./variablen.py basis tokens    # einzelne Varianten

Gemessen werden berechnete Styles und Layout, kein Bild. Ob es gut aussieht,
zeigt nur der echte Browser.
"""
import json
import sys
import time

from mn import OPEN_TABS, run

VARIANTS = {
    "basis": "",
    "tab-variablen": """:root {
  --tab-border-radius: 0 !important;
  --tab-margin-block: 0px !important;
  --tab-overflow-clip-margin: 0px !important;
  --tab-inline-padding: 2px !important;
}
#tabbrowser-tabs { --tab-min-width-pref: 40px !important; }
""",
    "tokens": """:root {
  --border-radius-xsmall: 0 !important;
  --border-radius-small: 0 !important;
  --border-radius-medium: 0 !important;
  --border-radius-large: 0 !important;
  --border-radius-xlarge: 0 !important;
  --border-radius-circle: 0 !important;
}
""",
    "stern": "* { border-radius: 0 !important; }\n",
}
MEASURE = """
const cs = el => getComputedStyle(el);
const q = s => document.querySelector(s);
const radius = {};
for (const s of [".tabbrowser-tab .tab-background", ".tab-close-button", ".urlbar-background",
                 ".urlbar-input-container", "#back-button > .toolbarbutton-icon",
                 "#PanelUI-menu-button > .toolbarbutton-badge-stack",
                 "#tabs-newtab-button > .toolbarbutton-icon",
                 "#tracking-protection-icon-container"]) {
  const el = q(s);
  radius[s] = el ? cs(el).borderRadius : "(nicht gefunden)";
}
const tabs = gBrowser.tabs;
const a = tabs[2].querySelector(".tab-background").getBoundingClientRect();
const b = tabs[3].querySelector(".tab-background").getBoundingClientRect();
const strip = q("#TabsToolbar").getBoundingClientRect();
const box = q("#tabbrowser-arrowscrollbox").getBoundingClientRect();
return {
  radius,
  "Tab-Hintergrund": { breite: a.width, hoehe: a.height, abstandOben: a.top - strip.top,
                       abstandUnten: strip.bottom - a.bottom, lueckeZumNachbarn: b.left - a.right },
  "Tab-Breite": tabs[2].getBoundingClientRect().width,
  "Innenabstand .tab-content": cs(tabs[2].querySelector(".tab-content")).padding,
  "Hoehe Tableiste": strip.height,
  "Hoehe Navigationsleiste": q("#nav-bar").getBoundingClientRect().height,
  "Tabs im sichtbaren Bereich (60 offen, Fenster 1400px)": [...tabs].filter(t => {
    const r = t.getBoundingClientRect();
    return r.left >= box.left - 1 && r.right <= box.right + 1;
  }).length,
};
"""


def body(client):
    client.js(OPEN_TABS, 59)
    time.sleep(2.5)
    return client.js(MEASURE)


for name in sys.argv[1:] or VARIANTS:
    print(f"== {name}")
    print(json.dumps(run(body, css={"userChrome.css": VARIANTS[name]}), indent=1, ensure_ascii=False))
