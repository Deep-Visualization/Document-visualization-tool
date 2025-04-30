# IMPORTS
import os
import spacy
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
# LOADING
nlp = spacy.load("en_core_web_sm")
nltk.download('punkt')
nltk.download('stopwords')

# DATASET
dataset = "569/Project 2/dataset"

# STORE
entities = []
filenames = []

#STOP WORDS AND STEMMING
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()


# FOR LOOP
for filename in os.listdir(dataset):
    file_path = os.path.join(dataset, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()  

    # TOKENS
    words = word_tokenize(text.lower())  
    # ONLY WORDS
    words = [word for word in words if word.isalpha()] 
    # NO STOP WORDS 
    words = [word for word in words if word not in stop_words]  
    # STEMMING
    words = [ps.stem(word) for word in words] 
    doc = nlp(text)

    # IMPORTANT TOKENS
    extracted_entities = {
        "person": [],
        "location": [],
        "date": [],
        "organization": []
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_entities["person"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:  # GPE (Geopolitical Entity), LOC (Location)
            extracted_entities["location"].append(ent.text)
        elif ent.label_ == "DATE":
            extracted_entities["date"].append(ent.text)
        elif ent.label_ == "ORG":
            extracted_entities["organization"].append(ent.text)

    entities.append(extracted_entities)
    filenames.append(filename)


entities_df = pd.DataFrame(entities, index=filenames)

# CSV
output_csv = "filtered_extracted_entities.csv"
entities_df.to_csv(output_csv)

print(f"\nProcessed {len(filenames)} .txt documents and saved extracted entities to '{output_csv}'.")

# DOCUMENT TERM MATRIX
entity_texts = [
    " ".join(extracted_entities["person"] + extracted_entities["location"] + extracted_entities["date"] + extracted_entities["organization"])
    for extracted_entities in entities
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(entity_texts)
document_term_matrix = X.toarray()
feature_names = vectorizer.get_feature_names_out()
document_term_matrix_df = pd.DataFrame(document_term_matrix, columns=feature_names, index=filenames)

# SAVE
document_term_matrix_csv = "document_term_matrix.csv"
document_term_matrix_df.to_csv(document_term_matrix_csv)
print(f"Document-Term Matrix saved to '{document_term_matrix_csv}'.")
