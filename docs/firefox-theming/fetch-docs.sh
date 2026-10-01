#!/usr/bin/env bash
# Lädt die Upstream-Theming-Doku nach upstream/ (neu) herunter.
#
#   ./fetch-docs.sh               # Firefox-Quellen vom release-Branch
#   FX_BRANCH=beta ./fetch-docs.sh
#
# upstream/mdn und upstream/firefox-source werden eingecheckt (CC-BY-SA 2.5 bzw.
# MPL 2.0). upstream/unlicensed ist per .gitignore ausgeschlossen, weil die
# Quell-Repos keine Lizenzdatei haben – siehe README.md in diesem Ordner.
set -euo pipefail
cd "$(dirname "$0")/upstream"

FX_BRANCH="${FX_BRANCH:-release}"
MDN=https://raw.githubusercontent.com/mdn/content/main/files/en-us/mozilla
FX=https://raw.githubusercontent.com/mozilla-firefox/firefox/$FX_BRANCH
ACORN=https://raw.githubusercontent.com/FirefoxUX/acorn-themes/main
EW=https://raw.githubusercontent.com/mozilla/extension-workshop/master

get() {
  mkdir -p "$(dirname "$2")"
  curl -fsSL "$1" -o "$2"
  echo "ok  $2"
}

# --- MDN (Prosa CC-BY-SA 2.5) -------------------------------------------------
WE=$MDN/add-ons/webextensions
get "$WE/manifest.json/theme/index.md"                     mdn/manifest-theme.md
get "$WE/manifest.json/dark_theme/index.md"                mdn/manifest-dark_theme.md
get "$WE/manifest.json/theme_experiment/index.md"          mdn/manifest-theme_experiment.md
get "$WE/manifest.json/browser_specific_settings/index.md" mdn/manifest-browser_specific_settings.md
get "$WE/api/theme/index.md"                               mdn/api-theme.md
get "$WE/api/theme/theme/index.md"                         mdn/api-theme-Theme.md
get "$WE/api/theme/update/index.md"                        mdn/api-theme-update.md
get "$WE/api/theme/getcurrent/index.md"                    mdn/api-theme-getCurrent.md
get "$WE/api/theme/reset/index.md"                         mdn/api-theme-reset.md
get "$WE/api/theme/onupdated/index.md"                     mdn/api-theme-onUpdated.md
get "$MDN/firefox/releases/157/index.md"                   mdn/firefox-157-for-developers.md

# --- Firefox-Quellcode (MPL 2.0) ----------------------------------------------
get "$FX/toolkit/components/extensions/schemas/theme.json"        firefox-source/theme.schema.json
get "$FX/browser/themes/ThemeVariableMap.sys.mjs"                 firefox-source/ThemeVariableMap.sys.mjs
get "$FX/toolkit/modules/LightweightThemeConsumer.sys.mjs"        firefox-source/LightweightThemeConsumer.sys.mjs
get "$FX/toolkit/mozapps/extensions/default-theme/manifest.json"  firefox-source/default-theme.manifest.json
get "$FX/toolkit/themes/shared/design-system/docs/README.design-tokens.stories.md" \
                                                                  firefox-source/design-tokens.md
get "$FX/browser/config/version.txt"                              firefox-source/version.txt

# --- Ohne Lizenzdatei: nur lokal, nicht eingecheckt ---------------------------
get "$ACORN/README.md"                         unlicensed/acorn-themes/README.md
get "$ACORN/schemas/README.md"                 unlicensed/acorn-themes/schemas/README.md
get "$ACORN/schemas/firefox-theme.schema.json" unlicensed/acorn-themes/schemas/firefox-theme.schema.json
get "$ACORN/themes/legacy/proton/manifest.json" unlicensed/acorn-themes/themes/legacy/proton/manifest.json
for t in ash dusk flame flare lagoon lavender pine smoke spark sun tide; do
  get "$ACORN/themes/nova/$t/manifest.json" "unlicensed/acorn-themes/themes/nova/$t/manifest.json"
done
get "$EW/src/content/documentation/themes/static-themes.md" unlicensed/extension-workshop/static-themes.md

{
  echo "Abgerufen:       $(date -u +%Y-%m-%d)"
  echo "Firefox-Branch:  $FX_BRANCH"
  echo "Firefox-Version: $(cat firefox-source/version.txt)"
} > STAND.txt
cat STAND.txt
