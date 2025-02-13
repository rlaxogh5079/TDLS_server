from model.response import ResponseModel, ResponseStatusCode
from controller.user_controller import user_controller
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()
app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return ResponseModel.show_json(status_code=ResponseStatusCode.INTERNAL_SERVER_ERROR, message="서버 내부에서 오류가 발생하였습니다.", detail=str(exc))

app.include_router(user_controller)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ResponseModel.show_json(status_code=ResponseStatusCode.ENTITY_ERROR, message="데이터를 전송하는데 오류가 발생하였습니다.", detail=exc.__dict__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000 if os.path.exists("./is-server") else 3000,
        reload=not os.path.exists("./is-server"),
    )
