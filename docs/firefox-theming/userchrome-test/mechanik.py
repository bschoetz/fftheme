#!/usr/bin/env python3
"""Prüft, wie Firefox userChrome.css lädt und kaskadiert (Sonden: mechanik.css).

    ./mechanik.py          # Pref an
    ./mechanik.py aus      # Pref aus: nichts darf greifen
"""
import json
import os
import shutil
import sys
import tempfile
import time

from mn import OPEN_TABS, run

HERE = os.path.dirname(os.path.abspath(__file__))
MEASURE = """
const cs = el => getComputedStyle(el);
const v = (el, name) => cs(el).getPropertyValue(name).trim() || null;
const root = document.documentElement;
const tabs = document.getElementById("tabbrowser-tabs");
const tab = gBrowser.tabs[3];
const bg = tab.querySelector(".tab-background");
const up = document.getElementById("tabbrowser-arrowscrollbox").shadowRoot.getElementById("scrollbutton-up");
const marker = {};
for (const n of ["--p-loaded", "--p-compact", "--p-import", "--p-pref-nova", "--p-pref-custom",
                 "--p-pref-missing", "--p-boolpref-old", "--p-late"]) marker[n] = v(root, n);
for (const n of ["--p-shadow-plain", "--p-shadow-cross", "--p-shadow-part"]) marker[n] = v(up, n);
return {
  version: Services.appinfo.version,
  marker,
  "normal: .tab-background border-radius": cs(bg).borderRadius,
  "normal: :root --tab-inline-padding": v(root, "--tab-inline-padding"),
  "!important: .tab-background margin-block": cs(bg).marginBlock,
  "!important: :root --tab-overflow-clip-margin": v(root, "--tab-overflow-clip-margin"),
  "!important gegen inline: --tab-min-width-pref": v(tabs, "--tab-min-width-pref"),
  "inline style auf #tabbrowser-tabs": tabs.getAttribute("style"),
  "Tab-Breite bei 60 Tabs": tab.getBoundingClientRect().width,
};
"""

work = tempfile.mkdtemp(prefix="fftheme-css-")
target = shutil.copy(f"{HERE}/mechanik.css", f"{work}/userChrome.css")
with open(f"{work}/extra.css", "w") as f:
    f.write(":root { --p-import: neben-symlink-ziel; }\n")


def body(client):
    client.js(OPEN_TABS, 59)
    time.sleep(2.5)
    result = client.js(MEASURE)
    # Datei im laufenden Betrieb ändern: wird das nachgeladen?
    with open(target, "a") as f:
        f.write("\n:root { --p-late: yes; }\n")
    time.sleep(2)
    result["marker"]["--p-late"] = client.js(MEASURE)["marker"]["--p-late"]
    return result


pref_on = sys.argv[1:] != ["aus"]
result = run(
    body,
    prefs={"toolkit.legacyUserProfileCustomizations.stylesheets": pref_on, "fftheme.probe": True},
    css={"extra.css": ":root { --p-import: im-profil; }\n"},
    link=("userChrome.css", target),
)
shutil.rmtree(work, ignore_errors=True)
print(json.dumps(result, indent=1, ensure_ascii=False))
