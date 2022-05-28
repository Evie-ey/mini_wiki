from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


def format_tags(results):
    for item in results:
        item["tags"] = list(map(lambda x: x["tag_text"], item["tags"]))
        # item["tags"] = [ item["tags"]['tag_text'] for a in item["tags"]]

    return results


def remove_stop_words(search_word):
    search_word_string = word_tokenize(search_word)

    search_word_without_sw = " ".join(
        [word for word in search_word_string if not word in stopwords.words()])

    return search_word_without_sw


def make_document_slug(search_word):
    search_word_string = word_tokenize(search_word)

    slug_without_sw = '-'.join([
        word for word in search_word_string if not word in stopwords.words()])

    return slug_without_sw
