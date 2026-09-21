#!/usr/bin/env bash
# scaffold_site.sh <repo-dir> <accent-hex> <accent2-hex> <monogram> <og-image-tagline>
# Copies the shared design-system kit into <repo>/website/assets and applies the
# per-project theme overrides + generates favicon, robots.txt, sitemap and OG image.
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
REPO="$1"
ACCENT="$2"
ACCENT2="$3"
MONO="$4"
TAGLINE="$5"

NAME="$(basename "$REPO")"
SITE="$REPO/website"
ASSETS="$SITE/assets"

mkdir -p "$ASSETS"
cp "$KIT/site.css" "$ASSETS/site.css"
cp "$KIT/site.js" "$ASSETS/site.js"

cat >> "$ASSETS/site.css" <<EOF

/* ---- $NAME theme ---- */
:root {
  --accent: #$ACCENT;
  --accent-2: #$ACCENT2;
  --accent-glow: rgba($(printf '%d' 0x${ACCENT:0:2}), $(printf '%d' 0x${ACCENT:2:2}), $(printf '%d' 0x${ACCENT:4:2}), 0.22);
}
EOF

# favicon
cat > "$SITE/favicon.svg" <<EOF
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#$ACCENT"/>
  <text x="32" y="45" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="36" font-weight="700" fill="#0b0e14" text-anchor="middle">$MONO</text>
</svg>
EOF

# robots + sitemap
cat > "$SITE/robots.txt" <<EOF
User-agent: *
Allow: /

Sitemap: https://honeyamn10-source.github.io/$NAME/sitemap.xml
EOF

cat > "$SITE/sitemap.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://honeyamn10-source.github.io/$NAME/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
EOF

# og image (PNG, real raster via Pillow)
"/tmp/opencode/tools-venv/bin/python" "$KIT/og_make.py" "$SITE/og.png" "$NAME" "$TAGLINE" "$ACCENT" "$ACCENT2" "$MONO"

touch "$SITE/.nojekyll"
echo "scaffolded $SITE"