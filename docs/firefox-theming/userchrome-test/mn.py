"""Minimaler Marionette-Client für Messungen an der Firefox-Oberfläche.

Startet das installierte Firefox headless mit einem Wegwerf-Profil (kein Fenster,
das eigene Profil bleibt unberührt), führt JavaScript im Chrome-Kontext aus und
beendet Firefox wieder. Braucht nur Python 3 und `firefox` im PATH.
"""
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time

PORT = 28281
PREFS = {
    "marionette.port": PORT,
    "toolkit.legacyUserProfileCustomizations.stylesheets": True,
    "browser.uidensity": 1,
    "browser.shell.checkDefaultBrowser": False,
    "browser.aboutwelcome.enabled": False,
    "browser.startup.page": 0,
    "browser.startup.homepage": "about:blank",
    "browser.newtabpage.enabled": False,
    "datareporting.policy.dataSubmissionEnabled": False,
    "datareporting.healthreport.uploadEnabled": False,
}

OPEN_TABS = """
for (let i = 0; i < arguments[0]; i++) {
  gBrowser.addTab("about:blank", {
    triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal(),
    skipAnimation: true,
  });
}
return gBrowser.tabs.length;
"""


def _recv(sock):
    buf = b""
    while b":" not in buf:
        buf += sock.recv(1)
    length, rest = buf.split(b":", 1)
    while len(rest) < int(length):
        rest += sock.recv(int(length) - len(rest))
    return json.loads(rest)


class Client:
    def __init__(self):
        for _ in range(120):
            try:
                self.sock = socket.create_connection(("127.0.0.1", PORT), timeout=60)
                break
            except OSError:
                time.sleep(0.5)
        else:
            raise SystemExit("Marionette nicht erreichbar")
        _recv(self.sock)
        self.id = 0

    def cmd(self, name, **params):
        self.id += 1
        msg = json.dumps([0, self.id, name, params]).encode()
        self.sock.sendall(str(len(msg)).encode() + b":" + msg)
        _, _, error, result = _recv(self.sock)
        if error:
            raise RuntimeError(f"{name}: {error['message']}")
        return result

    def js(self, script, *args):
        return self.cmd("WebDriver:ExecuteScript", script=script, args=list(args))["value"]


def run(body, prefs=None, css=None, link=None):
    """Startet Firefox, ruft body(client) auf und gibt dessen Ergebnis zurück.

    css:  {Dateiname: Inhalt} für <Profil>/chrome/
    link: (Dateiname, Ziel) – Symlink in <Profil>/chrome/
    """
    prof = tempfile.mkdtemp(prefix="fftheme-prof-")
    os.mkdir(f"{prof}/chrome")
    with open(f"{prof}/user.js", "w") as f:
        for key, value in {**PREFS, **(prefs or {})}.items():
            f.write(f"user_pref({json.dumps(key)}, {json.dumps(value)});\n")
    for name, text in (css or {}).items():
        with open(f"{prof}/chrome/{name}", "w") as f:
            f.write(text)
    if link:
        os.symlink(os.path.abspath(link[1]), f"{prof}/chrome/{link[0]}")
    proc = subprocess.Popen(
        ["firefox", "--headless", "--no-remote", "--marionette",
         "-remote-allow-system-access", "--width", "1400", "--height", "500",
         "-profile", prof],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        client = Client()
        client.cmd("WebDriver:NewSession", capabilities={})
        client.cmd("Marionette:SetContext", value="chrome")
        result = body(client)
        try:
            client.cmd("Marionette:Quit", flags=["eForceQuit"])
        except Exception:
            pass
        return result
    finally:
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(prof, ignore_errors=True)
