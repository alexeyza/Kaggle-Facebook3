import sys
import csv as csv 
from bs4 import BeautifulSoup
import os

def main():
    stop_words = get_common_english_words('common-english-words.csv')
    # if no filenames were given as input it would try to run on the default 'train.csv' and 'test.csv'
    if len(sys.argv)==1:
        pre_process_csv('train.csv',stop_words)
        pre_process_csv('test.csv',stop_words)
    # pre process any given filename in the command line input
    for arg in sys.argv[1:]:
        pre_process_csv(arg,stop_words)


def filter_common_words(text, stop_words):
    if isinstance(text, unicode):
        text = text.encode('utf8')
    # the following symbols will be replaced with white space
    symbols = [',','.',':',';','+','=','"','/']
    for symbol in symbols:
        text = text.replace(symbol,' ')
    output = ""
    for word in text.split():
        if not word.lower() in stop_words:
            output += word + ' '
    return output


def filter_html_tags(text):
    # the following tags and their content will be removed, for example <a> tag will remove any html links
    tags_to_filter = ['code','a']
    if isinstance(text, unicode):
        text = text.encode('utf8')
    soup = BeautifulSoup(text)
    for tag_to_filter in tags_to_filter:
        text_to_remove = soup.findAll(tag_to_filter)
        [tag.extract() for tag in text_to_remove]
    return soup.get_text()


def pre_process_csv(filename, word_set_to_filter=None):
    if word_set_to_filter is None:
        word_set_to_filter = set()
    print 'pre processing '+filename+'...'
    train_file_object = csv.reader(open('..'+os.path.sep+'csv'+os.path.sep+filename, 'rb'))
    header = train_file_object.next()
    pre_processed_file = csv.writer(open('..'+os.path.sep+'csv'+os.path.sep+'pre_process_'+filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
    pre_processed_file.writerow(header)
    # if the csv file is the test data
    if len(header)==3:
        for row in train_file_object:
            pre_processed_file.writerow([int(row[0]), filter_common_words(row[1],word_set_to_filter), filter_common_words(filter_html_tags(row[2]),word_set_to_filter)])
    # if the csv file is the train data
    if len(header)==4:
        for row in train_file_object:
            pre_processed_file.writerow([int(row[0]), filter_common_words(row[1],word_set_to_filter), filter_common_words(filter_html_tags(row[2]),word_set_to_filter),row[3]])
    print 'finished'


def get_common_english_words(filename):
    english_words_file = csv.reader(open('..'+os.path.sep+'csv'+os.path.sep+filename, 'rb'))
    stop_words = set()
    for row in english_words_file:
        for word in row:
            stop_words.add(word.lower())
    return stop_words


if __name__ == '__main__':
    main()