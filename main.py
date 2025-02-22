from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from english_learning_agent import EnglishLearningAgent

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize the English Learning Agent
agent = EnglishLearningAgent()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_card(request: Request, expression: str = Form(...)):
    card = await agent.generate_anki_card(expression)
    return templates.TemplateResponse(
        "card.html", 
        {
            "request": request,
            "card": card
        }
    ) 