import os
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load spaCy model with disabled components for speed
nlp = spacy.load('en_core_web_sm', disable=['parser', 'lemmatizer'])

def get_all_paths(directory):
    file_paths = []  
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_paths.append(filepath)
    return file_paths

def read_texts(file_paths):
    texts = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                texts.append(file.read())
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return texts

def extract_entities(texts):
    # Processing texts in batches for efficiency
    entities = {}
    for doc in nlp.pipe(texts, batch_size=20):
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'EVENT', 'PRODUCT', 'LAW']:  # Focus on specific entities
                entities[ent.text] = entities.get(ent.text, 0) + 1
    return entities

# Collect all paths and read texts
file_paths = get_all_paths("data-MSFT")[:2]
texts = read_texts(file_paths)

# Extract entities from all texts
all_entities = extract_entities(texts)
print(all_entities.keys())

# Create a word cloud from entities
wordcloud = WordCloud(width=800, height=400).generate(' '.join(all_entities.keys()))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Named Entities in 10-K Filings')
plt.show()
