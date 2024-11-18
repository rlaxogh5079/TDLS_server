from controllers.friend_controller import (
    request_friend,
    get_transmit_friend_list,
    get_friend_list,
    update_friend_status,
    get_receive_friend_list,
    get_block_friend_list,
)

from models.response import ResponseModel
from database.connection import DBObject
from models.friend import FriendStatus
from fastapi import APIRouter

friend_router = APIRouter(prefix="/friend", tags=["friend"])


@friend_router.post("/request")
async def request_friend_router(access_token: str, receive_user_uuid: str):
    status_code, detail = request_friend(DBObject(), access_token, receive_user_uuid)
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="친구 요청을 성공적으로 보냈습니다!",
        detail=detail.text,
    )


@friend_router.get("/list")
async def get_friend_list_router(access_token: str):
    status_code, result = get_friend_list(DBObject(), access_token)
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="성공적으로 친구 목록을 불러왔습니다!",
        friend_list=result,  # type: ignore
    )


@friend_router.get("/list/transmit")
async def get_transmit_friend_list_router(access_token: str):
    status_code, result = get_transmit_friend_list(DBObject(), access_token)
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="성공적으로 친구 요청 목록을 불러왔습니다!",
        friend_list=result,  # type: ignore
    )


@friend_router.get("/list/receive")
async def get_receive_friend_list_router(access_token: str):
    status_code, result = get_receive_friend_list(DBObject(), access_token)
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="성공적으로 친구 요청 목록을 불러왔습니다!",
        friend_list=result,  # type: ignore
    )


@friend_router.get("/list/block")
async def get_block_friend_list_router(access_token: str):
    status_code, result = get_block_friend_list(DBObject(), access_token)
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="성공적으로 친구 목록을 불러왔습니다!",
        friend_list=result,  # type: ignore
    )


@friend_router.post("/update")
async def update_friend_status_router(
    access_token: str, target_user_uuid: str, status: FriendStatus
):
    status_code, detail = update_friend_status(
        DBObject(), access_token, target_user_uuid, status
    )
    return ResponseModel.show_json(
        status_code=status_code.value,
        message="친구 요청 상태를 변경하였습니다.",
        detail=detail.text,
    )
