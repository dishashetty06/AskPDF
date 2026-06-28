# AskPDF: Retrieval-Augmented Generation (RAG) Chatbot

AskPDF is an interactive web application that allows users to upload multiple PDF documents and have context-aware conversations with their content.

---

## 🚀 Features

* **Multi-PDF Support:** Upload and process multiple large PDF documents simultaneously.
* **Intelligent Text Chunking:** Uses recursive character splitting to maintain context boundaries and semantic integrity.
* **Vector Semantic Search:** Embeds text chunks via Google's latest embedding models and handles rapid similarity mapping locally using Meta's FAISS index.
* **Context-Grounded QA:** Utilizes `gemini-2.5-flash` to generate highly detailed answers based strictly on the extracted context.
* **Modern UI:** Clean, responsive, sidebar-driven user interface styled directly within Streamlit.

---

## 🛠️ Tech Stack

* **Frontend Framework:** Streamlit
* **LLM Orchestration:** LangChain (LangChain Community, LangChain Google GenAI)
* **Foundation Models:** * Generation: `gemini-2.5-flash`
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **PDF Parsing:** PyPDF2

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dishashetty06/AskPDF.git
cd AskPDF
cd langhchain

```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install streamlit pypdf2 langchain langchain-community langchain-google-genai google-generativeai python-dotenv faiss-cpu

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and insert your Google Gemini API key:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here

```
---

## 💻 How to Run

Launch the Streamlit dashboard by executing the following command in your terminal:

```bash
streamlit run app.py
```

1. Open the local URL provided by Streamlit (usually `http://localhost:8501`).
2. Use the left **Sidebar Menu** to upload your PDF files.
3. Click **Submit & Process** and wait for the "Done" success status.
4. Type your question into the main screen input bar and press Enter to fetch context-grounded answers instantly.
