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
