import textdistance as td
from fuzzymatching import *


def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    # c=1
    # o=0
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = (j+s+c+o)/4
    # total = (s+o)/2
    return total*100

# def match_skills(resume_skill, job_des_skill):
#     j = td.jaccard.similarity(resume_skill, job_des_skill)
#     s = td.sorensen_dice.similarity(resume_skill, job_des_skill)
#     c = td.cosine.similarity(resume_skill, job_des_skill)
#     o = td.overlap.normalized_similarity(resume_skill, job_des_skill)
#     total = (j+s+c+o)/4
#     return total*100

def calculate_scores(resumes, job_description, index):
    scores = []
    for x in range(resumes.shape[0]):
        try:
            score = match(
                resumes['TF_Based'][x], job_description['TF_Based'][index])
            scores.append(score)
        except Exception as e:
            print(e, "Appending score 0")
            scores.append(0)
        
    return scores

def calculate_scores_using_skills(resumes, job_description, index):
    df = pd.DataFrame(columns=['Resume', 'JD'])
    df['Resume'] = resumes['Skills_extracted']
    df['JD'] = job_description['Skills_extracted'].iloc[index]

    df_result = (df.pipe(fuzzy_tf_idf, # Function and messy data
                     column = 'Resume', # Messy column in data
                     clean = df['JD'], # Master data (list)
                     mapping_df = df, # Master data
                     col = 'Result') # Can be customized
            )
    
    # df_result['Name'] = resumes['Name']
    # df_result['JD_name'] = job_description['Name'].iloc[0]
    # scores = []
    # for x in range(resumes.shape[0]):
    #     score = match_skills(
    #         resumes['Skills_extracted'][x], job_description['Skills_extracted'][index])
    #     scores.append(score)
    return df_result['Ratio'].tolist()

