import gc
import re
import time
import pickle
import pandas as pd


def read_text_data(file_name: str):
    data = []
    with (open(file_name, "rb")) as openfile:
        while True:
            try:
                data.append(pickle.load(openfile))
            except EOFError:
                break
    return data


def filter_articles(articles):
    articles[:] = [re.sub('[^a-zA-Z ]+', ' ', article) for article in articles]


def get_words_dict(articles):
    words_list = []
    filter_articles(articles)

    for article in articles:
        words_list.extend(article.split())

    words_dict = dict()
    for elem in words_list:
        # if is_long_enough(elem):
        words_dict[elem] = 0
    return words_dict


def is_long_enough(word):
    if len(word) > 3:
        return True


def get_words_occurrence_dict(words_dict, article):
    words_dict_copy = words_dict.copy()

    # modified_article = re.sub('[^a-zA-Z ]+', ' ', article)
    for word in article.split():
        # if is_long_enough(word):
        if word not in words_dict_copy.keys():
            words_dict_copy[word] = 0
        words_dict_copy[word] = words_dict_copy.get(word, 0) + 1

    gc.collect()
    return words_dict_copy


def get_words_occurrence_matrix(articles):
    words_dict = get_words_dict(articles)
    words_occ = []
    counter = 0
    max_counter = len(articles)
    for article in articles:
        counter += 1
        print('Processing article: ', counter, '|', max_counter)
        words_occurrence_dict = get_words_occurrence_dict(words_dict, article)
        words_occ.append(words_occurrence_dict)
    return words_occ


def filter_article(article):
    pass


text_data = read_text_data('data/text_data.pickle')

articles = []
articles_test = [
    'The Counter class itself is it it a dictionary subclass with no restrictions it on its keys and values.',
    'The values are intended to be numbers representing counts, but you could store anything in the value field.',
    'The most_common() method requires only that the values be orderable.',
    'The elements() method requires integer counts. It ignores zero and negative counts.',
    'The same is also true for update() and subtract() which allow negative and zero values for both inputs and outputs.',
    ]

for elements in text_data[0]:
    articles.append(elements[4])

start = time.perf_counter()
words_occ = get_words_occurrence_matrix(articles_test)
end = time.perf_counter()
print(f'Elapsed time of articles processing: {end - start}[s]')

start = time.perf_counter()
print('Creating occurrence matrix...')
words_occurrence_matrix = pd.DataFrame(words_occ)
sum_df = words_occurrence_matrix.sum(axis=0)
sum_ = sum(sum_df)
new_sum_df = sum_df / sum_
sum_ * 0.9

end = time.perf_counter()
print(f'Elapsed time of words occurrence matrix creation: {end - start}[s]')

start = time.perf_counter()
print('Saving words occurrence matrix to pickle file...')
words_occurrence_matrix.to_pickle('data/words_occurrence_matrix.pickle')
print(words_occurrence_matrix.shape)
end = time.perf_counter()
print(f'Elapsed time of saving words occurrence matrix to pickle file...n: {end - start}[s]')
print('DEBUG')

test_df = words_occurrence_matrix.iloc[0:100, :]
