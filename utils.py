import os
import re
import sys
from io import StringIO
import time

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
    return file_name



def delete_dir(dir_path = None, delete_before = 24*60*60):
    # Specify the directory path
    if dir_path == None:
        return
    # Get the current time in seconds
    now = time.time()

    # Loop through all directories in the specified path
    for dir in os.listdir(dir_path):
        # Get the full path of the directory
        dir_full_path = os.path.join(dir_path, dir)
        
        # Check if the directory exists and is actually a directory
        if os.path.isdir(dir_full_path):
            # Get the creation time of the directory in seconds
            creation_time = os.path.getctime(dir_full_path)
            
            # Calculate the age of the directory in seconds
            age = now - creation_time
            
            # Check if the directory is older than 24 hours
            if age > delete_before:
                # Delete the directory and its contents recursively
                os.system("rm -rf " + dir_full_path)


def del_old_data(path="/root/ResumeRanking-NLP/Data", delete_before = 24*60*60):
    for folder in ["JobDesc", "Resumes"]:
        delete_dir(os.path.join(path, folder), delete_before)


