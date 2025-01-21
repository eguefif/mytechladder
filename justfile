# Justfile

# Command to build and run the services using Docker Compose
web:
    cd nginx && docker compose up --build

# Command to run the application using Poetry and Uvicorn
run:
    cd backend/backend && poetry run uvicorn main:app --reload
