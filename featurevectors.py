# -*- coding: utf-8 -*-

import csv

# ------------------preprocess.py---------------------------
import re

# первоначальная обработка вопросов
def processQuestion(question):
    # обработка вопроса
    
    # перевод в нижний регистр
    question = question.lower()
    # замена ссылок на 'URL
    question = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',question)
    # удаление дополнительных пробелов
    question = re.sub('[\s]+',' ',question)
    # удаление кавычек
    question = question.strip('\'"')
    return question
    
# ----------------------------------------------------------

# создание списка стоп-слов
stopWords = []

# функция удаление повторяющихся сивовол replaceTwoOrMore
def replaceTwoOrMore(s):
    # поиск 2 и более повторяющихся символов
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

# функция получание стоп-слов
def getStopWordList(stopWordListFileName):
    # подгрузка стоп-слов из файла и создание списка
    stopWords = []
    stopWords.append('URL')
    
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

# функция получения векторов признаков
def getFeatureVector(question):
    featureVector = []
    # деление вопроса на слова (простейшая токенизация)
    words = question.split()
    for w in words:
        # удаление повторяющихся символов
        w = replaceTwoOrMore(w)
        # удаление пуктуационных знаков
        w = w.strip('\'"?,.')
        # проверка наличия слов, начинающихся не с букв
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # игнорирование стоп-слов
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
    
fp = open('Data/training.txt', 'r')
line = fp.readline()

st = open('Data/stopwords.txt', 'r')
stopWords = getStopWordList('Data/stopwords.txt')

"""
while line:
    processedQuestion = processQuestion(line)
    featureVector = getFeatureVector(processedQuestion)
    print featureVector
    line = fp.readline()
    
fp.close()
"""
# ------------------- Feature Extraction -----------------------------
inpQuestions = csv.reader(open('Data/sampleQuestions.csv', 'rb'), delimiter = ',', quotechar='|')
questions = []

for row in inpQuestions:
    classType = row[0]
    question = row[1]
    processedQuestion = processQuestion(question)
    featureVector = getFeatureVector(processedQuestion)
    questions.append((featureVector, classType))
    
# --------------------------------------------------------------------

# ---------------- Feature List -------------------------
featureList = []
for words in questions:
    for innerWord in words[0]:
        featureList.append(innerWord)
        
output_file = open('Data/sampleQuestionFeatureList.txt', 'w')
for oneFeature in featureList:
    output_file.write("%s\n" % oneFeature)
output_file.close()
                
# -------------------------------------------------------        

# --------------------------
"""
def extract_features(question):
    question_words = set(question)
    print question_words
    features = {}
    for word in featureList:
        features['contatins(%s)' % word] = (question in question_words)
    return features

extract_features(q)
"""    
    
    
    
    
    
