"""Translations: gettext catalogs from usr/share/locale, in the chosen language or the system's, else English."""

import gettext
import json
import os
from pathlib import Path

DOMAIN = "kiro-atelier-check"
LOCALE_DIR = Path(__file__).resolve().parent.parent / "locale"
PREFS_FILE = Path.home() / ".config" / DOMAIN / "prefs.json"

NAMES = {
    "en": "English", "nl": "Nederlands", "de": "Deutsch", "es": "Español", "fr": "Français",
    "pt_BR": "Português (Brasil)", "ru": "Русский", "hu": "Magyar", "it": "Italiano", "tr": "Türkçe",
    "pl": "Polski", "ro": "Română", "zh_CN": "简体中文", "ja": "日本語",
}


def available():
    """Return English and every language with a compiled catalog."""
    catalogs = sorted(path.parent.parent.name for path in LOCALE_DIR.glob(f"*/LC_MESSAGES/{DOMAIN}.mo"))
    return ["en", *catalogs]


def name(code):
    """Return the language's own name, or the code itself."""
    return NAMES.get(code) or NAMES.get(code.split("_")[0]) or code


def _saved_choice():
    try:
        prefs = json.loads(PREFS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(prefs, dict):
        return None
    return prefs.get("language")


def chosen():
    """Return the saved language, or None to follow the system."""
    code = _saved_choice()
    return code if code in available() else None


def save_choice(code):
    """Save the selected language; None follows the system again."""
    PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PREFS_FILE.write_text(json.dumps({"language": code}, indent=2) + "\n", encoding="utf-8")


def _system_language():
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var, "").split(":")[0].split(".")[0]
        if value:
            return value
    return "en"


_SIBLING = {"pt": "pt_BR", "zh": "zh_CN"}


def _shown(code):
    codes = available()
    base = code.split("_")[0]
    for candidate in (code, base, _SIBLING.get(base)):
        if candidate in codes:
            return candidate
    return "en"


SYSTEM = _shown(_system_language())
ACTIVE = os.environ.get("KAC_LANGUAGE") or chosen()
_SYSTEM_LANGUAGE_VAR = os.environ.get("LANGUAGE")
if ACTIVE:
    os.environ["LANGUAGE"] = ACTIVE

_translation = gettext.translation(DOMAIN, localedir=LOCALE_DIR, languages=[ACTIVE or SYSTEM], fallback=True)
_ = _translation.gettext
ngettext = _translation.ngettext


def N_(text):
    """Mark a string for translation without translating it here."""
    return text


def restore_environment():
    """Restore LANGUAGE so a restarted app follows the real system setting."""
    if _SYSTEM_LANGUAGE_VAR is None:
        os.environ.pop("LANGUAGE", None)
    else:
        os.environ["LANGUAGE"] = _SYSTEM_LANGUAGE_VAR
