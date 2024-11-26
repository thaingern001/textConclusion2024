#this code output raw data to clean data
import json
import string 
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
def read_data():
    f = open("dataset/Morbi_bridge_collapse.json") 

    data = json.load(f)
    print(type(data))
    print(len(data))
    # print(data[0])
    tweet  = data[0]

    for i in tweet :
        print(i,":",tweet[i],"\n")

def rm_punctuations(text):
    return text.translate(str.maketrans('','',string.punctuation))

def rm_url(text):
    text = re.sub(r'http\S+','',text)
    text = re.sub(r'https\S+','',text)
    return text



def Tokenization(text):
    lis = text.split()
    return lis

def rm_stopword(words) :
    stop_words = set(stopwords.words("english"))
    return [word for word in words if word.lower() not in stop_words]

def preprocessing(text):
    text = re.sub(r'[^A-Za-z\s]', '', text)
    
    text = text.lower()
    # print(text)
    text = rm_punctuations(text)
    # print(text)
    text = rm_url(text)
    # print(text)
    words = Tokenization(text)
    # print(words)
    words = rm_stopword(words)
    # print(words)
    return words

def group_pairs(words): #make bigram
    bigram_words = [f"{words[i]} {words[i + 1]}" for i in range(len(words)-1) ]
    return bigram_words



def test():
    f = open("dataset/Morbi_bridge_collapse.json") 
    data = json.load(f)
    text = data[0]["full_text"]
    # print(text)
    # text = rm_punctuations(text)
    # print(text)
    # text = rm_url(text)
    # print(text)
    # words = Tokenization(text)
    # print(words)
    # words = rm_stopword(words)
    # print(words)
    print(text)
    after_pps = preprocessing(text)
    print(after_pps)

    bigram_words = group_pairs(after_pps)
    print(bigram_words)

def main():
    f = open("dataset/Morbi_bridge_collapse.json") 
    data = json.load(f)
    list_of_bigrams = []
    for i in range(len(data)) :
        text = data[i]["full_text"]
        words = preprocessing(text)
        bigram_words = group_pairs(words)
        list_of_bigrams.append(bigram_words)
    return list_of_bigrams

# read_data()
# test()
print(main())
# print(len(main()))



# print(Tokenization("don't"))
# print(rm_punctuations("not! $ don't thaingern."))
# print(rm_url("Here's a link: http://example.com and another one: https://secure-site.com."))

# print("====================== Finished code... ======================")
