from gensim.models import LdaModel
import gensim.corpora as corpora

def get_list_of_words(document):
    Document = []

    for a in document:
        raw = a.split(" ")
        Document.append(raw)

    return Document


def get_model(Resumes):
    document = get_list_of_words(Resumes['Cleaned'])

    id2word = corpora.Dictionary(document)
    corpus = [id2word.doc2bow(text) for text in document]


    chunksize = 100
    passes = 50
    iterations = 400 # we increase its iterations
    eval_every = None  #

    lda_model = LdaModel(corpus=corpus,
                                id2word=id2word,
                                num_topics=7,
                                random_state=100,
                                chunksize=chunksize,
                                passes=passes,
                                update_every=3, # determines how often the model parameters should be updated
                                alpha='auto',
                                eta ='auto',
                                iterations = iterations,
                                gamma_threshold=0.001,
                                per_word_topics=True,
                                eval_every = eval_every)
    return lda_model, corpus

################################### LDA CODE ##############################################


def format_topics_sentences(ldamodel, corpus):
    sent_topics_df = []
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df.append(
                    [i, int(topic_num), round(prop_topic, 4)*100, topic_keywords])
            else:
                break

    return sent_topics_df
