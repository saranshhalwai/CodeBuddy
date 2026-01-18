# CodeBuddy: CF Prerequisite Analyzer

CodeBuddy is a comprehensive tool designed to help competitive programmers on Codeforces understand the prerequisites for solving specific problems. It leverages the power of **Google Gemini** to analyze problem statements and determine the necessary algorithms and data structures.

## 🚀 Tech Stack Highlights

This project utilizes cutting-edge Google technologies:
- **Google Cloud Run**: For scalable, serverless backend deployment.
- **Google Gemini API**: specifically the `gemini-2.5-flash-lite` model, for high-speed, intelligent text analysis.

## 📂 Project Components

The repository consists of three main components:

### 1. Backend Service
A **FastAPI** application acting as the central gateway. It manages user data, coordinates between the browser extension and the Agent API, and handles request logging and validation.
- **Path**: `/backend`
- **Deployment**: Deployed on **Google Cloud Run** for high availability and scalability.

### 2. Agent API
A specialized **FastAPI** service that interfaces with the LLM.
- **Path**: `/agent_api`
- **Functionality**: Uses **Google Gemini API** (`gemini-2.5-flash-lite`) to analyze Codeforces problems and extract prerequisite tags (e.g., "Dynamic Programming", "Graphs").
- **Deployment**: Deployed on **Google Cloud Run** for high availability and scalability.
- **Development Note**: While **Gemini** is the production engine, the codebase includes support for *Groq* (`llama-3.3-70b-versatile`) strictly for local development and testing purposes.

### 3. Chrome Extension ("CF Prerequisite Analyzer")
A browser extension that integrates directly into the Codeforces UI.
- **Path**: `/extension`
- **Feature**: Displays a "Prerequisites" section on Codeforces problem pages, fetched in real-time via the Backend and Agent API.
- **Note**: A fully working, packaged version of the extension has been provided in the submitted Google Doc.

## 🛠️ How to Run Locally

You can run the entire system locally using Docker Compose.

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd CodeBuddy
    ```

2.  **Environment Setup**:
    - Create a `.env` file in `agent_api/` with your API keys:
      ```env
      GEMINI_API_KEY=your_gemini_key
      # Optional: GROQ_API_KEY=your_groq_key (if enabling DEV_MODE)
      ```
    - Create a `.env` file in `backend/` if required (refer to `backend/main.py` for needed variables like `ML_SERVICE_URL`).

3.  **Start Services**:
    ```bash
    docker compose up --build
    ```
    This will start:
    - **Backend** on port `8000`
    - **Agent API** on port `9000`

## ☁️ Deployment

The backend services are designed to be deployed on **Google Cloud Run**.
The `compose.yaml` and separate `Dockerfile`s in each service directory provide the necessary build configurations.

## 📝 License
[MIT](LICENSE)
