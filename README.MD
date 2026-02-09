# AIFlow 🚀

AIFlow is a full-stack AI workflow automation platform that enables users to create, manage, and execute AI-powered workflows with an intuitive visual interface.

## ✨ Features

- **Visual Workflow Builder**: Create complex AI workflows using a drag-and-drop interface powered by React Flow
- **AI Chat Interface**: Interactive chat functionality integrated with your workflows
- **Knowledge Base Management**: Upload and manage documents (PDF, DOCX) for AI context
- **Workflow Execution**: Execute workflows with custom queries and get real-time results
- **Persistent Storage**: PostgreSQL/Supabase backend for reliable data storage
- **RESTful API**: Well-documented FastAPI backend for seamless integration

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with Supabase
- **ORM**: SQLAlchemy + SQLModel
- **AI Integration**: Google Gemini AI
- **Document Processing**: PyPDF, python-docx, pandas
- **Async Support**: asyncio, asyncpg

### Frontend
- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite
- **UI Components**: Radix UI
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **Workflow Canvas**: React Flow (@xyflow/react)
- **Routing**: React Router v7
- **Markdown Rendering**: React Markdown with LaTeX support

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL database (or Supabase account)
- Google Gemini API key

## 🚀 Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp sample.env .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_key
SUPABASE_BUCKET_KB=your_bucket_name
EMBEDDING_SIZE=256
EMBEDDING_KEY_GEMINI=your_gemini_api_key
FRONTEND_URL=http://localhost:5173
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp sample.env .env
```

Edit `.env` with your configuration:
```env
VITE_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 📖 Usage

### Creating a Workflow

1. Navigate to the home page
2. Click "Create" to open the workflow builder
3. Drag and drop nodes to create your workflow:
   - **Input Node**: Entry point for your workflow
   - **LLM Nodes**: AI processing nodes
   - **Output Node**: Final result node
4. Connect nodes to define the flow
5. Configure each node with appropriate settings
6. Save your workflow

### Running a Workflow

1. Go to the Chat interface
2. Select a workflow
3. Enter your query
4. View the AI-generated results

### Uploading Knowledge Base Files

1. Use the file upload feature
2. Upload PDF or DOCX files
3. Files are processed and stored in the knowledge base
4. Reference these files in your workflows

## 🔌 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /workflow/` - Create a new workflow
- `GET /workflow/{id}` - Get workflow details
- `POST /run/{workflow_id}` - Execute a workflow
- `POST /chat/create` - Create a new chat
- `POST /upload_kb_file` - Upload knowledge base file

## 🏗️ Project Structure

```
AIFlow/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # SQLModel schemas
│   │   ├── services/         # Business logic
│   │   ├── repositories/     # Data access layer
│   │   ├── llm/              # LLM integration
│   │   ├── embeddings/       # Vector embeddings
│   │   ├── text_extraction/  # Document processing
│   │   └── main.py           # Application entry point
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── apis/             # API client
    │   ├── components/       # React components
    │   ├── views/            # Page components
    │   ├── store/            # Redux store
    │   ├── types/            # TypeScript types
    │   └── main.tsx          # Application entry point
    └── package.json
```

## 🧪 Development

### Backend

Run with auto-reload:
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend

Run development server:
```bash
cd frontend
npm run dev
```

Build for production:
```bash
npm run build
```

Lint code:
```bash
npm run lint
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

License information is to be determined.

## 🐛 Issues

If you encounter any issues or have suggestions, please file an issue on the GitHub repository.

## 👨‍💻 Author

Created by [devshah23](https://github.com/devshah23)

---

**Note**: Make sure to keep your API keys and sensitive information secure. Never commit `.env` files to version control.
