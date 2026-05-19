---
name: html-to-pdf
description: Convert HTML files to PDF using headless Chrome. Use when the user asks to convert an HTML file (.html) to PDF (.pdf), export an HTML document as PDF, or generate a PDF from a web page file. Supports Japanese fonts, complex CSS, and print-optimized layouts. Triggers on requests like "HTMLをPDFに変換", "convert this HTML to PDF", "export as PDF", or "generate PDF from HTML".
---

# HTML to PDF

## Overview

Convert local HTML files to PDF using headless Chrome. Handles Japanese fonts, CSS styling, and complex layouts reliably.

## Quick Start

Run the bundled script directly:

```bash
python scripts/html_to_pdf.py <input.html> [output.pdf]
```

**Defaults:** A4 portrait, no header/footer, output to same directory as input.

## Common Patterns

**Basic conversion:**
```bash
python scripts/html_to_pdf.py report.html
# → report.pdf (same directory)
```

**Specify output path:**
```bash
python scripts/html_to_pdf.py report.html /path/to/output.pdf
```

**Landscape + custom output:**
```bash
python scripts/html_to_pdf.py report.html output.pdf --landscape
```

**Keep Chrome header/footer:**
```bash
python scripts/html_to_pdf.py report.html --with-header
```

## Options

| Option | Default | Description |
|---|---|---|
| `--no-header` | on | Remove Chrome's default header/footer |
| `--with-header` | off | Keep Chrome's default header/footer |
| `--landscape` | off | Landscape orientation |
| `--paper-size` | A4 | A3, A4, A5, Letter, Legal |
| `--scale FLOAT` | 1.0 | Page scale factor (0.1–2.0) |

## Requirements

- **Google Chrome** or **Chromium** must be installed
- Supported locations (auto-detected):
  - macOS: `/Applications/Google Chrome.app`
  - Linux: `/usr/bin/google-chrome`, `/usr/bin/chromium`

## Tips for HTML Authors

- Use `@page { size: A4; margin: 20mm; }` CSS for precise page control
- Use `page-break-before: always` / `break-before: page` for explicit page breaks
- Japanese fonts (Yu Gothic, Hiragino Sans, Noto Sans JP) render correctly with Chrome

## Troubleshooting

**"Chrome/Chromium not found"** — Install Google Chrome or add its path to `CHROME_PATHS` in the script.

**PDF looks different from browser** — Chrome's print rendering differs from screen rendering. Adjust CSS with `@media print {}` rules in the HTML.
