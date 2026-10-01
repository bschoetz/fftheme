#!/usr/bin/env python3
"""Vergleicht userchrome/simulator.html mit dem echten Firefox.

Misst die Tableiste in Firefox (Chrome-Kontext) und im Simulator (als Seite
geladen) für mehrere Tab-Zahlen: einmal mit Firefox-Standard, einmal mit einem
Stil, der jede Stellschraube verändert. Dessen userChrome.css erzeugt der
Simulator selbst; Firefox wird damit ein zweites Mal gestartet.

    ./simulator.py
"""
import json
import os
import time

from mn import run

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = "file://" + os.path.abspath(f"{HERE}/../../../userchrome/simulator.html")
COUNTS = [6, 12, 40]
TOLERANCE = 0.6  # px
STYLE = {
    "radius": 6, "minHeight": 24, "marginBlock": 2, "gap": 2, "inlinePadding": 4,
    "minWidth": 60, "maxWidth": 180, "fontSize": 12, "lineHeight": 1.4, "selWeight": "600",
    "iconEndMargin": 3, "maskSize": 0.5, "closeMode": "active", "closeSize": 16,
    "sepOn": True, "sepStrength": 60, "sepHeight": 12, "sepWidth": 2,
    "inactiveBg": 8, "inactiveBorder": 30, "hoverBg": 25, "borderWidth": 2, "chromeRadius": 6,
}

THEME = """
const [id, done] = arguments;
const { AddonManager } = ChromeUtils.importESModule("resource://gre/modules/AddonManager.sys.mjs");
AddonManager.getAddonByID(id).then(a => a.enable()).then(() => done(true), e => done(String(e)));
"""
OPEN = """
const icon = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='16' fill='teal'/></svg>";
while (gBrowser.tabs.length < arguments[0]) {
  const html = "<title>Beispielseite mit langem Titel " + gBrowser.tabs.length + "</title><link rel='icon' href=\\"" + icon + "\\">";
  gBrowser.addTab("data:text/html," + encodeURIComponent(html), {
    triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(), skipAnimation: true });
}
for (const tab of gBrowser.tabs) {
  if (tab.pinned) gBrowser.unpinTab(tab);
}
gBrowser.selectedTab = gBrowser.tabs[2];
"""
LOAD = """
// Hintergrund-Tabs laden erst beim Auswählen; ohne das fehlen die Favicons.
const done = arguments[0];
(async () => {
  for (const tab of [...gBrowser.tabs]) {
    gBrowser.selectedTab = tab;
    await new Promise(r => setTimeout(r, 60));
  }
  gBrowser.selectedTab = gBrowser.tabs[2];
  await new Promise(r => setTimeout(r, 1500));
  done(true);
})();
"""
# Dieselbe Struktur wie sim.metrics() im Simulator
MEASURE = """
const cs = el => getComputedStyle(el), q = s => document.querySelector(s);
const strip = q("#TabsToolbar").getBoundingClientRect();
const box = q("#tabbrowser-arrowscrollbox").shadowRoot.querySelector("scrollbox").getBoundingClientRect();
const rect = n => {
  const r = n.getBoundingClientRect();
  if (!r.width && !r.height) return [0, 0, 0, 0];
  return [r.left - strip.left, r.top - strip.top, r.width, r.height].map(x => Math.round(x * 10) / 10);
};
const part = tab => ({
  tab: rect(tab), bg: rect(tab.querySelector(".tab-background")), content: rect(tab.querySelector(".tab-content")),
  icon: rect(tab.querySelector(".tab-icon-image")), labelContainer: rect(tab.querySelector(".tab-label-container")),
  close: rect(tab.querySelector(".tab-close-button")),
  radius: cs(tab.querySelector(".tab-background")).borderTopLeftRadius,
  closeRadius: cs(tab.querySelector(".tab-close-button")).borderTopLeftRadius,
  fontSize: cs(tab.querySelector(".tab-label")).fontSize,
});
const all = [...gBrowser.tabs];
return {
  stripHeight: Math.round(strip.height * 10) / 10,
  windowWidth: innerWidth,
  overflow: q("#tabbrowser-tabs").hasAttribute("overflow"),
  closebuttons: q("#tabbrowser-tabs").getAttribute("closebuttons"),
  visible: all.filter(t => { const r = t.getBoundingClientRect(); return r.left >= box.left - 1 && r.right <= box.right + 1; }).length,
  total: all.length,
  selected: part(gBrowser.selectedTab),
  inactive: part(all[1]),
};
"""
PINNED = """
gBrowser.pinTab(gBrowser.tabs[0]);
return gBrowser.tabs[0].getBoundingClientRect().width;
"""


