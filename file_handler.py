from pathlib import Path
import base64


# =========================================================
# SUPPORTED FILE TYPES
# =========================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".csv",
    ".xlsx",

    # Images
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# =========================================================
# IMAGE MIME TYPES
# =========================================================

IMAGE_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


# =========================================================
# EXTRACT TEXT
# =========================================================

def extract_text(file_path):
    """
    Read an uploaded text/document file
    and return its text content.
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
# IMAGE TO BASE64
# =========================================================

def image_to_data_url(file_path):
    """
    Convert an image into a Base64 data URL.

    This can be directly used by vision-capable
    OpenRouter/OpenAI-compatible models.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in IMAGE_MIME_TYPES:

        raise ValueError(
            f"Unsupported image type: {extension}"
        )

    mime_type = IMAGE_MIME_TYPES[extension]

    with open(path, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_image}"


# =========================================================
# PROCESS UPLOADED FILE
# =========================================================

def process_file(file_path):
    """
    Process a Gradio uploaded file.

    Returns:
        filename, extracted text/image data
    """

    if not file_path:
        return None, ""

    path = Path(file_path)
    extension = path.suffix.lower()


    # -----------------------------------------------------
    # CHECK FILE TYPE
    # -----------------------------------------------------

    if extension not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )


    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    if extension in IMAGE_MIME_TYPES:

        image_data = image_to_data_url(
            str(path)
        )

        return path.name, {
            "type": "image_url",
            "image_url": {
                "url": image_data
            }
        }


    # -----------------------------------------------------
    # TEXT / DOCUMENT
    # -----------------------------------------------------

    text = extract_text(
        str(path)
    )

    return path.name, text
