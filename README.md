# fftheme

My idea of a better modern Firefox theme.

Firefox 157 shipped the "Nova" redesign. This project builds a **minimalist, highly usable theme**
for Nova that stays out of the way and is designed for the returning **compact mode**, so the
browser chrome takes as little space and attention as possible.

## Goals

- **Neutral:** the browser is a neutral window in which the content can shine – no tinted chrome,
  no gradients, no decoration without a function.
- **Made for many tabs:** tabs stay legible and take as little horizontal space as possible; no
  rounded corners or gaps that waste room.
- **Usable first:** the active tab, the focused address bar and hover states are obvious at a
  glance; text and icons meet WCAG contrast (4.5:1 text, 3:1 UI elements).
- **Compact-mode native:** designed and tested with the compact density setting.
- **Built on the official theming system:** a WebExtension static theme (`manifest.json`) for
  Firefox 157+.

## Status

Early setup. The theming documentation is collected, the design decisions are still open – see
[`OFFENE_FRAGEN.md`](OFFENE_FRAGEN.md).

## Repository layout

| Path | Content |
| --- | --- |
| [`docs/firefox-theming/`](docs/firefox-theming/) | Firefox theming documentation: German working notes plus unmodified upstream copies (MDN, Firefox source) |
| [`OFFENE_FRAGEN.md`](OFFENE_FRAGEN.md) | Open design and project questions (German) |
| [`CLAUDE.md`](CLAUDE.md) | Working agreements for AI-assisted development (German) |

## What a theme can and cannot do

A static theme sets colors, background images and gradients of the browser chrome. It cannot change
shapes, spacing, icons or layout, and it cannot switch on compact mode – that is a user setting
(Settings → Appearance → Density, or `browser.uidensity = 1` in `about:config`). Details:
[`docs/firefox-theming/README.md`](docs/firefox-theming/README.md).

## Third-party material

`docs/firefox-theming/upstream/mdn/` contains pages from [MDN Web Docs](https://developer.mozilla.org/)
by Mozilla Contributors, licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/).
`docs/firefox-theming/upstream/firefox-source/` contains files from the
[Firefox source code](https://github.com/mozilla-firefox/firefox), licensed under the
[MPL 2.0](https://www.mozilla.org/MPL/2.0/). Firefox is a trademark of the Mozilla Foundation; this
project is not affiliated with Mozilla.
