import pdfplumber


class ResumeParser:

    def extract_text(self, uploaded_file):

        try:
            uploaded_file.seek(0)

            text = ""

            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            return text

        except Exception as e:
            print(e)
            return ""