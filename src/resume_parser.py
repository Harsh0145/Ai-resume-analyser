from io import BytesIO

import PyPDF2


def extract_text(uploaded_file):
    """Extract readable text from an uploaded PDF resume."""
    if not uploaded_file.name.lower().endswith(".pdf"):
        raise ValueError("Only PDF resume files are supported.")

    try:
        data = uploaded_file.getvalue()
        reader = PyPDF2.PdfReader(BytesIO(data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        if not text.strip():
            raise ValueError(
                "No readable text was found in this PDF. Please upload a text-based PDF."
            )

        return text
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            "Unable to read this PDF. Please upload a valid text-based PDF."
        ) from exc
