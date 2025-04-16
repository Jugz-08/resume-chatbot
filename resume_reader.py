# resume_reader.py
import pdfplumber
import docx

class ResumeReaderAgent:
    def read(self, file_path):
        if file_path.endswith('.pdf'):
            return self._read_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._read_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    def _read_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _read_docx(self, path):
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
