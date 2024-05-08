import re
import os
import spacy
import matplotlib.pyplot as plt
import networkx as nx

# Load spaCy model with disabled components for speed
nlp = spacy.load('en_core_web_sm', disable=['parser', 'lemmatizer'])

def get_all_paths(directory):
    file_paths = []  
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_paths.append(filepath)
    return file_paths

def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return ""

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ['PERSON', 'EVENT', 'PRODUCT', 'LAW']]

def build_network(entities):
    G = nx.Graph()
    # Add nodes and edges
    for ent in entities:
        G.add_node(ent[0], label=ent[1])
    for i, entity1 in enumerate(entities):
        for entity2 in entities[i+1:]:
            if entity1[1] == entity2[1] and entity1[0] != entity2[0]:
                G.add_edge(entity1[0], entity2[0])
    return G

# Collect all paths
file_paths = get_all_paths("data-MSFT")

# Collect all entities from all files
all_entities = []
for file_path in file_paths:
    text = read_text(file_path)
    entities = extract_entities(text)
    all_entities.extend(entities)

# Build and plot the network from all entities
G = build_network(all_entities)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=40, font_size=10)
plt.title('Combined Network of All Entities')
plt.show()
