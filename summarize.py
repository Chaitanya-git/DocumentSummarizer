#!/usr/bin/python
import fire
import bs4
import pprint
import nltk
import urllib.request
import sys
from urllib.request import Request, urlopen
from nltk.tokenize import sent_tokenize
from LDASummarizer import LDASummarizer as Summarizer

def get_webpage_content(url, para_lim=10):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage=str(urlopen(req).read().decode("utf-8"))
    soup = bs4.BeautifulSoup(webpage, "lxml")

    corpus = []
    for elem in soup.find_all('p'):
        para = elem.get_text().replace("\n", "")
        corpus.append(para)

    if len(corpus) <= para_lim:
        print("Warning: the webpage may have been formatted in an unsupported manner due to which the correct content may not have been retreived, or the webpage you've provided is already too short to be summarized")
    return "\n".join(corpus)

def split_lines(doc):
    # Each line is assumed to contain one paragraph of text
    return doc.split("\n")

def split_sentences(doc):
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    return sent_tokenize(doc)

def print_summary(src=sys.stdin, from_url:bool=False, tokenize_sentences:bool=False, num_topics:int=10, print_topics:bool=False):
    pp = pprint.PrettyPrinter(indent=4)
    text = ""
    if from_url:
        text = get_webpage_content(src)
    elif src == sys.stdin:
        text = src.read()
    else:
        with open(src) as f:
            text = f.read()

    corpus = []
    if tokenize_sentences:
        corpus = split_sentences(text)
    else:
        corpus = split_lines(text)

    summarizer = Summarizer(corpus, num_topics)
    if print_topics:
        pp.pprint(summarizer.get_topic_breakdown())
    else:
        print(summarizer.get_summary())


if __name__ == "__main__":
    fire.Fire(print_summary)
