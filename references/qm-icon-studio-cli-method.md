# QM Icon Studio CLI Method

Use this method when the user wants deterministic, vector-friendly icon candidates that can remain editable as SVG. This path is faster and cleaner than bitmap generation, but usually less expressive than Codex bitmap reference generation.

## Command

```bash
node "$HOME/Documents/qm-icon-studio/cli/qm-icon-options.mjs" \
  --name "Qiaomu Music" \
  --query music \
  --count 8 \
  --out design/qiaomu-music-svg-cli-options \
  --offline
```

Useful flags:

- `--query <keyword>`: semantic icon keyword, such as `music`, `book`, `radar`, `camera`, `money`.
- `--icon <name>`: force a built-in icon or Iconify id.
- `--text <text>`: generate text-mark candidates instead of symbol candidates.
- `--png`: also render PNG files when Playwright is available.
- `--offline`: use the built-in icon library only.

## Expected Output

The CLI produces:

- `option-01.svg` to `option-08.svg`
- `contact-sheet.svg`
- `choices.md`
- `qm-icon-options.json`

If Playwright is available and `--png` is used, it can also produce `option-*.png` and `contact-sheet.png`. If PNG rendering is skipped, that is not a failure; show the SVG contact sheet directly and continue.

## Public Example

The Qiaomu Music SVG CLI example in this repository lives at:

- `docs/assets/examples/qiaomu-music/svg-cli/contact-sheet.svg`
- `docs/assets/examples/qiaomu-music/svg-cli/svg-cli-preview.png`
- `docs/assets/examples/qiaomu-music/svg-cli/svg-cli-readability.png`
- `docs/assets/examples/qiaomu-music/svg-cli/choices.md`
- `docs/assets/examples/qiaomu-music/svg-cli/qm-icon-options.json`

Use this example to explain the CLI path in public docs: it is a quick vector candidate generator, not the final rich iOS-style app icon path.

## Selection Guidance

- Prefer SVG CLI when the product needs a simple favicon, toolbar icon, extension icon, or editable design starting point.
- Prefer Codex bitmap reference generation when the product needs a polished iOS-style app icon or richer material direction.
- Even with SVG candidates, check 64px and 32px readability before recommending a winner.
- Do not overwrite production icons before the user selects a candidate.
