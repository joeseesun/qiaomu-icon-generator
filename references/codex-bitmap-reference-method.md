# Codex Bitmap Reference Method

Use this method when the user wants richer raster app-icon candidates generated with Codex built-in image generation, especially for iOS-style icons or when they ask to use a local icon-gallery reference library.

## Local Reference Library

This method can use any local icon reference library that has image files and metadata. On Joe's machine, the Icon Museum snapshot usually lives at:

- `/Users/joe/Documents/图片参考生成icon/icon-museum/manifest.json`
- `/Users/joe/Documents/图片参考生成icon/icon-museum/icons/`
- `/Users/joe/Documents/图片参考生成icon/icon-museum/index.html`

If those paths are unavailable, ask the user for a local reference directory or continue from product context without reference images. Use available metadata to search by app name, category, palette, and filename. Treat icons as style references only. Do not copy exact artwork, app marks, names, or distinctive compositions.

Useful queries:

```bash
jq -r '.icons[] | select((.category_names|join(" ")|test("Music|Entertainment";"i")) or (.app_name|test("music|audio|song|sound|dj|album|cassette|playlist|piano|radio|vinyl";"i"))) | [.index,.app_name,(.category_names|join("; ")),.filename,(.palette|join(" "))] | @tsv' /Users/joe/Documents/图片参考生成icon/icon-museum/manifest.json
```

## Prompt Contract

Every generated icon prompt should include:

- Product name and intended use.
- Square app icon, opaque background, no transparency.
- Works for iOS app icon and website favicon.
- Bold centered symbol, safe padding, readable at 32px.
- No text, no letters, no numbers, no pseudo-text, no watermark.
- No existing brand marks and no copying reference icons.
- Palette from the project, not from arbitrary taste.

Example prompt skeleton:

```text
Use case: logo-brand
Asset type: <product> website favicon and iOS app icon candidate <NN>
Primary request: Create one original square app icon for <product>, inspired by curated iOS icon craft but not copying any reference.
Subject: <one strong motif>
Style/medium: premium vector-friendly 3D app icon, clean layered geometry, Apple App Store quality.
Composition/framing: single centered symbol, generous safe padding, bold silhouette readable at 32px.
Color palette: <project colors>
Materials/textures: <short material direction>
Constraints: square master icon, opaque background, no transparency, no rounded-corner mask baked into the subject, no text, no letters, no numbers, no existing brand marks, no watermark.
Avoid: app screenshots, tiny details, illegible pseudo-text, copying any real app icon exactly.
```

## Candidate Directory

Create a project-local directory such as:

```text
design/<product-slug>-icon-options/
```

Recommended files:

- `prompts.md`
- `choices.md`
- `option-01.png` to `option-10.png`
- `contact-sheet.png`
- `favicon-readability-sheet.png`
- `ios-1024/`
- `web-180/`
- `web-64/`
- `web-32/`

Use 6 to 12 candidates. Ten is a good default when the user asks to choose.

## Export Selected Candidate

After the user chooses one candidate, export platform assets:

```bash
python3 scripts/export_selected_icon.py \
  --source design/<product-slug>-icon-options/ios-1024/option-05.png \
  --web-out public/icons \
  --web-prefix <product-slug>-icon \
  --appiconset path/to/AppIcon.appiconset
```

The export script uses Pillow:

```bash
python3 -m pip install pillow
```

For websites, add real PNG references:

```html
<link rel="icon" type="image/png" sizes="32x32" href="/icons/<product-slug>-icon-32.png" />
<link rel="icon" type="image/png" sizes="64x64" href="/icons/<product-slug>-icon-64.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/icons/<product-slug>-icon-180.png" />
<link rel="manifest" href="/site.webmanifest" />
```

For iOS, update the existing `.appiconset` files named by `Contents.json` instead of inventing a new asset catalog unless the project has no app icon yet.

## Qiaomu Music Example

The Qiaomu Music run used this method:

- Candidate directory: `/Users/joe/Documents/图片参考生成icon/design/qiaomu-music-icon-options/`
- Selected candidate: `option-05`, an abstract amber disc that evolves the existing black/gold favicon.
- Final web files: `public/icons/qiaomu-music-icon-32.png`, `64.png`, `180.png`, `192.png`, `512.png`, `1024.png`
- Final iOS files: existing `AppIcon.appiconset/AppIcon-*.png`

Shortlist logic:

- Prefer continuity when a product already has a recognizable favicon.
- Prefer the option that survives 32px best over the most detailed full-size render.
- For music products, strong motifs include disc, waveform, album stack, radio dial, cassette, and turntable. Avoid generic music notes unless explicitly requested.
