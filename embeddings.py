import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_together import TogetherEmbeddings
from langchain_community.llms import Together

# Constants for paths
CHROMA_PATH = "chroma"
DATA_PATH = "data-META"
os.environ["TOGETHER_API_KEY"] = "f05b0e9e7a8827d89812a472aac092b61e1c5e4ddb447d7b32baf036e97da446"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter LangChain API Key: ")

def load_and_split_documents():
    """Load documents from the directory and split them into manageable chunks."""
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_embeddings(chunks, batch_size=10):
    """Create vector embeddings for document chunks with progress update."""
    embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-32k-retrieval")
    all_embeddings = []
    total_batches = (len(chunks) + batch_size - 1) // batch_size  # Calculate the total number of batches

    # Process texts in batches
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        texts = [chunk.page_content for chunk in batch_chunks]
        batch_embeddings = embeddings.embed_documents(texts)
        all_embeddings.extend(batch_embeddings)
        
        # Calculate and print the percentage of progress
        progress = (i // batch_size + 1) / total_batches * 100
        print(f"Processed batch {i//batch_size + 1}/{total_batches} ({progress:.2f}% complete)")

    return all_embeddings

def setup_vector_store(texts, embeddings):
    """Save embeddings in a FAISS vector store and return the retriever."""
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore.as_retriever()

def setup_query_interface(retriever):
    """Set up the query interface to ask questions about the documents."""
    model = Together(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.7,
        max_tokens= 1000,
        top_k=50,
    )
    prompt = ChatPromptTemplate.from_template(
        "<s>[INST] Answer the question in a simple sentence based only on the following context:\n{context}\n\nQuestion: {question} [/INST] "
    )
    return prompt | model | StrOutputParser()

def main():
    chunks = load_and_split_documents()
    print("Checkpoint 1")
    texts = [chunk.page_content for chunk in chunks]
    print("Checkpoint 2")
    embeddings = create_embeddings(chunks)
    print("Checkpoint 3")
    retriever = setup_vector_store(texts, embeddings)
    print("Checkpoint 4")
    chain = setup_query_interface(retriever)
    print("Checkpoint 5")
    
    input_query = "Tell me something about the compnay's risk factors based on these documents over the years."
    output = chain.invoke({"context": retriever, "question": input_query})
    print(output)

if __name__ == "__main__":
    main()
