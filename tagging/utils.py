
import fasttext
import fasttext.util
fasttext.util.download_model('ko', if_exists='ignore')  # Korean
ft = fasttext.load_model('cc.ko.300.bin')

def embedding(word):
    return ft.get_word_vector(word)
