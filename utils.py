import os
import re
import sys
from io import StringIO

import docx
from docx import Document
from PyPDF2 import PdfReader


def convert_pdf_to_docx(pdf_path, docx_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        output = StringIO()
        for i in range(len(pdf_reader.pages)):
            output.write(pdf_reader.pages[i].extract_text())
        text = output.getvalue()
        output.close()

    doc = Document()
    for line in text.split("\n"):
        if re.match(r"\s*\d+\.\d+\s+", line):
            paragraph = doc.add_paragraph(line)
            paragraph.style = doc.styles["List Bullet"]
        else:
            paragraph = doc.add_paragraph(line)

    doc.save(docx_path)




def check_pdf_file(pdf_path):
    pdf_extensions = [
        ".pdf",
        ".PDF"
    ]
    file_name, file_extension = os.path.splitext(pdf_path)

    if file_extension in pdf_extensions:
        return True, file_name + ".docx"
    return False, pdf_path


def check_and_convert_pdf_file(pdf_path, inplace = True):
    check_result, file_name = check_pdf_file(pdf_path)
    if check_result:
        convert_pdf_to_docx(pdf_path, file_name)
        if inplace:
            os.remove(pdf_path)