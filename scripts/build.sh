#!/usr/bin/env sh

npm run dev --prefix frontend
rm -rf static
rm -rf static/css static/js static/media
mkdir -p static
mv frontend/build/index.html static/index.html
mv frontend/build/static/css static/css
mv frontend/build/static/js static/js
mv frontend/build/static/media static/media
mv frontend/build/asset-manifest.json staticasset-manifest.json
mv frontend/build/favicon.ico static/favicon.ico
mv frontend/build/logo192.png static/logo192.png
mv frontend/build/logo512.png static/logo512.png
mv frontend/build/manifest.json static/manifest.json
mv frontend/build/robots.txt static/robots.txt

rm -rf frontend/build
