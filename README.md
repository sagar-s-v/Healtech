LLM-Powered Intelligent Query–Retrieval System
This project is a full-stack application that allows users to upload documents (PDF, DOCX, EML) and ask natural language questions about their content. It uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers with explainable rationale. It's designed for domains like insurance, legal, HR, and compliance.

✨ Features
Multi-Format Document Processing: Ingests and extracts text from PDF, DOCX, and email (.eml) files.

Semantic Search: Uses vector embeddings to find the most relevant document clauses based on the meaning of the user's query.

Retrieval-Augmented Generation (RAG): Provides relevant text passages to a Large Language Model (LLM) to generate highly accurate, context-aware answers.

Explainable AI: Delivers not just an answer, but also the conditions, rationale, and the specific clauses used to make the decision.

Modern Tech Stack: Built with a robust FastAPI backend and a dynamic React frontend.

Scalable Architecture: Uses PostgreSQL for metadata and Pinecone as a dedicated vector database for efficient scaling.

User-Friendly Interface: Simple UI for uploading documents, selecting them, and asking questions.

Cancellable Queries: Includes a feature to cancel long-running LLM queries to improve user experience.

⚙️ Tech Stack
Backend: FastAPI, Python 3.9+, Gunicorn

Frontend: React.js, Axios

LLM: Google Gemini AI (easily switchable with OpenAI)

Vector Database: Pinecone

Relational Database: PostgreSQL

Embeddings: Sentence-Transformers

Text Splitting: LangChain

Data Validation: Pydantic

Database ORM: SQLAlchemy

🏛️ Architecture
The application follows a standard RAG pipeline architecture:

Code snippet

graph TD
    A[User's Browser <br/> React Frontend] -->|1. Upload/Query| B(FastAPI Backend);
    subgraph "Indexing Pipeline"
        B -->|2. Extract Text| C{Document Processor};
        C -->|3. Chunk Text| D[LangChain Text Splitter];
        D -->|4. Create Embeddings| E[Sentence-Transformer];
        E -->|5. Store Vectors| F[Pinecone Vector DB];
        B -->|6. Store Metadata| G[PostgreSQL Database];
    end
    subgraph "Query Pipeline"
        B -->|7. Embed Query| E;
        E -->|8. Semantic Search| F;
        F -->|9. Retrieve Context| B;
        B -->|10. Prompt + Context| H[Google Gemini AI];
        H -->|11. Structured JSON| B;
    end
    B -->|12. Final Answer| A;
📋 Prerequisites
Before you begin, ensure you have the following installed and configured:

Python 3.9+ and pip

Node.js and npm

A running PostgreSQL server

A Pinecone account and API key.

A Google AI (Gemini) API key.

Git for cloning the repository.

🚀 Setup and Installation
Follow these steps to get the project running locally.

1. Clone the Repository

git clone <your-repository-url>
cd <your-project-folder>
2. Backend Setup
Navigate into the backend directory and set up the environment.


cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Create a .env file in the backend/ directory and add your secret keys.
backend/.env

Ini, TOML

# PostgreSQL Database URL
DATABASE_URL="postgresql://YOUR_POSTGRES_USER:YOUR_POSTGRES_PASSWORD@localhost/your_db_name"

# API Keys
GOOGLE_API_KEY="your-google-ai-api-key"
PINECONE_API_KEY="your-pinecone-api-key"

# Pinecone Configuration
PINECONE_ENVIRONMENT="your-pinecone-environment"
PINECONE_INDEX_NAME="intelligent-query-system"
3. Frontend Setup
Navigate into the frontend directory in a new terminal

cd frontend

# Install dependencies
npm install
Create a .env file in the frontend/ directory.
frontend/.env

REACT_APP_API_BASE_URL=http://127.0.0.1:8000

▶️ Running the Application
You need to run both the backend and frontend servers simultaneously in two separate terminals.

Start the Backend Server (from the backend/ directory):

# Make sure your virtual environment is activated
uvicorn app.main:app --reload
The backend will be running at http://127.0.0.1:8000.

Start the Frontend Server (from the frontend/ directory):

npm start
Your browser will automatically open to http://localhost:3000.

You can now upload documents and start asking questions!
