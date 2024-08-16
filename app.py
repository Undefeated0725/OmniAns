import glob
import os
from asyncflows import AsyncFlows
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import List

class PDFChatbot:
    def __init__(self, document_folder='documents', config_file='omniAns.ai.yaml'):
        self.document_folder = document_folder
        self.config_file = config_file
        self.flow = None
        self.conversation_history = []
        self.load_documents()

    def load_documents(self):
        document_paths = glob.glob(os.path.join(self.document_folder, "*/*.pdf"))
        self.flow = AsyncFlows.from_file(self.config_file).set_vars(
            pdf_filepaths=document_paths,
        )

    async def ask(self, message):
        query_flow = self.flow.set_vars(
            message=message,
            conversation_history=self.conversation_history,
        )
        result = await query_flow.run()
        self.conversation_history.extend([
            f"User: {message}",
            f"Assistant: {result}",
        ])
        return result

    def get_next_folder_number(self):
        existing_folders = glob.glob(os.path.join(self.document_folder, '*'))
        existing_numbers = [int(os.path.basename(folder)) for folder in existing_folders if os.path.basename(folder).isdigit()]
        return max(existing_numbers, default=0) + 1

app = FastAPI()
chatbot = PDFChatbot()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    next_folder_number = chatbot.get_next_folder_number()
    folder_path = os.path.join(chatbot.document_folder, str(next_folder_number))
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_location = os.path.join(folder_path, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

    chatbot.load_documents()
    return RedirectResponse(url="/", status_code=303)

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    response = await chatbot.ask(question)
    return {"response": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
