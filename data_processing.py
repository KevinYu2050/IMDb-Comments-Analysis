import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import movie_reviews
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

for i in movie_reviews:
    print(i)