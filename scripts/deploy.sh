#!/bin/sh
# Run on the host: sh /path/to/pwa/scripts/deploy.sh /path/to/web-root
set -eu

fail() {
    printf 'Deployment stopped: %s\n' "$*" >&2
    exit 1
}

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
    printf 'Usage: sh %s /absolute/path/to/basecentral.link/web-root\n' "$0" >&2
    exit 2
fi
case "$1" in
    /*) ;;
    *) fail 'Use an absolute path to the existing public web directory.' ;;
esac
[ -d "$1" ] || fail 'The public web directory must already exist.'
[ -w "$1" ] || fail 'The public web directory must be writable.'

checkout=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
target=$(CDPATH= cd -- "$1" && pwd -P)
root=$(git -C "$checkout" rev-parse --show-toplevel) || fail 'Run this script from a Git checkout.'
[ "$root" = "$checkout" ] || fail 'The script must live in the checkout scripts directory.'

# Do not expose or overwrite the source checkout, even through symlinked paths.
case "$target/" in "$checkout/"*) fail 'The public web directory must be outside the checkout.' ;; esac
case "$checkout/" in "$target/"*) fail 'The public web directory must not contain the checkout.' ;; esac

git -C "$checkout" symbolic-ref --quiet HEAD >/dev/null || fail 'The checkout must be on a branch.'
git -C "$checkout" rev-parse --verify '@{upstream}' >/dev/null 2>&1 || fail 'The branch must track a remote branch.'
[ -z "$(git -C "$checkout" status --porcelain)" ] || fail 'The checkout must be clean; commit or move local changes first.'

printf 'Pulling %s\n' "$checkout"
git -C "$checkout" pull --ff-only
[ "$(git -C "$checkout" rev-parse HEAD)" = "$(git -C "$checkout" rev-parse '@{upstream}')" ] || fail 'The host branch has local commits; deploy from the remote branch.'

# Validate every asset before changing any published file.
for asset in index.html styles.css favicon.svg; do
    [ -f "$checkout/$asset" ] && [ ! -L "$checkout/$asset" ] || fail "Missing or symlinked source asset: $asset"
    [ ! -L "$target/$asset" ] || fail "Refusing to replace a symlink: $asset"
    if [ -e "$target/$asset" ] && [ ! -f "$target/$asset" ]; then
        fail "The destination is not a regular file: $asset"
    fi
done

umask 022
stage=$(mktemp -d "$target/.pwa-deploy.XXXXXXXX")
cleanup() {
    rm -f "$stage/index.html" "$stage/styles.css" "$stage/favicon.svg" || :
    rmdir "$stage" 2>/dev/null || :
}
trap cleanup 0
trap 'exit 1' 1 2 15

for asset in index.html styles.css favicon.svg; do
    cp "$checkout/$asset" "$stage/$asset"
    chmod 644 "$stage/$asset"
done
# Each replacement is a rename on the same filesystem: no half-written files.
# The three-file set is not one atomic release.
for asset in styles.css favicon.svg index.html; do
    mv -f "$stage/$asset" "$target/$asset"
done

printf 'Deployed commit %s to %s\n' "$(git -C "$checkout" rev-parse --short HEAD)" "$target"
