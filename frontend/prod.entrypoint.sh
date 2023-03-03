#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

# Replace env vars in files
echo "Replacing env constants in JS"
for file in $ROOT_DIR/assets/index*.js $ROOT_DIR/index.html; do
  echo "Processing $file ...";
  sed -i 's|VITE_APP_API_BASE_URL|'${VUE_APP_API_BASE_URL}'|g' $file
  sed -i 's|VITE_APP_I18N_FALLBACK_LOCALE|'${VUE_APP_I18N_FALLBACK_LOCALE}'|g' $file
  sed -i 's|VITE_APP_VERSION|'${VUE_APP_VERSION}'|g' $file
done

echo "Starting Nginx"
nginx -g 'daemon off;'
