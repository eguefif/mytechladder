# Justfile

list:
    just -l

# Command to build and run the services using Docker Compose
web:
    cd nginx && docker compose up --build

dev:
    cd nginx && cd content && cd MyTechLadder && npm run dev

# Command to run the application using Poetry and Uvicorn
backend:
    cd backend/backend && poetry run uvicorn main:app --reload
