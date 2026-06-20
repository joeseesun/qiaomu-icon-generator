---
name: qiaomu-icon-generator
description: |
  Generate multiple app, favicon, or website icon candidates with either the local QM Icon Studio CLI or Codex built-in image generation with reference icons, then present a contact sheet so the user can choose. Use when building websites or apps and needing reusable icon options.
---

# Qiaomu Icon Generator

用本机 QM Icon Studio CLI 或 Codex 内置生图能力，为网站、App、工具或 Skill 生成多套图标候选，并给用户一张选择稿。

Copyright (c) 向阳乔木
X: https://x.com/vista8
GitHub: https://github.com/joeseesun/

## When To Use

- 新网站、App、Chrome 插件、Skill、CLI 工具需要 favicon、app icon 或品牌入口图标。
- 用户想先看多个方向再选，而不是直接替换生产图标。
- 项目还没有完整品牌系统，但已有名称、域名、用途或一句话描述。

## Method Choice

Use the **QM Icon Studio CLI method** when the user wants deterministic, vector-friendly icons based on Iconify-style symbols, or when they need fast clean SVG candidates.

Use the **Codex bitmap reference method** when the user explicitly asks for Codex built-in image generation, wants richer iOS-style app icons, asks to reference existing icon galleries, or needs a polished raster icon direction before final export.

## Workflow: QM Icon Studio CLI

1. 读取项目上下文：`README.md`、`package.json`、站点域名、已有 `public/` 或 `assets/` 图标、主色 CSS 变量。
2. 提炼一个短英文语义关键词，例如 `rocket`、`globe`、`code`、`book`、`camera`、`music`、`money`。中文需求可以直接传给 CLI；CLI 会先翻译再搜索 Iconify，必要时你也可以手动改成更准确的英文词。
3. 在项目内创建候选目录，默认使用 `design/icon-options/`；如果项目已有设计目录，沿用现有结构。
4. 如果当前机器有 QM Icon Studio CLI，调用：

```bash
node "$HOME/Documents/qm-icon-studio/cli/qm-icon-options.mjs" \
  --name "Product Name" \
  --query "rocket" \
  --count 8 \
  --out design/icon-options \
  --png
```

如果这个本机路径不存在，用 Codex bitmap reference method，或让用户提供自己的图标生成 CLI / 图标参考库路径。

5. 把 `contact-sheet.png` 或 `contact-sheet.svg` 展示给用户，并推荐 2 到 3 个最适合项目气质的方向。
6. 用户确认后，再把选中的 SVG/PNG 复制到目标项目，或打开 QM Icon Studio 继续导出完整平台资源包。

## Workflow: Codex Bitmap Reference Method

Read `references/codex-bitmap-reference-method.md` before using this path.

1. 读取项目上下文：产品名、用途、域名、现有 favicon/app icon、主色、品牌调性、目标平台。
2. 如果用户要参考 Icon Museum，优先使用可用的本机参考库。Joe 的默认路径是 `$HOME/Documents/图片参考生成icon/icon-museum/manifest.json` 和 `icons/`；其他机器可使用用户提供的 manifest / 图片目录。按品类、颜色、用途筛出 6 到 12 个参考方向，但不要复制原图、商标、应用名或独特构图。
3. 在项目内创建候选目录，默认 `design/<product-slug>-icon-options/`，包含 `prompts.md`、`choices.md`、候选 PNG、选择稿和导出尺寸。
4. 使用 Codex 内置 `image_gen`，每个候选单独一次生成。Prompt 必须包含：square app icon, opaque background, no text/letters/numbers/watermark, centered bold symbol, readable at 32px, iOS and web favicon use.
5. 将内置生图输出从 `$CODEX_HOME/generated_images/...` 复制到候选目录，命名为 `option-01.png` 至 `option-10.png`。保留原始生成文件，不删除。
6. 生成 `contact-sheet.png` 和 `favicon-readability-sheet.png`，检查 64px 和 32px 仍可辨认。
7. 用户选中后，运行导出脚本生成 Web/iOS 资产：

```bash
python3 scripts/export_selected_icon.py \
  --source design/qiaomu-music-icon-options/ios-1024/option-05.png \
  --web-out public/icons \
  --web-prefix qiaomu-music-icon \
  --appiconset ios/QiaomuMusic/QiaomuMusic/Assets.xcassets/AppIcon.appiconset
```

8. 把网站入口改为引用真实 PNG favicon/apple-touch icon；iOS 工程则更新 `.appiconset` 里已有尺寸。不要在用户确认前覆盖生产图标。

## Rules

- 不要在用户选择前覆盖现有生产图标。
- 不要把纯装饰图案当成品牌图标；图形必须能在 32px favicon 下辨认。
- 优先生成 6 到 12 个候选，少于 4 个不利于比较，多于 12 个会让选择变累。
- 候选稿默认保留方形源图；iOS、macOS、Windows 等平台圆角和格式留到最终导出阶段处理。
- 如果 PNG 渲染失败，继续使用 SVG 候选稿，并说明 Playwright 不可用。
- 如果外部网络不可用，加 `--offline` 使用内置图标库继续生成候选。
- Codex bitmap reference method 必须避免文字、字母、数字、伪文字、水印、真实商标和对参考图的近似复制。
- Web/iOS 最终资产必须是方形、无透明通道、中心主体有安全边距；iOS App Store master 使用 1024x1024 PNG。
- 若要替换现有网站或 App 图标，先确认用户已选择候选编号，再导出并替换。

## Output

QM Icon Studio CLI 候选目录通常包含：

- `option-01.svg` 至 `option-08.svg`
- `option-01.png` 至 `option-08.png`，如果 Playwright 可用
- `contact-sheet.svg`
- `contact-sheet.png`，如果 Playwright 可用
- `choices.md`
- `qm-icon-options.json`

Codex bitmap reference method 候选目录通常包含：

- `option-01.png` 至 `option-10.png`
- `ios-1024/`
- `web-180/`
- `web-64/`
- `web-32/`
- `contact-sheet.png`
- `favicon-readability-sheet.png`
- `prompts.md`
- `choices.md`
