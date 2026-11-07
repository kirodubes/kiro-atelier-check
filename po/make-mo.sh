#!/bin/bash
set -euo pipefail
#####################################################################
# Purpose:
# - Extract Python and desktop strings into the gettext template.
# - Merge the template into every catalog and compile each .mo file.
# - Generate the translated desktop entry from its .in template.
#####################################################################

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOMAIN="kiro-atelier-check"
REPO="$(dirname "$SCRIPT_DIR")"
POT="$SCRIPT_DIR/$DOMAIN.pot"
DESKTOP_IN="$SCRIPT_DIR/$DOMAIN.desktop.in"
DESKTOP="$REPO/usr/share/applications/$DOMAIN.desktop"

extract() {
    (cd "$REPO" && xgettext --language=Python --from-code=UTF-8 --keyword=_ --keyword=N_ \
        --keyword=ngettext:1,2 --add-comments=TRANSLATORS --package-name="$DOMAIN" --sort-by-file \
        -o "$POT" usr/bin/kiro-atelier-check)
    (cd "$REPO" && xgettext --language=Desktop --join-existing -o "$POT" "po/$(basename "$DESKTOP_IN")")
    sed -i "s/Project-Id-Version: PACKAGE VERSION/Project-Id-Version: $DOMAIN/" "$POT"
}

merge_and_compile() {
    local po lang mo
    for po in "$SCRIPT_DIR"/*.po; do
        [[ -e "$po" ]] || continue
        lang="$(basename "$po" .po)"
        msgmerge --quiet --update --backup=none "$po" "$POT"
        mo="$REPO/usr/share/locale/$lang/LC_MESSAGES/$DOMAIN.mo"
        mkdir -p "$(dirname "$mo")"
        msgfmt --check --statistics -o "$mo" "$po"
    done
}

write_desktop() {
    find "$SCRIPT_DIR" -maxdepth 1 -name '*.po' -printf '%f\n' | sed 's/\.po$//' | sort > "$SCRIPT_DIR/LINGUAS"
    msgfmt --desktop --template="$DESKTOP_IN" -d "$SCRIPT_DIR" -o "$DESKTOP"
}

main() {
    extract
    merge_and_compile
    write_desktop
    desktop-file-validate "$DESKTOP"
}

main "$@"
