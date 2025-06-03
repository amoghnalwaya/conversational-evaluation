from fastapi import FastAPI
from conversational_evaluation.api.routes import router

app = FastAPI(title="Conversational Belief Evaluation API")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Conversational Evaluation API"}