def firefox(css, simulate):
    def body(client):
        client.cmd("WebDriver:ExecuteAsyncScript", script=THEME, args=["firefox-compact-dark@mozilla.org"])
        out = {"firefox": {}, "sim": {}}
        for n in COUNTS:
            client.js(OPEN, n)
            client.cmd("WebDriver:ExecuteAsyncScript", script=LOAD, args=[])
            time.sleep(1)
            out["firefox"][n] = client.js(MEASURE)
        out["pinned"] = client.js(PINNED)
        if simulate:
            client.cmd("Marionette:SetContext", value="content")
            client.cmd("WebDriver:Navigate", url=SIM)
            time.sleep(1)
            for name, style in (("Standard", {}), ("alles verändert", STYLE)):
                out["sim"][name] = {}
                for n in COUNTS:
                    client.js("sim.set(arguments[0], arguments[1]);", style, {"tabCount": n, "winWidth": 1400})
                    time.sleep(0.3)
                    out["sim"][name][n] = client.js("return sim.metrics();")
                client.js("sim.set(arguments[0], { tabCount: 6, pinned: 1, winWidth: 1400 });", style)
                out["sim"][name]["pinned"] = client.js(
                    "return document.querySelector('#fx .tabbrowser-tab[pinned]').getBoundingClientRect().width;")
            client.js("sim.set(arguments[0], {});", STYLE)
            out["css"] = client.js("return sim.exportCss();")
            client.js("localStorage.clear();")
        return out
    return run(body, css={"userChrome.css": css})


def relative(m):
    """x-Positionen relativ zum Tab: die Scrollposition der Leiste ist kein Stilmerkmal."""
    m = json.loads(json.dumps(m))
    for part in ("selected", "inactive"):
        x0 = m[part]["tab"][0]
        for key in ("tab", "bg", "content", "icon", "labelContainer", "close"):
            if any(m[part][key]):
                m[part][key][0] = round(m[part][key][0] - x0, 1)
    return m


def diff(a, b, path=""):
    if isinstance(a, dict):
        return [d for k in a for d in diff(a[k], b[k], f"{path}.{k}")]
    if isinstance(a, list):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, f"{path}[{i}]")]
    if isinstance(a, (int, float)) and not isinstance(a, bool):
        return [] if abs(a - b) <= TOLERANCE else [f"{path}: Firefox {a}, Simulator {b}"]
    return [] if a == b else [f"{path}: Firefox {a!r}, Simulator {b!r}"]


first = firefox("", simulate=True)
second = firefox(first["css"], simulate=False)
total = 0
for name, result in (("Standard", first), ("alles verändert", second)):
    for n in COUNTS:
        d = diff(relative(result["firefox"][n]), relative(first["sim"][name][n]))
        total += len(d)
        print(f"{name}, {n} Tabs: {len(d)} Abweichungen")
        for line in d:
            print("   " + line)
    d = diff(result["pinned"], first["sim"][name]["pinned"], "angehefteter Tab, Breite")
    total += len(d)
    print(f"{name}, angehefteter Tab: {len(d)} Abweichungen")
    for line in d:
        print("   " + line)
print(f"\nSumme: {total} Abweichungen über {TOLERANCE} px")
