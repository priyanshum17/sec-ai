import os
import json
import spacy
from client import important_words, text_generation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load spaCy model with specific components disabled for increased processing speed.
nlp = spacy.load('en_core_web_sm', disable=['parser', 'lemmatizer'])

def get_all_paths(directory):
    """
    Retrieve all file paths within a specified directory recursively.

    Args:
        directory (str): The directory from which to fetch file paths.

    Returns:
        list: A list of all file paths within the directory.
    """
    file_paths = []  
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_paths.append(filepath)
    return file_paths

def read_texts(file_paths):
    """
    Read and return the content of text files given a list of file paths.

    Args:
        file_paths (list): A list of file paths from which to read text.

    Returns:
        list: A list containing the contents of each text file.
    """
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
    """
    Extract and count named entities from a list of texts, focusing on persons, events, products, and laws.

    Args:
        texts (list): A list of strings, each being a text to process.

    Returns:
        dict: A dictionary of entities and their occurrence counts.
    """
    entities = {}
    for doc in nlp.pipe(texts, batch_size=1000):
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'EVENT', 'PRODUCT', 'LAW']:
                entities[ent.text] = entities.setdefault(ent.text, 0) + 1
    return entities

def get_vis(ticker):
    """
    Generate a visualization of important words as a word cloud for texts related to a specific ticker.

    Args:
        ticker (str): The ticker symbol of the company for which to generate a word cloud.

    Returns:
        str: The response text after generating the word cloud.
    """
    # Collect all paths for a given ticker and read the texts.
    file_paths = get_all_paths(f"data-{ticker}")    
    texts = read_texts(sorted(file_paths))
    
    # Extract relevant entities from the texts.
    all_entities = extract_entities(texts)
    print("Extraction Done")
    
    # Retrieve important words from the entities using an external service.
    print("Getting words...")
    response = important_words(all_entities)
    dict = json.loads(response)
    print("Finishing")
    
    # Generate additional text responses if necessary.
    text_response = text_generation(response=response)

    # Generate a word cloud. If too few important words, fallback to all extracted entities.
    if len(dict.keys()) < 10:
        dict = all_entities
    wordcloud = WordCloud(width=800, height=400).generate(' '.join(dict.keys()))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('vis.png')

    return text_response