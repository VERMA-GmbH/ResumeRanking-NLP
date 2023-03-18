from gensim.models import LdaModel
import gensim.corpora as corpora
from operator import index
import pandas as pd
from typing import Union
from typing import List
from fastapi import FastAPI, File, UploadFile
from enum import Enum


import Similar
import readData
import lda

app = FastAPI()

class Type(str, Enum):
    JobDesc = "JobDesc"
    Resume = "Resume"

@app.post("/uploadfiles/")
async def create_upload_files(type:Type, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        if type == "JobDesc":
            with open("Data/JobDesc/file.filename", "wb") as f:
                f.write(contents)
        else:
            with open("Data/Resumes/file.filename", "wb") as f:
                f.write(contents)
    return {"file_names": [file.filename for file in files]}

@app.get("/jobdescs")
def get_job_descriptions():
    jobs = readData.read_jd(job_desc_dir="Data/JobDesc/")
    return {'jobs':jobs}

@app.get("/resumes")
def get_resumes():
    resumes = readData.read_resumes(resume_dir="Data/Resumes/")
    return {'resumes':resumes}

@app.post("/similarity-rankings")
def get_similarity(index:int):
    jobs = readData.read_jd(job_desc_dir="Data/JobDesc/")
    resumes = readData.read_resumes(resume_dir="Data/Resumes/")
    resumes['scores_tf_idf'] = Similar.calculate_scores(resumes, jobs, index)
    resumes['scores_skills_extracted'] = Similar.calculate_scores_using_skills(resumes, jobs, index)
    resumes['Scores'] = (resumes['Scores_tf_idf'] + resumes['Scores_skills_extracted'])/2
    ranked_resumes = resumes.sort_values(
        by=['scores'], ascending=False).reset_index(drop=True)
    ranked_resumes['rank'] = pd.DataFrame([i for i in range(1, len(ranked_resumes['scores'])+1)])
    ranked_resumes = ranked_resumes[['Name','scores','rank']]
    return ranked_resumes.to_json(orient='records')

@app.post("/lda-rankings")
def get_lda_topics():
    resumes = readData.read_resumes(resume_dir="Data/Resumes/")
    lda_model, corpus = lda.get_model(resumes)

    df_topic_sents_keywords = lda.format_topics_sentences(ldamodel=lda_model, corpus=corpus)
    df_some = pd.DataFrame(df_topic_sents_keywords,
                           columns=['Document No', 'Dominant Topic', 'Topic % Contribution', 'Keywords'])
    df_some['Names'] = resumes['Name']
    df_some = df_some.sort_values(by=['Topic % Contribution'], ascending=False)
    print(df_some)
    return df_some.to_json(orient='records')








# print("Loading Resume data and running Resume Ranking System")
#
# #%%
# # Reading the CSV files prepared by the fileReader.py
# # Resumes = pd.read_csv('Resume_Data.csv')
# # Jobs = pd.read_csv('Job_Data.csv')
#
# Resumes = readData.read_resumes(resume_dir="Data/Resumes/")
# Jobs = readData.read_jd(job_desc_dir="Data/JobDesc/")
#
# print('Number of JDs available', len(Jobs))
# print('Nmber of Resume available', len(Resumes))
#
#
# #Print the Job Desciption Names
# print(Jobs['Name'])
#
# index = int(input('Enter the index of the jd you want to process the CV with: '))
#
# # print('The selected JD: ', Jobs['Context'][index])
#
#
# #################################### SCORE CALCUATION ################################
# def calculate_scores(resumes, job_description):
#     scores = []
#     for x in range(resumes.shape[0]):
#         score = Similar.match(
#             resumes['TF_Based'][x], job_description['TF_Based'][index])
#         scores.append(score)
#     return scores
#
#
# Resumes['Scores'] = calculate_scores(Resumes, Jobs)
#
# Ranked_resumes = Resumes.sort_values(
#     by=['Scores'], ascending=False).reset_index(drop=True)
#
# Ranked_resumes['Rank'] = pd.DataFrame(
#     [i for i in range(1, len(Ranked_resumes['Scores'])+1)])
#
#
# ############################## RESUME PRINTING #############################
# print('\n\n.................Ranked Resumes based on cosine similarity score.....................')
# print(Ranked_resumes)
#
# print('\n\n =============================== Ranking system based on LDA topic modelling ================')
# ############################################ TF-IDF Code ###################################
#
# def get_list_of_words(document):
#     Document = []
#
#     for a in document:
#         raw = a.split(" ")
#         Document.append(raw)
#
#     return Document
#
#
# document = get_list_of_words(Resumes['Cleaned'])
#
# id2word = corpora.Dictionary(document)
# corpus = [id2word.doc2bow(text) for text in document]
#
#
# chunksize = 100
# passes = 50
# iterations = 400 # we increase its iterations
# eval_every = None  #
#
# lda_model = LdaModel(corpus=corpus,
#                             id2word=id2word,
#                             num_topics=4,
#                             random_state=100,
#                             chunksize=chunksize,
#                             passes=passes,
#                             alpha='auto',
#                             eta ='auto',
#                             iterations = iterations,
#                             gamma_threshold=0.001,
#                             per_word_topics=True,
#                             eval_every = eval_every)
#
# ################################### LDA CODE ##############################################
#
#
# def format_topics_sentences(ldamodel, corpus):
#     sent_topics_df = []
#     for i, row_list in enumerate(ldamodel[corpus]):
#         row = row_list[0] if ldamodel.per_word_topics else row_list
#         row = sorted(row, key=lambda x: (x[1]), reverse=True)
#         for j, (topic_num, prop_topic) in enumerate(row):
#             if j == 0:
#                 wp = ldamodel.show_topic(topic_num)
#                 topic_keywords = ", ".join([word for word, prop in wp])
#                 sent_topics_df.append(
#                     [i, int(topic_num), round(prop_topic, 4)*100, topic_keywords])
#             else:
#                 break
#
#     return sent_topics_df
#
#
# ####################### SETTING UP THE DATAFRAME for topic wise resume ranking ############################
# df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus)
#
# df_some = pd.DataFrame(df_topic_sents_keywords, columns=['Document No', 'Dominant Topic', 'Topic % Contribution', 'Keywords'])
#
# df_some['Names'] = Resumes['Name']
# df_some = df_some.sort_values(by=['Topic % Contribution'], ascending=False)
#
# print("## Topic Modelling of Resumes ")
# print('\n\n.............................Ranking based on topic relevance................................')
# print(df_some)
