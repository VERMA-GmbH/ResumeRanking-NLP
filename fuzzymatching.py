# Import module for data manipulation
import pandas as pd
# Import module for linear algebra
import numpy as np
# Import module for Fuzzy string matching
from fuzzywuzzy import fuzz, process
# Import module for regex
import re
# Import module for iteration
import itertools
# Import module for function development
from typing import Union, List, Tuple
# Import module for TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
# Import module for cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
# Import module for KNN
from sklearn.neighbors import NearestNeighbors

# String pre-processing
def preprocess_string(s):
    # Remove spaces between strings with one or two letters
    s = re.sub(r'(?<=\b\w)\s*[ &]\s*(?=\w\b)', '', s)
    return s

# String matching - TF-IDF
def build_vectorizer(
    clean: pd.Series,
    analyzer: str = 'char', 
    ngram_range: Tuple[int, int] = (1, 4), 
    n_neighbors: int = 1, 
    **kwargs
    ) -> Tuple:
    # Create vectorizer
    vectorizer = TfidfVectorizer(analyzer = analyzer, ngram_range = ngram_range, **kwargs)
    X = vectorizer.fit_transform(clean.values.astype('U'))

    # Fit nearest neighbors corpus
    nbrs = NearestNeighbors(n_neighbors = n_neighbors, metric = 'cosine').fit(X)
    return vectorizer, nbrs

# String matching - KNN
def tfidf_nn(
    messy, 
    clean, 
    n_neighbors = 1, 
    **kwargs
    ):
    # Fit clean data and transform messy data
    vectorizer, nbrs = build_vectorizer(clean, n_neighbors = n_neighbors, **kwargs)
    input_vec = vectorizer.transform(messy)

    # Determine best possible matches
    distances, indices = nbrs.kneighbors(input_vec, n_neighbors = n_neighbors)
    nearest_values = np.array(clean)[indices]
    return nearest_values, distances

# String matching - match fuzzy
def find_matches_fuzzy(
    row, 
    match_candidates, 
    limit = 5
    ):
    row_matches = process.extract(
        row, dict(enumerate(match_candidates)), 
        scorer = fuzz.token_sort_ratio, 
        limit = limit
        )
    result = [(row, match[0], match[1]) for match in row_matches]
    return result

# String matching - TF-IDF
def fuzzy_nn_match(
    messy,
    clean,
    column,
    col,
    n_neighbors = 100,
    limit = 5, **kwargs):
    nearest_values, _ = tfidf_nn(messy, clean, n_neighbors, **kwargs)

    results = [find_matches_fuzzy(row, nearest_values[i], limit) for i, row in enumerate(messy)]
    df = pd.DataFrame(itertools.chain.from_iterable(results),
        columns = [column, col, 'Ratio']
        )
    return df

# String matching - Fuzzy
def fuzzy_tf_idf(
    df: pd.DataFrame,
    column: str,
    clean: pd.Series,
    mapping_df: pd.DataFrame,
    col: str,
    analyzer: str = 'char',
    ngram_range: Tuple[int, int] = (1, 3)
    ) -> pd.Series:
    # Create vectorizer
    clean = clean.drop_duplicates().reset_index(drop = True)
    messy_prep = df[column].drop_duplicates().dropna().reset_index(drop = True).astype(str)
    messy = messy_prep.apply(preprocess_string)
    result = fuzzy_nn_match(messy = messy, clean = clean, column = column, col = col, n_neighbors = 1)
    # Map value from messy to clean
    return result