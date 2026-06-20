# Contributing

Thanks for improving `qiaomu-icon-generator`.

Useful contributions include:

- clearer icon-generation prompts
- additional export targets
- better favicon readability checks
- docs for non-Qiaomu environments
- bug reports with the exact command, source image size, and output path

Before opening a pull request:

1. Run `python3 -m py_compile scripts/export_selected_icon.py`.
2. Test `python3 scripts/export_selected_icon.py --help`.
3. If editing `SKILL.md`, run `npx skills add . --list` from the repo root.
4. Do not include copyrighted reference icon files, private app assets, or generated images that copy existing brand marks.

Pull requests should include a short summary, verification commands, and screenshots or output paths when relevant.
