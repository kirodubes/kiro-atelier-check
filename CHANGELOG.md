# Changelog — kiro-atelier-check

## 2026.11.07 — Public: GitHub + nemesis_repo

### What Changed
- **KA Check is public** (Erik): source on GitHub `kirodubes/kiro-atelier-check`, package in `nemesis_repo`, so
  Kiro and KiroTux users install it with `sudo pacman -S kiro-atelier-check`. Other Arch-based systems get the package
  from the Kiro Atelier Ko-fi page.
- **Freeware licence** replaces the "all rights reserved" notice: free to run and redistribute unchanged (repos,
  mirrors, installation images), no modified versions, no selling.
- **New style gallery photos**: the gallery is now painted on four CC0 / public-domain photos from Wikimedia Commons,
  free to publish with KA Check (a snowy mountain lake, a colourful
  old-town street, a smiling woman in a cornfield, a big wave on rocks), and every profile was painted on them again.
  The fourth photo is "Sea" now (was "Sunset shore"; 1 string in all 13 languages, 127 per catalog).
- **The licence has no version number of its own**: versions are package releases (title "Freeware Licence").
- **README shows what Kiro Atelier paints**: one lake photo in five styles at the top (`docs/styles.jpg`, not in the
  package), a short pitch and the Ko-fi link.
- **Floating World's description is honest about faces**: "Scenes and poses stay; faces take on the woodblock look"
  replaces "People and action scenes stay recognisable" (in the gallery the portrait got Japanese features). Same
  text as Kiro Atelier, all 13 languages; `gallery.json` updated.
- **The Ko-fi card shows the mountain lake** (original, Palette Knife, Poster Studio, Edo Landscape): it shows the
  styles best. Same styles as before, so the caption stays true.

### Technical Details
- Moved from `~/KIROTUX/kiro-atelier-check` to `~/KIRO/kiro-atelier-check`; `up.sh` + `setup.sh` copied from the
  `kiro-gdrive` block (generic). Recipe `~/KIRO-PKG-BUILD-APPS/kiro-atelier-check` (git source), generated
  `flow-kiro-atelier-check` (flows.manifest), replacing the private KIROTUX recipe and hand-written flow.
- Photo sources and licences: KA `tools/gallery-photos/SOURCES.md`.

