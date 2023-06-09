import nltk
nltk.download('stopwords')
nltk.download('punkt')
import spacy
import re
nltk.data.path.append(' /usr/local/nltk_data')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

from skills_extract import get_skills


# Define english stopwords
stop_words = stopwords.words('english') 

# load the spacy module and create a nlp object
# This need the spacy en module to be present on the system.
nlp = spacy.load('en_core_web_lg')
# proces to remove stopwords form a file, takes an optional_word list
# for the words that are not present in the stop words but the user wants them deleted.


def remove_stopwords(text, stopwords=stop_words, optional_params=False, optional_words=[]):
    if optional_params:
        stopwords.append([a for a in optional_words])
    return [word for word in text if word not in stopwords]


def tokenize(text):
    # Removes any useless punctuations from the text
    # text = re.sub(r'[^\w\s]', '', text)  # using remove_punctuations function
    return word_tokenize(text)


def lemmatize(text):
    # the input to this function is a list
    str_text = nlp(" ".join(text))
    lemmatized_text = []
    for word in str_text:
        lemmatized_text.append(word.lemma_)
    return lemmatized_text

# internal fuction, useless right now.


def _to_string(List):
    # the input parameter must be a list
    string = " "
    return string.join(List)


def remove_tags(text, postags=['PROPN', 'NOUN', 'ADJ', 'VERB', 'ADV']):
    """
    Takes in Tags which are allowed by the user and then elimnates the rest of the words
    based on their Part of Speech (POS) Tags.
    """
    filtered = []
    str_text = nlp(" ".join(text))
    for token in str_text:
        if token.pos_ in postags:
            filtered.append(token.text)
    return filtered

def remove_punctuations(text):
    # Removes any useless punctuations from the text
    text = re.sub('http\S+\s*', ' ', text)  # remove URLs
    text = re.sub('#\S+', '', text)  # remove hashtags
    text = re.sub('@\S+', '  ', text)  # remove mentions
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)  # remove punctuations
    text = re.sub(r'[^\x00-\x7f]',r' ', text) 
    text = re.sub('\s+', ' ', text)  # remove extra whitespace
    return text

def extract_skills(text):
    '''
    Helper function to extract skills from spacy nlp text
    :param text: noun chunks extracted from nlp text
    :return: string of skills extracted
    '''
    return get_skills(nlp, text)