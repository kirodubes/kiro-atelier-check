# kiro-atelier-check — Claude instructions

## What this is
KA Check: a free, read-only check whether a PC can run Kiro Atelier (sibling repo `~/KIROTUX/kiro-atelier`, private).
The whole tool is `usr/bin/kiro-atelier-check`, one standalone Python file. Keep it standalone: no imports from
Kiro Atelier, so it can also be offered as a single-file download.

## Rules — do not break
- **Public since 2026-11-07** (Erik): GitHub `kirodubes/kiro-atelier-check`, package in `nemesis_repo`
  (recipe `~/KIRO-PKG-BUILD-APPS/kiro-atelier-check`, generated `flow-kiro-atelier-check`; the build also copies the
  package to `~/Insync/KoFi/`). Freeware licence (`LICENSE`): free to run and redistribute unchanged, no modified
  versions, no selling. Everything here is public: no hostnames, LAN addresses or private photos.
- The style gallery comes from KA's `tools/style_gallery.py --export`, painted on CC0 / public-domain photos only
  (KA `tools/gallery-photos/SOURCES.md`). Never export a gallery made from photos we may not publish.
- Never `cd` into `usr/` (use absolute paths): the harness drops a `.claude/` folder in the cwd.
- Read-only: the check never installs, starts or changes anything. Text for users: plain words, no jargon in
  the main line; the technical reason goes in `more` ("More info").
- Python: `ruff check` before done (`ruff.toml` here), lines ≤ 120.

## Keep in step with Kiro Atelier
The thresholds mirror KA's real needs: `MIN_VRAM_GB` (KA `setup_checks.MIN_VRAM_GB`), compute 7.5 (KA's PyTorch is
the cu128 build), RAM (ComfyUI with SDXL + naming model ~10 GB), disk (ComfyUI + PyTorch ~6 GB, models ~7.5 GB).
Change them here when KA's Setup or models change.
`CARD_LIST` (the "Which graphics cards work?" window, `--cards`) follows the same rule (Turing+, 6 GB; `SLOW_CARDS` =
ComfyUI's `nvidia_16_series` list → warning). Recheck it when NVIDIA ships new cards or the rule changes. Only the
RTX 2060 6 GB is tested: never word the list or texts as "works" or with times that weren't measured.
**Coupling**: README "Which graphics cards work?" is a copy of `CARD_LIST` + `CARD_NOTE`; change both together.

## Ko-fi card (2026.11.06)
- `buy_card()` points to KA on Ko-fi: link `KOFI_URL` (button, link and the last line of `--text`). Under the verdict when
  the PC can run KA, after the tips when it can't. Keep it honest: never promise what KA doesn't do.
- **Coupling**: the caption names the 4 `HERO_PICTURES` styles; change both together (and the 13 `.po`).

## Testing
Run `--text` over ssh on the test boxes; to show the window on a box's screen, start it with the environment of
a running desktop process (all variables, not only WAYLAND_DISPLAY). Never on Erik's own screens.

## Translations (2026-11-05)
- 13 languages (nl de es fr pt_BR ru hu it tr pl ja zh_CN ro), 145 strings (2026-11-08), domain `kiro-atelier-check`.
  `usr/share/kiro-atelier-check/kac_i18n.py` (env pin `KAC_LANGUAGE`, choice in `~/.config/kiro-atelier-check/
  prefs.json`); the script adds that folder to `sys.path` from its own location (works installed and from the repo).
  Header bar with the language dropdown + Restart now. Window and `--text` report both translated; the title column
  of `--text` fits the longest title (CJK counts double).
- Round: Copilot did the plumbing and reused 23 strings from KA's catalogs, then stopped; Claude translated the other
  79 per language (4 parallel agents, KA's catalogs as glossary), `ai-review.py` ×13 → 101 fixes applied, 0 rejected.
  French uses "Go" like KA's French (checked by Erik).
- **Coupling**: the gallery's settings lines ("strength 0.65 · impasto · 3840 × 2160") and profile descriptions are an
  `N_()` list in the script so xgettext finds them; after changing a profile in KA and re-exporting the gallery, update
  that list too, or the new line shows in English. The export also writes `detail/` (KA's chooser close-ups):
  delete it here, KA Check never shipped it.
- After changing English text: `bash po/make-mo.sh`, translate the new entries in all 13 `.po`, run it again.
- Second check: `ai-review.py <lang> po/<lang>.po --register … --model gpt-6-luna --out …` per language, then
  `apply-review.py`. Reject fixes that rename KiroTux or change text quoted from KA's own screens (Setup page,
  "ComfyUI runs on"): those must match KA's catalog for that language.
  After applying, check that every card name of the `CARD_LIST` rows is still in each language: a Copilot fix
  dropped "RTX 500 Ada" from the Russian row (2026-11-06).