### Files Modified
- `LICENSE`, `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `up.sh` + `setup.sh` (new),
  `usr/share/kiro-atelier-check/gallery/` (re-exported)

## 2026.11.06 — Ko-fi card, graphics card list

### What Changed
- **Get Kiro Atelier on Ko-fi**: KA Check now points to Kiro Atelier. A card shows one photo in four styles (the original,
  Palette Knife, Poster Studio, Edo Landscape), a short pitch (4K wallpapers, the styles, paints on your own PC so
  photos never leave home), a big orange "Get Kiro Atelier on Ko-fi" button, "See what Kiro Atelier paints" next to
  it and the link itself under it. A PC that can run KA sees the card right under the verdict ("Your PC is ready:
  turn your photos into paintings"); one that can't sees it after the "What you can do" tips, with "Get it once a PC
  in your home passes this check." The terminal report ends with the Ko-fi link.
- 6 new strings in all 13 languages (107 per catalog).
- **Which graphics cards work?** A button under the requirements (and `--cards` in the terminal) lists the cards
  per series, desktop and laptop: meets the requirements / meets them but likely slow (not tested) / doesn't work
  (under 6 GB, too old, not NVIDIA). Note: only the RTX 2060 6 GB is tested; laptop cards paint slower; same-name
  laptop and workstation cards can have different video memory.
- **GTX 16xx and similar cards** (GTX 1660, T1000 8GB …) now get a warning instead of a plain pass: ComfyUI doesn't
  use half precision on them by default, so painting is likely much slower. Tip: an RTX card is the safe choice.
- Requirement line: "an NVIDIA graphics card with at least 6 GB of video memory (RTX 20 series or newer)" (was
  "RTX 20xx or newer, 6 GB", which wrongly suggested every newer card works: RTX 2050 and many RTX 3050 laptops
  have 4 GB).
- More-info texts no longer claim what wasn't measured: no "black pictures", no "many times longer", no "5–10
  minutes" for cards under 6 GB.
- **Translated** after Erik approved the English: the 20 new and changed strings in all 13 languages (124 per
  catalog), each language's existing terms reused (video memory, graphics card, Setup).
- **Second check by Copilot** (gpt-6-luna, `ai-review.py`) over every string of every catalog: 149 findings, 136
  applied automatically, 1 by hand (Russian, line break), 1 rewritten by hand (German: the fix dropped "not tested"
  and turned "settings" into "pictures"), 11 rejected: "KiroTux" → "Kirotux" in French and Dutch (product name),
  Dutch "Koop" → "Haal" on the Ko-fi button (it leads to the Ko-fi page) and "Workstation" → "Werkstation", and Hungarian
  fixes that renamed Kiro Atelier's own "Beállítás" (Setup) page and "A ComfyUI helye" option, which KA Check quotes
  word for word.
- The "doesn't work" rows of the card list held ordinary words ("all versions", "and older", "graphics built into
  the processor") that were never translated: they are `N_()` now, translated in all 13 languages (127 per
  catalog) and checked by Copilot again (3 of 4 fixes applied; the Dutch one called built-in graphics a "card").
  The Russian fix had dropped "RTX 500 Ada" (restored) and "старше" became "и более ранние" (unambiguous); a check
  confirms every card name of the English rows is in every language. "(Max-Q too)" became "(+ Max-Q)".

### Technical Details
- `buy_card()` builds the card; `KOFI_URL` and `HERO_PICTURES` (gallery view pictures, 1280 px, so they stay sharp
  on a wide window) sit next to the gallery constants.
- The pictures keep their shape at any window width: a small `Photo` subclass of `Gtk.Picture` makes the height
  follow the width. The first version had a fixed 100 px height and stretched into thin strips on a full-width
  window (Erik's screen); a plain shrinkable `GtkPicture` has minimum height 0 and got squeezed flat instead. The button opens the link with `Gtk.UriLauncher`; the plain link is a `Gtk.LinkButton`.
- `--cards` opens the card list as its own window on a desktop (`show_cards_window()`, own application id so it
  opens next to a running KA Check); `--cards --text` or no desktop prints it. Kiro Atelier's ☰ menu opens it this
  way. The window CSS moved to a module constant `CSS` + `_add_css()`, shared by both windows.
- `SLOW_CARDS` copies ComfyUI's `nvidia_16_series` list from `comfy/model_management.py` (`should_use_fp16`), same
  case-sensitive match on the card name from `nvidia-smi`. It is a warning heuristic: ComfyUI's `manual_cast` path
  can still pick fp16 when a model is large for the card.
- The 7.5 minimum was confirmed on the test box: Kiro Atelier's PyTorch 2.11.0+cu128 reports
  `get_arch_list()` = sm_75, sm_80, sm_86, sm_90, sm_100, sm_120 (KA pins `whl/cu128` in `setup_checks.py`).
- The card list (`CARD_LIST`) was checked twice: a Claude agent against NVIDIA's own spec pages (TechPowerUp blocked
  it), then a Copilot (gpt-6.1-terra) review online with TechPowerUp and the ComfyUI source. Fixes: RTX A1000/A2000
  laptop split by memory; about 20 workstation laptop cards added; 4 GB cards added to "doesn't work" (RTX 3050 A,
  A400, A500, RTX 500 Ada, T500/T550/T1200/T2000); "works" became "meets the requirements"; "too old" means before
  the RTX 20 / GTX 16 generation (GTX 16 is Turing too). Left out on purpose: datacenter cards (T4, A10, L4), the
  CMP 30HX mining card, and TechPowerUp-only entries not found elsewhere.
- The sunset photo was picked from a contact sheet of every style: its four looks differ the most at thumbnail size
  (the mountain lake ones looked alike).
- Checked off-screen with Broadway + headless Chromium, both the "can run" and the "can't run" window.

### Files Modified
- `usr/bin/kiro-atelier-check`
- `po/*.po`, `po/kiro-atelier-check.pot`, `usr/share/locale/*/LC_MESSAGES/kiro-atelier-check.mo`, `usr/share/applications/kiro-atelier-check.desktop`
- `CHANGELOG.md`, `CLAUDE.md`

## 2026.11.05 — Initial package

### What Changed
- Style gallery: the cat photo is out (Erik: a bad example); 4 photos per profile now (56 pictures, 8.5 MB). The
  "5 photos" texts say 4 in all 13 languages (Russian and Polish number forms adjusted).
- **13 languages** (Dutch, German, Spanish, French, Brazilian Portuguese, Russian, Hungarian, Italian, Turkish,
  Polish, Japanese, Simplified Chinese, Romanian): the window, the style gallery and the terminal report follow the
  system language; a dropdown in the new header bar picks another one (Restart now). Profile names stay English.
- Terminal report: the title column fits the longest title in the language (German and Japanese titles are longer).
- **See what Kiro Atelier paints**: a button under the requirements opens a style gallery, every ready-made
  style on the same 5 photos; a click shows a painting big, arrow keys move on. Pictures in
  `usr/share/kiro-atelier-check/gallery/` (400 px thumbnails, 1280 px views, `gallery.json`, 10.7 MB), exported
  from Kiro Atelier's `tools/style_gallery.py --export`. Standalone code, like the rest of KA Check.
- KA Check becomes its own package, next to Kiro Atelier: a free, read-only check whether a PC can run Kiro
  Atelier, meant for people before they get Kiro Atelier. Menu entry "KA Check" with KA's brush icon plus a green check.
- Checks: Arch-based system, NVIDIA card, working driver, card generation (RTX 20xx / GTX 16xx or newer), 6 GB
  video memory, 16 GB RAM, 20 GB free disk. "More info" on every hard failure gives the technical reason;
  "What you can do" cards explain the next step (another Arch-based Linux PC can do the painting; Windows and
  Mac aren't supported for that).
- Tested on six PCs: one with an RTX 2060 (can), two with Intel graphics only, a laptop with a GTX 1050 Ti (too
  old, 4 GB), a laptop with a GT 620M and 8 GB RAM, a laptop with Intel + AMD graphics and 8 GB RAM.

### Technical Details
- One standalone Python file (no Kiro Atelier imports) so it can also be handed out as a single download.
  GTK 4 window when a desktop is there, terminal report otherwise or with `--text` (`--more` for the reasons).
- Old NVIDIA chips are recognised from the lspci chip name (GF/GK/GM/GP/GV = Fermi to Volta), so a card without
  a working driver is still called too old. Compute capability comes from `nvidia-smi --query-gpu=compute_cap`.
- The window content sits in a scroller that never scrolls sideways: on a tiling desktop GTK otherwise sized
  the window to the longest line and cut text and the Close button off.
- Moved here from Kiro Atelier's `tools/ka-check.py` (its history up to this point is in that repo).

### Files Modified
- `usr/bin/kiro-atelier-check`, `usr/share/applications/kiro-atelier-check.desktop`,
  `usr/share/icons/hicolor/scalable/apps/kiro-atelier-check.svg`,
  `usr/share/icons/hicolor/256x256/apps/kiro-atelier-check.png`,
  `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `LICENSE`, `ruff.toml`, `.codespellrc`, `.gitignore`
