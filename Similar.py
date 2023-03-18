import textdistance as td


def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c=1
    o=0
    total = (j+s+c+o)/4
    # total = (s+o)/2
    return total*100

def match_skills(resume_skill, job_des_skill):
    j = td.jaccard.similarity(resume_skill, job_des_skill)
    s = td.sorensen_dice.similarity(resume_skill, job_des_skill)
    c = td.cosine.similarity(resume_skill, job_des_skill)
    o = td.overlap.normalized_similarity(resume_skill, job_des_skill)
    total = (j+s+c+o)/4
    return total*100

def calculate_scores(resumes, job_description, index):
    scores = []
    for x in range(resumes.shape[0]):
        score = match(
            resumes['TF_Based'][x], job_description['TF_Based'][index])
        scores.append(score)
    return scores

def calculate_scores_using_skills(resumes, job_description, index):
    scores = []
    for x in range(resumes.shape[0]):
        score = match_skills(
            resumes['Skills_extracted'][x], job_description['Skills_extracted'][index])
        scores.append(score)
    return scores
