import argparse
from pathlib import Path

from pdf_nup import create_nup_pdf


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Combine multiple PDF pages into a single page (n-up)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-nup input.pdf -n 4              Combine 4 pages into 1 (default)
  pdf-nup input.pdf -n 2             Combine 2 pages into 1
  pdf-nup input.pdf -n 9              Combine 9 pages into 1
  pdf-nup input.pdf -o output.pdf     Specify output file
  pdf-nup input.pdf -n 4 --landscape  Use landscape orientation
        """,
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Input PDF file",
    )
    parser.add_argument(
        "-n", "--pages-per-sheet",
        type=int,
        default=4,
        metavar="N",
        help="Number of pages to combine into one (default: 4)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PDF file (default: input_nup.pdf)",
    )
    parser.add_argument(
        "--landscape",
        action="store_true",
        help="Use landscape orientation for output pages",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress information",
    )
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        return 1

    if not args.input.exists():
        parser.error(f"Input file not found: {args.input}")

    if args.pages_per_sheet < 1:
        parser.error("Pages per sheet must be at least 1")

    output_path = args.output or args.input.with_name(f"{args.input.stem}_nup.pdf")

    if args.verbose:
        print(f"Input: {args.input}")
        print(f"Output: {output_path}")
        print(f"Pages per sheet: {args.pages_per_sheet}")
        print(f"Orientation: {'landscape' if args.landscape else 'portrait'}")

    try:
        create_nup_pdf(
            input_path=args.input,
            output_path=output_path,
            pages_per_sheet=args.pages_per_sheet,
            landscape=args.landscape,
            verbose=args.verbose,
        )
        print(f"Created: {output_path}")
        return 0
    except Exception as e:
        parser.error(str(e))
