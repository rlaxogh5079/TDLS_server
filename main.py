from models.response import TDLSException, ResponseModel
from starlette.middleware.cors import CORSMiddleware
from routes.friend_router import friend_router
from routes.user_router import user_router
from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

app.include_router(user_router)
app.include_router(friend_router)


@app.exception_handler(TDLSException)
async def tdls_exception_handler(request: Request, exc: TDLSException):
    return ResponseModel.show_json(
        status_code=500,
        message="서버 내부 오류가 발생하였습니다",
        detail=exc.message,
    )


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
