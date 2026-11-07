# KA Check (kiro-atelier-check)

**KA Check** tells whether a PC can run **Kiro Atelier** (KA), before anyone gets it. It is free, installs and
changes nothing, and gives one plain verdict: "This PC can run Kiro Atelier" or "This PC can't run Kiro Atelier",
with the reason per check and what the user can do about it.

## What it checks

| Check | Needed |
|---|---|
| Linux system | Arch-based (pacman): Kiro, KiroTux, Arch |
| Graphics card | NVIDIA (Intel and AMD are not supported) |
| NVIDIA driver | working (`nvidia-smi`) |
| Card generation | Turing or newer (RTX 20xx / GTX 16xx, compute 7.5) |
| Video memory | 6 GB |
| Memory (RAM) | 16 GB (12–15 GB gives a warning) |
| Free disk space | about 20 GB in the home folder |

Hard failures carry a "More info" with the technical reason. When the card is the problem, "What you can do"
explains how another Arch-based Linux PC in the home can do the painting ("Another computer" mode).

## What it ships

- `/usr/bin/kiro-atelier-check` — the whole tool, one standalone Python file (no Kiro Atelier imports)
- `/usr/share/applications/kiro-atelier-check.desktop` — menu entry "KA Check"
- `/usr/share/icons/hicolor/{scalable,256x256}/apps/kiro-atelier-check.*` — KA's brush with a green check

## How to install and run

On Kiro and KiroTux it comes from `nemesis_repo`. On other Arch-based systems, download the package for free from
[KA Check on Ko-fi](https://ko-fi.com/s/313e890205) and install the file.

```
sudo pacman -S kiro-atelier-check                        # Kiro, KiroTux
sudo pacman -U kiro-atelier-check-*.pkg.tar.zst          # other Arch-based systems
kiro-atelier-check            # window (GTK 4); falls back to the terminal without a desktop
kiro-atelier-check --text     # terminal report; add --more for the technical reasons
```

The file also runs on its own (`python3 kiro-atelier-check`), which is how it can be offered as a single
download. Exit code: 0 = can run, 1 = can't, 2 = can run with a warning.

## Languages

English, Dutch, German, Spanish, French, Brazilian Portuguese, Russian, Hungarian, Italian, Turkish, Polish,
Japanese, Simplified Chinese and Romanian: KA Check follows the system language, and the dropdown at the top right
picks another one. Catalogs live in `po/`; `bash po/make-mo.sh` extracts, merges and compiles them.
