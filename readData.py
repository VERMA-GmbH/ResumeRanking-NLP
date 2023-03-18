# from operator import index
# from pandas._config.config import options
# import Cleaner
import Cleaner as Cleaner
import textract as tx
import pandas as pd
import os
# import tf_idf
import tf_idf as tf_idf

columns = ["Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"]

def get_cleaned_words(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
    return document

def read_resumes(resume_dir = "/Data/Resumes/"):
    document = []

    for resume in os.listdir(resume_dir):
        filepath = os.path.join(resume_dir, resume)
        temp = []
        temp.append(filepath)
        text = tx.process(filepath, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        document.append(temp)

    document = get_cleaned_words(document)
    document = pd.DataFrame(document, columns = columns)
    return document


# document = read_resumes()


def read_jd(job_desc_dir = "/Data/JobDesc/"):
    jd = []
    for job_desc in os.listdir(job_desc_dir):
        filepath = os.path.join(job_desc_dir, job_desc)
        temp = []
        temp.append(filepath)
        text = tx.process(filepath, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        jd.append(temp)
    jd = get_cleaned_words(jd)
    jd = pd.DataFrame(jd, columns = columns)
    return jd


# job_document = read_jobdescriptions()
