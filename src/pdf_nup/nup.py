import math
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter


class PDFNupError(Exception):
    pass


def _calculate_grid(pages_per_sheet: int, landscape: bool) -> tuple[int, int]:
    if pages_per_sheet == 1:
        return 1, 1

    best_cols, best_rows = 1, pages_per_sheet
    best_empty = pages_per_sheet - 1

    output_ratio = 1.29 if landscape else 0.77

    for cols in range(1, pages_per_sheet + 1):
        rows = math.ceil(pages_per_sheet / cols)
        empty_cells = cols * rows - pages_per_sheet

        if empty_cells < best_empty:
            best_empty = empty_cells
            best_cols, best_rows = cols, rows
        elif empty_cells == best_empty:
            cell_ratio = (1 / rows) / (1 / cols)
            best_cell_ratio = (1 / best_rows) / (1 / best_cols)
            if abs(cell_ratio - output_ratio) < abs(best_cell_ratio - output_ratio):
                best_cols, best_rows = cols, rows

    return best_cols, best_rows


def create_nup_pdf(
    input_path: Path,
    output_path: Path,
    pages_per_sheet: int = 4,
    landscape: bool = False,
    verbose: bool = False,
) -> None:
    if pages_per_sheet < 1:
        raise PDFNupError("Pages per sheet must be at least 1")

    reader = PdfReader(input_path)
    num_pages = len(reader.pages)

    if num_pages == 0:
        raise PDFNupError("Input PDF has no pages")

    if verbose:
        total_sheets = math.ceil(num_pages / pages_per_sheet)
        print(f"Processing {num_pages} pages into {total_sheets} sheets...")

    cols = int(math.ceil(math.sqrt(pages_per_sheet)))
    rows = int(math.ceil(pages_per_sheet / cols))

    cols, rows = _calculate_grid(pages_per_sheet, landscape)

    if landscape:
        page_width, page_height = letter
    else:
        page_height, page_width = letter

    cell_width = page_width / cols
    cell_height = page_height / rows

    output_writer = PdfWriter()
    pages_needed = math.ceil(num_pages / pages_per_sheet)

    for sheet_idx in range(pages_needed):
        if verbose and pages_needed > 10:
            if sheet_idx % max(1, pages_needed // 10) == 0:
                print(f"  Processing sheet {sheet_idx + 1}/{pages_needed}...")

        new_page = output_writer.add_blank_page(page_width, page_height)

        for i in range(pages_per_sheet):
            page_idx = sheet_idx * pages_per_sheet + i
            if page_idx >= num_pages:
                break

            source_page = reader.pages[page_idx]

            source_width = source_page.mediabox.width
            source_height = source_page.mediabox.height

            scale = min(
                (cell_width - 10) / source_width,
                (cell_height - 10) / source_height,
            )

            scaled_width = source_width * scale
            scaled_height = source_height * scale

            col = i % cols
            row = rows - 1 - (i // cols)

            x = col * cell_width + (cell_width - scaled_width) / 2
            y = row * cell_height + (cell_height - scaled_height) / 2

            temp_writer = PdfWriter()
            temp_writer.add_page(source_page)

            temp_buffer = BytesIO()
            temp_writer.write(temp_buffer)
            temp_buffer.seek(0)

            temp_reader = PdfReader(temp_buffer)
            temp_page = temp_reader.pages[0]

            transform = (scale, 0, 0, scale, x, y)
            new_page.merge_transformed_page(temp_page, transform)

    with open(output_path, "wb") as f:
        output_writer.write(f)

    if verbose:
        print(f"Created: {output_path}")
