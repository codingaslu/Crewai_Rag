from fastapi import FastAPI, Request
from routes import router as main_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

app.include_router(main_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("chat_qa.html", {"request": request})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
