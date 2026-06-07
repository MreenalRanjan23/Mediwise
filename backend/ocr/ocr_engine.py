import easyocr
from PIL import Image
import fitz
import io

reader = easyocr.Reader(['en'])


class OCREngine:

    def extract_from_image(self, image_path):

        results = reader.readtext(image_path)

        extracted_text = " ".join(
            [result[1] for result in results]
        )

        return extracted_text

    def extract_from_pdf(self, pdf_path):

        text = ""

        pdf_document = fitz.open(pdf_path)

        for page in pdf_document:

            pix = page.get_pixmap()

            img_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(img_bytes))

            temp_path = "temp_page.png"

            image.save(temp_path)

            page_text = self.extract_from_image(
                temp_path
            )

            text += " " + page_text

        return text