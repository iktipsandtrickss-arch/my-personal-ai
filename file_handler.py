from pathlib import Path


# =========================================================
# SUPPORTED FILE TYPES
# =========================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".csv",
    ".xlsx",
}


# =========================================================
# EXTRACT TEXT
# =========================================================

def extract_text(file_path):
    """
    Read an uploaded file and return its text content.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    # TXT
    if extension == ".txt":

        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )


    # PDF
    if extension == ".pdf":

        from pypdf import PdfReader

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)


    # DOCX
    if extension == ".docx":

        from docx import Document

        document = Document(str(path))

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                paragraphs.append(
                    paragraph.text
                )

        return "\n".join(paragraphs)


    # CSV
    if extension == ".csv":

        import pandas as pd

        dataframe = pd.read_csv(
            str(path)
        )

        return dataframe.to_string(
            index=False
        )


    # XLSX
    if extension == ".xlsx":

        import pandas as pd

        dataframe = pd.read_excel(
            str(path)
        )

        return dataframe.to_string(
            index=False
        )


    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# =========================================================
# PROCESS UPLOADED FILE
# =========================================================

def process_file(file_path):
    """
    Process a Gradio uploaded file.

    Returns:
        filename, extracted text
    """

    if not file_path:
        return None, ""

    path = Path(file_path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )

    text = extract_text(
        str(path)
    )

    return path.name, text
