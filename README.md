# PromptGuard

PromptGuard is a FastAPI-based microservice that provides prompt safety evaluation and prompt generation capabilities for AI-powered systems.  
It acts as a lightweight safety layer that evaluates user prompts for potential risks and generates safe, structured prompts using an external Large Language Model (LLM).

This project focuses on **DevSecOps best practices**, demonstrating a production-grade **CI/CD pipeline with Kubernetes-based deployment validation** using GitHub Actions.

---

## Features

- Prompt risk evaluation using an LLM
- Safe prompt generation for given tasks
- Health endpoint for runtime validation
- Dockerized FastAPI application
- Automated CI pipeline with security scanning
- Kubernetes-based CD pipeline using kind

---

## How to Run Locally

### Prerequisites

- Python 3.11 or higher  
- Docker  
- Git  

---

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Manan21st/PromptGuard.git
   cd PromptGuard
   ```

2. **Install Dependencies** (optional: create a venv)

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables**

    Create a .env file in the project root:

    ```bash
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

4. **Run the application**

    ```bash
    python src/main.py
    ```

    The API will be available at:  
    ```bash
    http://localhost:8000
    ```

5. **Run using Docker**

    ```bash
    docker build -t promptguard:local .
    docker run -p 8000:8000 -e GEMINI_API_KEY=your_gemini_api_key_here promptguard:local
    ```


## Secrets Configuration

Secrets are never hardcoded in the repository.

### GitHub Secrets Used
| Secret Name          | Purpose                          |
|----------------------|----------------------------------|
| DOCKERHUB_USERNAME  | DockerHub registry username     |
| DOCKERHUB_TOKEN     | DockerHub access token          |
| GEMINI_API_KEY      | API key for LLM integration (Optional for CI/CD, put placeholder such as "xxxxx")|

Secrets are configured at:  
GitHub Repository → Settings → Secrets and variables → Actions

## CI Pipeline Explanation

The Continuous Integration (CI) pipeline is implemented using GitHub Actions and runs on every push to the `main` branch or via manual trigger.

### CI Stages

1. **Checkout Source Code**  
   Retrieves the latest code from the repository.

2. **Setup Python Runtime**  
   Uses Python 3.11 for consistent and reproducible builds.

3. **Install Dependencies**  
   Installs application and test dependencies from `requirements.txt`.

4. **Code Quality – Linting (Ruff)**  
   Runs Ruff to check for code quality issues.

5. **SAST – CodeQL (Python)**  
   Performs static application security testing using CodeQL.

6. **SCA – Dependency Vulnerability Scan**  
   Uses pip-audit to scan for vulnerable dependencies.

7. **Unit Tests**  
   Executes pytest with mocked LLM calls to validate business logic.

8. **Docker Image Build**  
   Builds an immutable Docker image tagged with `latest` and the commit SHA.

9. **Container Vulnerability Scan**  
   Uses Trivy to detect OS and dependency vulnerabilities, scanning for CRITICAL and HIGH severity issues.

10. **Push Trusted Image**  
    Pushes the verified Docker image to DockerHub.

The CI pipeline follows a fail-fast approach to prevent insecure or faulty artifacts from progressing further.

## Continuous Deployment (CD) Overview

A separate Continuous Deployment (CD) workflow is implemented and will be triggered only after a successful CI run.

### CD Stages

1. Create a Kubernetes cluster using kind
2. Pull the trusted Docker image from DockerHub
3. Deploy the application using Kubernetes manifests
4. Wait for deployment rollout completion
5. Validate application availability using the /health endpoint
6. Optionally perform a runtime API smoke test

This ensures that every released artifact is secure, validated, and deployable in a Kubernetes environment.

## Project Structure
```
project-root/
├── .github/workflows/
│   └── ci.yml
│   └── cd.yml
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── src/
│   ├── api/
│   ├── core/
│   ├── tests/
│   └── main.py
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

Made with ❤️ by Manan

