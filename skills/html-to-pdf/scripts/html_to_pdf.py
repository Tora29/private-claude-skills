#!/usr/bin/env python3
"""
HTML to PDF converter using headless Chrome.

Usage:
    python html_to_pdf.py <input.html> [output.pdf] [options]

Options:
    --no-header          Remove default header/footer (default: enabled)
    --landscape          Landscape orientation (default: portrait)
    --paper-size SIZE    Paper size: A4, A3, Letter (default: A4)
    --scale FLOAT        Page scale factor 0.1–2.0 (default: 1.0)
    --margin MARGIN      Margin in CSS format e.g. "10mm" (default: system default)

Examples:
    python html_to_pdf.py report.html
    python html_to_pdf.py report.html output.pdf
    python html_to_pdf.py report.html output.pdf --no-header --landscape
"""

import argparse
import subprocess
import sys
from pathlib import Path


CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]

PAPER_SIZES = {
    "A3": (297, 420),
    "A4": (210, 297),
    "A5": (148, 210),
    "Letter": (216, 279),
    "Legal": (216, 356),
}


def find_chrome():
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    raise RuntimeError(
        "Chrome/Chromium not found. Install Google Chrome or Chromium."
    )


def convert(input_html: str, output_pdf: str = None, no_header: bool = True,
            landscape: bool = False, paper_size: str = "A4", scale: float = 1.0,
            margin: str = None):
    input_path = Path(input_html).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_pdf is None:
        output_pdf = input_path.with_suffix(".pdf")
    output_path = Path(output_pdf).resolve()

    chrome = find_chrome()

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={output_path}",
    ]

    if no_header:
        cmd.append("--print-to-pdf-no-header")
        cmd.append("--no-pdf-header-footer")

    if landscape:
        cmd.append("--landscape")

    if paper_size in PAPER_SIZES:
        w, h = PAPER_SIZES[paper_size]
        if landscape:
            w, h = h, w
        cmd.append(f"--virtual-time-budget=5000")

    if scale != 1.0:
        cmd.append(f"--force-device-scale-factor={scale}")

    if margin:
        # Passed as virtual printer margins via JS injection is complex;
        # instead we rely on CSS @page in the HTML itself for margin control.
        print(f"Note: --margin option requires @page CSS rules in the HTML. "
              f"Ignoring --margin={margin}.")

    cmd.append(f"file://{input_path}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"Chrome exited with code {result.returncode}:\n{result.stderr}"
        )

    if not output_path.exists():
        raise RuntimeError(f"PDF not generated at {output_path}")

    size_kb = output_path.stat().st_size // 1024
    print(f"✅ PDF saved: {output_path} ({size_kb} KB)")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML to PDF using headless Chrome"
    )
    parser.add_argument("input", help="Input HTML file path")
    parser.add_argument("output", nargs="?", help="Output PDF path (default: same name as input)")
    parser.add_argument("--no-header", dest="no_header", action="store_true",
                        default=True, help="Remove header/footer (default: on)")
    parser.add_argument("--with-header", dest="no_header", action="store_false",
                        help="Keep Chrome's default header/footer")
    parser.add_argument("--landscape", action="store_true", help="Landscape orientation")
    parser.add_argument("--paper-size", default="A4",
                        choices=list(PAPER_SIZES.keys()), help="Paper size (default: A4)")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor (default: 1.0)")
    parser.add_argument("--margin", default=None,
                        help="Margin (requires @page CSS in HTML; informational only)")

    args = parser.parse_args()

    try:
        convert(
            input_html=args.input,
            output_pdf=args.output,
            no_header=args.no_header,
            landscape=args.landscape,
            paper_size=args.paper_size,
            scale=args.scale,
            margin=args.margin,
        )
    except (FileNotFoundError, RuntimeError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
