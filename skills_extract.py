# imports
import spacy
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
# nlp = spacy.load("en_core_web_lg")
# init skill extractor


def get_skills(nlp, text):
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

    # extract skills from job_description
    job_description = text

    annotations = skill_extractor.annotate(job_description)
    skills = set()
    for key in annotations['results']['full_matches']:
        skills.add(key['doc_node_value'])
    for key in annotations['results']['ngram_scored']:
        skills.add(key['doc_node_value'])

    return skills
