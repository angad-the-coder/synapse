import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain

# Load environment variables
load_dotenv('../.env.local')

class LangchainPipeline:
    def __init__(self):
        # Initialize OpenAI
        self.llm = ChatOpenAI(
            model_name=os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
            temperature=float(os.getenv('TEMPERATURE', 0.7)),
            max_tokens=int(os.getenv('MAX_TOKENS', 2000))
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize memory
        self.memory = ConversationBufferMemory()
        
        # Initialize conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        
        # Initialize vector store
        self.vector_store = None

    def create_vector_store(self, texts, collection_name=None):
        """Create a vector store from a list of texts"""
        if collection_name is None:
            collection_name = os.getenv('COLLECTION_NAME', 'default_collection')
            
        # Create vector store
        self.vector_store = FAISS.from_texts(
            texts,
            self.embeddings,
            collection_name
        )
        return self.vector_store

    def load_and_split_document(self, file_path):
        """Load and split a document into chunks"""
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return text_splitter.split_documents(documents)

    def query_vector_store(self, query, k=4):
        """Query the vector store for similar documents"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        return self.vector_store.similarity_search(query, k=k)

    def ask_question(self, question):
        """Ask a question using the conversation chain"""
        return self.conversation.predict(input=question)

    def create_custom_chain(self, prompt_template):
        """Create a custom chain with a specific prompt template"""
        prompt = PromptTemplate.from_template(prompt_template)
        return LLMChain(llm=self.llm, prompt=prompt)

    def create_qa_chain(self):
        """Create a question-answering chain"""
        return load_qa_chain(self.llm, chain_type="stuff")

# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = LangchainPipeline()
    
    # Example conversation
    response = pipeline.ask_question("What is artificial intelligence?")
    print(f"Response: {response}")
    
    # Example document processing
    texts = [
        "Artificial intelligence is the simulation of human intelligence by machines.",
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning is a type of machine learning based on artificial neural networks."
    ]
    
    # Create vector store
    vector_store = pipeline.create_vector_store(texts)
    
    # Query vector store
    results = pipeline.query_vector_store("What is machine learning?")
    print("\nSimilar documents:")
    for doc in results:
        print(f"- {doc.page_content}")
    
    # Create custom chain
    custom_prompt = """
    You are an AI expert. Please explain {concept} in simple terms.
    """
    custom_chain = pipeline.create_custom_chain(custom_prompt)
    response = custom_chain.run(concept="neural networks")
    print(f"\nCustom chain response: {response}")