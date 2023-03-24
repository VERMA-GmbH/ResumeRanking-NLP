# from operator import index
# from pandas._config.config import options
import os
import textract as tx
import pandas as pd
# import Cleaner
import Cleaner as Cleaner
# import tf_idf
import tf_idf as tf_idf
import Distill as Distill
from pdf2docx import Converter

columns = ["Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based","Skills_extracted"]


def check_file_docx(file_name):
    if file_name.endswith(".docx") or file_name.endswith(".doc"):
        return True
    return False

def convert_pdf_to_docx(file_path):
    docx_file_path = os.path.splitext(file_path)[0]+'.docx'
    cv = Converter(file_path)
    cv.convert(docx_file_path)      # all pages by default
    cv.close()

def get_cleaned_words(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
        skills = Distill.extract_skills(document[i][1])
        document[i].append(' '.join(skills))
    return document

def read_resumes(resume_dir = "/Data/Resumes/"):
    document = []
    documents_failed = []
    for resume in os.listdir(resume_dir):
        temp = []
        try:
            docx_file = os.path.splitext(resume)[0]+'.docx'
            if not resume.endswith(".docx"):
                if resume.endswith(".pdf") and not os.path.exists(os.path.join(resume_dir,resume)):
                    convert_pdf_to_docx(os.path.join(resume_dir, resume))
                else:
                    continue
            filepath = os.path.join(resume_dir, docx_file)
            temp.append(filepath)
            text = tx.process(filepath, encoding='ascii')
            text = str(text, 'utf-8')
            temp.append(text)
            document.append(temp)

        except Exception as e:
            documents_failed.append(resume)


    document = get_cleaned_words(document)
    document = pd.DataFrame(document, columns = columns)
    return document, documents_failed


# document = read_resumes()


def read_jd(job_desc_dir = "/Data/JobDesc/", index:int = None):
    jd_search = os.listdir(job_desc_dir)
    if index is not None:
        jd_search = [os.listdir(job_desc_dir)[index]]
    jd = []
    for job_desc in jd_search:
        temp = []
        docx_file = os.path.splitext(job_desc)[0]+'.docx'
        if not job_desc.endswith(".docx"):
            if job_desc.endswith(".pdf") and not os.path.exists(os.path.join(job_desc_dir,job_desc)):
                convert_pdf_to_docx(os.path.join(job_desc_dir, job_desc))
            else:
                continue
        filepath = os.path.join(job_desc_dir, docx_file)
        temp.append(filepath)
        text = tx.process(filepath, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        jd.append(temp)
    jd = get_cleaned_words(jd)
    jd = pd.DataFrame(jd, columns = columns)
    return jd


# job_document = read_jobdescriptions()
