import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("LANGCHAIN_API_KEY"))


def get_pdf_text(pdf_docs):
    t=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            t+= page.extract_text()
    return  t

def get_text_chunks(t):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    c = text_splitter.split_text(t)
    return c

def get_vector_store(tchunk):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(tchunk, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(que):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(que)

    chain = get_conversational_chain()

    
    op = chain({"input_documents":docs, "question": que}, return_only_outputs=True)

    print(op)
    st.write("Reply: ", op["output_text"])




def main():
    st.set_page_config("AskPDF")
    st.header("Chat with PDF")
    st.markdown("""
    <style>
        .main-container {
            background-color: #f4f4f4;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 2px 2px 20px rgba(0,0,0,0.1);
        }
        .header {
            color: #4CAF50;
            text-align: center;
            font-size: 36px;
        }
        .subheader {
            font-size: 20px;
            color: #555;
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px;
        }
        .sidebar .stButton>button {
            background-color: #2196F3;
            color: white;
        }
    </style>

    """, unsafe_allow_html=True)

    que = st.text_input("Ask a Question from the selected PDF Files")

    if que:
        user_input(que)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                tchunk = get_text_chunks(raw_text)
                get_vector_store(tchunk)
                st.success("Done")



if __name__ == "__main__":
    main()