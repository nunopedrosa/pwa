# App-owned publication contract; common engine: BaseCentral deploy 1.0.0.
APP_ID=pwa
SOURCE_SUBDIR=.
DEFAULT_DESTINATION=''
DEPLOY_URL=https://basecentral.link
PUBLIC_FILES=$(cat <<'PUBLIC_FILES'
assets/BaseCentral.jpg
favicon.svg
index.html
styles.css
PUBLIC_FILES
)

deploy_validate(){
  local expected
  deploy_path "$DEPLOY_CHECKOUT" apps.txt yes
  git -C "$DEPLOY_CHECKOUT" ls-files --error-unmatch -- apps.txt >/dev/null 2>&1 || deploy_fail 'apps.txt must be committed.'
  expected=$(deploy_sha "$DEPLOY_CHECKOUT/apps.txt")
  grep -Fq "name=\"directory-config\" content=\"$expected\"" "$1/index.html" || deploy_fail 'Directory list changed: run python3 scripts/build-directory.py locally and commit the generated HTML.'
}
