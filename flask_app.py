from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
import sklearn
import pickle
import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
app = Flask(__name__)
CORS(app,support_credentials=True)

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
word_lemmatizer = WordNetLemmatizer()
cooking_words = {"cut","organic","fresh","large","small","diced","chopped","minced","cup","spoon","chop","tablespoon","teaspoon","pinch","boiled","baked","grilled","steamed","sliced","whole","crushed","pureed","roasted","blended","mashed","peeled","shredded","cut","stirred","whisked","seared","toasted","frozen","softened","defrosted","grated","fried","drained","seasoned","marinated","garnished","glazed","caramelized","zested","dressed","broiled","cubed","poured","melted","scrambled","simmered","braised","browned","reduced","cooled","tossed"}

def pre_process(ingredient_list):
    print(f"INGRIDIENTS IN PREPROCESSING : {ingredient_list}")
    stop_words = set(stopwords.words("english"))
    word_lemmatizer = WordNetLemmatizer()
    cooking_words = {"cut","organic","fresh","large","small","diced","chopped","minced","cup","spoon","chop","tablespoon","teaspoon","pinch","boiled","baked","grilled","steamed","sliced","whole","crushed","pureed","roasted","blended","mashed","peeled","shredded","cut","stirred","whisked","seared","toasted","frozen","softened","defrosted","grated","fried","drained","seasoned","marinated","garnished","glazed","caramelized","zested","dressed","broiled","cubed","poured","melted","scrambled","simmered","braised","browned","reduced","cooled","tossed"}
    ingridient_processed = []
    for ingredients in ingredient_list:
        final_ingredient = []
        split_list = ingredients.split(" ")
        for ingredient in split_list:
            ingredient = ingredient.strip()
            ingredient = re.sub(r'[^a-zA-Z\s]','',ingredient)
            if(ingredient in stop_words or ingredient in cooking_words):
#                 print(ingredient)
                continue
            else:
                
                ingredient = word_lemmatizer.lemmatize(ingredient)
                if(ingredient == ""):
                    continue
                final_ingredient.append(ingredient)
        if(len(final_ingredient) > 0):
            ingridient_processed.append(" ".join(final_ingredient))
#     print(ingridient_processed)
    return " ".join(ingridient_processed)


  
@app.route('/predict', methods=['POST','OPTIONS'])
@cross_origin(supports_credentials=True)
def GetPrediction():
  # print(request.json)
  input_data = request.json
  # print(input_data)
  
  ingredients = request.json
  ingredients_preprocessed = [pre_process(ingredients)]
  # print(df)
  
  with open("pipeline.pkl", 'rb') as f:
    model = pickle.load(f)
  print(f"Preprocessed ingridients : {ingredients_preprocessed}")
  pred = model.predict(ingredients_preprocessed)
  d={}
  d["output"]=pred[0]
  print(pred)
  return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
# print(model.predict(input_data))
# app.run(debug=False,host="0.0.0.0",port=4444)