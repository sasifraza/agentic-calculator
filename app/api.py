from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import run_agent

app = FastAPI(
    title="Agentic Calculator API",
    description="Ask math questions in plain English. Claude does the rest.",
    version="1.0.0"
)

class TaskRequest(BaseModel):
    task: str

class TaskResponse(BaseModel):
    task: str
    answer: str

@app.get("/")
def root():
    return {"status": "running", "message": "Agentic Calculator API is live!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/calculate", response_model=TaskResponse)
def calculate(request: TaskRequest):
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    try:
        result = run_agent(request.task)
        return TaskResponse(task=request.task, answer=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))