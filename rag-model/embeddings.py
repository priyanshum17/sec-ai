import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_together import TogetherEmbeddings
from langchain_community.llms import Together

# Define the path constants for the directory locations.
CHROMA_PATH = "chroma"
DATA_PATH = "data-META"
os.environ["TOGETHER_API_KEY"] = ""
# Optionally set the LangChain API key from an environment variable or prompt.
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter LangChain API Key: ")

def load_and_split_documents():
    """
    Load text documents from a specified directory and split them into smaller chunks.

    Returns:
        list: A list of document chunks, each within the specified size constraints.
    """
    # Load all text files from the specified data path.
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()

    # Split documents into chunks of 512 characters with 128 characters overlap.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_embeddings(chunks, batch_size=10):
    """
    Create embeddings for each chunk of text using a pre-trained model and track the progress.

    Args:
        chunks (list): A list of document chunks.
        batch_size (int): The number of chunks to process at one time.

    Returns:
        list: A list of embeddings corresponding to the document chunks.
    """
    embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-32k-retrieval")
    all_embeddings = []
    total_batches = (len(chunks) + batch_size - 1) // batch_size

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        texts = [chunk.page_content for chunk in batch_chunks]
        batch_embeddings = embeddings.embed_documents(texts)
        all_embeddings.extend(batch_embeddings)
        progress = (i // batch_size + 1) / total_batches * 100
        print(f"Processed batch {i//batch_size + 1}/{total_batches} ({progress:.2f}% complete)")

    return all_embeddings

def setup_vector_store(texts, embeddings):
    """
    Initialize a FAISS vector store with texts and their corresponding embeddings.

    Args:
        texts (list): A list of document texts.
        embeddings (list): A list of embeddings for the texts.

    Returns:
        object: A retriever object capable of handling queries based on the embeddings.
    """
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore.as_retriever()

def setup_query_interface(retriever):
    """
    Create a query interface for asking questions about the documents using a language model.

    Args:
        retriever (object): A retriever object containing document embeddings.

    Returns:
        object: A pipeline object configured for responding to queries about the documents.
    """
    model = Together(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.7,
        max_tokens=1000,
        top_k=50,
    )
    prompt = ChatPromptTemplate.from_template(
        "<s>[INST] Answer the question in a simple sentence based only on the following context:\n{context}\n\nQuestion: {question} [/INST]"
    )
    return prompt | model | StrOutputParser()

def main():
    """
    The main function to load documents, create embeddings, and set up a query interface.
    """
    chunks = load_and_split_documents()
    texts = [chunk.page_content for chunk in chunks]
    embeddings = create_embeddings(chunks)
    retriever = setup_vector_store(texts, embeddings)
    chain = setup_query_interface(retriever)
    
    input_query = "Tell me something about the company's risk factors based on these documents over the years."
    output = chain.invoke({"context": retriever, "question": input_query})
    print(output)

if __name__ == "__main__":
    main()
