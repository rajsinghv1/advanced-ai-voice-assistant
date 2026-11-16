# 🎙️ Advanced AI Voice Assistant

### An Agentic AI System Powered by Google Gemini, LangChain, RAG, and Voice Technologies

## 📌 Overview

Advanced AI Voice Assistant is an intelligent, Python-based Generative AI application designed to enable natural language conversations, voice interaction, and document-based question answering.

Built using **Google Gemini, LangChain, FastAPI, and Streamlit**, the application leverages Agentic AI and Retrieval-Augmented Generation (RAG) to process user queries, retrieve relevant information from PDF documents, and execute tasks through integrated AI tools.

The project demonstrates practical implementation of **LLM integration, AI agent orchestration, document retrieval, conversational memory, and speech processing** in a modular application.

## 🚀 Key Features

- **Agentic AI:** Uses LangChain agents to interpret user queries, select appropriate tools, and execute tasks.
- **Retrieval-Augmented Generation (RAG):** Processes PDF documents and retrieves relevant contextual information to answer user questions.
- **Conversational Memory:** Maintains conversation context to support multi-turn interactions.
- **Voice-Based Interaction:** Supports speech-to-text input and text-to-speech responses.
- **AI Tool Integration:** Provides task execution capabilities through document question-answering and calculator tools.
- **REST API Backend:** Uses FastAPI to expose application functionality through API endpoints.
- **Interactive User Interface:** Provides a Streamlit-based interface for text and voice interactions.
- **Modular Codebase:** Separates application components to improve maintainability and extensibility.

## 🧠 Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Large Language Model | Google Gemini |
| AI Framework | LangChain |
| AI Concepts | Agentic AI, RAG, LLMs, Prompt Engineering |
| Backend | FastAPI, REST API |
| Frontend | Streamlit |
| Document Processing | PyPDF2 |
| Speech Recognition | SpeechRecognition |
| Text-to-Speech | gTTS |
| Configuration | Python-dotenv |

## 🔄 Application Workflow

1. **User Interaction:** Users submit questions through text input or voice commands.
2. **Request Handling:** The Streamlit frontend communicates with the FastAPI backend.
3. **AI Agent Processing:** The LangChain agent analyzes the query and determines the appropriate action.
4. **Tool Selection:** The agent invokes the relevant tool, such as document retrieval or calculator operations.
5. **Context Retrieval:** The RAG pipeline retrieves relevant information from processed PDF documents.
6. **LLM Response Generation:** Google Gemini generates responses using the retrieved context and conversation history.
7. **Response Delivery:** The generated response is displayed in the interface and can be converted into speech.

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or later
- Git
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/rajsinghv1/advanced-ai-voice-assistant.git
cd advanced-ai-voice-assistant
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory using `.env.example`.

```env
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=your_supported_gemini_model
APP_NAME=Advanced AI Voice Assistant
```

**Get your Gemini API Key:** [Google AI Studio](https://aistudio.google.com/apikey)

Keep your API key private. Never commit your `.env` file to GitHub.

### 5. Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)

API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 6. Start the Streamlit Frontend

Open a second terminal, activate the virtual environment, and execute:

```bash
streamlit run frontend/streamlit_app.py
```

Application URL: [http://localhost:8501](http://localhost:8501)

## 💡 Example Use Cases

- Ask questions about uploaded PDF documents.
- Retrieve information from research papers and other documents.
- Perform mathematical calculations using the integrated calculator tool.
- Interact with the AI assistant using voice commands.
- Maintain context across conversational interactions.
- Receive AI-generated responses in text and speech formats.

## 👨‍💻 Developer

**Raj Singh**

Aspiring AI/ML Engineer | Generative AI | Agentic AI | Machine Learning | NLP

- **GitHub:** [rajsinghv1](https://github.com/rajsinghv1)
- **LinkedIn:** [Raj Singh](https://linkedin.com/in/rajsingh0510)
- **Email:** [rajsingh05102004@gmail.com](mailto:rajsingh05102004@gmail.com)

---

⭐ If you find this project useful, consider giving the repository a star.

**Developed with Python, Generative AI, and LangChain.**
