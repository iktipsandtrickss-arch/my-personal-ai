import os
import shutil
from pathlib import Path


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

FILES_DIR = BASE_DIR / "data" / "files"

FILES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SAVE FILE
# =========================================================

def save_file(file_path, user_id="ishtiaq"):
    """
    Save an uploaded file locally.

    Returns:
        saved file path
    """

    user_dir = FILES_DIR / user_id

    user_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    source = Path(file_path)

    destination = user_dir / source.name

    shutil.copy2(
        source,
        destination
    )

    return str(destination)


# =========================================================
# GET USER FILES
# =========================================================

def list_files(user_id="ishtiaq"):
    """
    Return all saved files for a user.
    """

    user_dir = FILES_DIR / user_id

    if not user_dir.exists():
        return []

    return [
        str(file)
        for file in user_dir.iterdir()
        if file.is_file()
    ]


# =========================================================
# GET FILE
# =========================================================

def get_file(filename, user_id="ishtiaq"):
    """
    Get the path of a saved file.
    """

    file_path = (
        FILES_DIR
        / user_id
        / filename
    )

    if file_path.exists():
        return str(file_path)

    return None


# =========================================================
# DELETE FILE
# =========================================================

def delete_file(filename, user_id="ishtiaq"):
    """
    Delete a user's saved file.
    """

    file_path = (
        FILES_DIR
        / user_id
        / filename
    )

    if file_path.exists():

        file_path.unlink()

        return True

    return False


# =========================================================
# TEXT EXTRACTION
# =========================================================

def extract_text(file_path):
    """
    Extract readable text from common file types.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    # -------------------------
    # TXT
    # -------------------------

    if extension == ".txt":

        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )


    # -------------------------
    # PDF
    # -------------------------

    if extension == ".pdf":

        from pypdf import PdfReader

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)


    # -------------------------
    # DOCX
    # -------------------------

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


    # -------------------------
    # CSV
    # -------------------------

    if extension == ".csv":

        import pandas as pd

        dataframe = pd.read_csv(
            str(path)
        )

        return dataframe.to_string(
            index=False
        )


    # -------------------------
    # XLSX
    # -------------------------

    if extension == ".xlsx":

        import pandas as pd

        dataframe = pd.read_excel(
            str(path)
        )

        return dataframe.to_string(
            index=False
        )


    # -------------------------
    # Unsupported
    # -------------------------

    raise ValueError(
        f"Unsupported file type: {extension}"
    )
