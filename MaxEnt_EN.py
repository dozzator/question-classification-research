﻿# -*- coding: utf-8 -*-
import re
import csv

import nltk

# ----------------------------------------------------------------
def replace_two_or_more(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def process_question(question):
    question = question.lower()
    question = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',question)
    question = re.sub('[\s]+',' ',question)
    question = question.strip('\'"')
    return question

def get_stop_word_list(stop_word_list_file_name):
    stop_words = []
    stop_words.append('URL')
    fp = open(stop_word_list_file_name, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_words.append(word)
        line = fp.readline()
    fp.close()
    return stop_words
    
def get_feature_vector(question, stop_words):
    feature_vector = []
    words = question.split()
    for w in words:
        w = replace_two_or_more(w)
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stop_words or val is None):
            continue
        else:
            feature_vector.append(w.lower())
    return feature_vector
    
def get_feature_list(file_name):
    fp = open(file_name, 'r')
    line = fp.readline()
    feature_list = []
    while line:
        line = line.strip()
        feature_list.append(line)
        line = fp.readline()
    fp.close()
    return feature_list
    
def extract_features(question):
    question_words = set(question)
    features = {}
    for word in feature_list:
        features['contatins(%s)' % word] = (word in question_words)
    return features   
        

inp_questions = csv.reader(open('Data/sampleQuestions.csv', 'rb'), delimiter=',', quotechar = '|')
stop_words = get_stop_word_list('Data/stopwords.txt')
feature_list = get_feature_list('Data/sampleQuestionFeatureList.txt')

questions = []
for row in inp_questions:
    class_type = row[0]
    question = row[1]
    processed_question = process_question(question)
    feature_vector = get_feature_vector(processed_question, stop_words)
    questions.append((feature_vector, class_type))
    
training_set = nltk.classify.util.apply_features(extract_features, questions)

maxent_classifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 5)

#testQuestion = 'What sport do the Cleaveland Cavaliers play ?'
#processedTestQuestion = processQuestion(testQuestion)
#print MaxEntClassifier.classify(extract_features(getFeatureVector(processedTestQuestion, stopWords)))


testQuestion = ["	What does INRI stand for when used on Jesus ' cross ?	",
"	CNN is the abbreviation for what ?	",
"	What does S.O.S. stand for ?	"]

for ask in testQuestion:
    processed_test_question = process_question(ask)
    print maxent_classifier.classify(extract_features(get_feature_vector(processed_test_question, stop_words)))



