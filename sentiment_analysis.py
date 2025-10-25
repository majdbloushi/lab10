import requests
import pickle
import re
from sklearn.metrics import accuracy_score

url = 'http://127.0.0.1:5000/'
parms = 'sort_order=a&count=1000'
texts = []
data = requests.get(url+'get_data', parms)

for i in data.json():
    texts.append(i[0])

with open('model.pickle', 'rb') as f:
    model = pickle.load(f)
    f.close()

with open('vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
    f.close()

def clean_txt(text:str):
    text = text.lower()
    text = re.sub("@[a-z0-9_]+", ' ', text)
    text = re.sub("[^ ]+\.[^ ]+", ' ', text)
    text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
    text = re.sub("[^a-z\' ]", ' ', text)
    text = re.sub(' +', ' ', text)
    return text

def get_total_data_count():
    pos_data = requests.get(url+'get_data_count', 'label_name=positive&count=1000').json()
    neg_data = requests.get(url+'get_data_count', 'label_name=negative&count=1000').json()
    print(pos_data)
    print(neg_data)

guess = []
for i in texts:
    ctxt = clean_txt(i)
    ex = vectorizer.transform([ctxt])
    example_result = model.predict(ex)
    guess.append(example_result[0])


x = vectorizer.transform(texts)
predictions = model.predict(x)
print(accuracy_score(guess, predictions))
# get_total_data_count()