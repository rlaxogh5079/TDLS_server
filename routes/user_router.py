from controllers.user_controller import (
    signup,
    login,
    signout,
    forgot_password,
    check_duplicate,
    get_profile,
    update_avatar,
)
from models.user import CreateUserModel, SignoutModel, ForgotPasswordModel
from models.response import ResponseStatusCode, ResponseModel
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import DBObject
from typing import Literal

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.put("/signup")
async def signup_router(model: CreateUserModel):
    response_dict = {
        ResponseStatusCode.SUCCESS: "회원가입에 성공하였습니다.",
        ResponseStatusCode.CONFLICT: "정보가 중복되었습니다.",
    }

    status_code, detail = signup(DBObject(), model)
    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value, message=response_dict[status_code]
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )


@user_router.delete("/signout")
async def signout_router(model: SignoutModel):
    response_dict = {
        ResponseStatusCode.SUCCESS: "회원탈퇴에 성공하였습니다.",
        ResponseStatusCode.FAIL: "회원탈퇴에 실패하였습니다.",
    }

    status_code, detail = signout(DBObject(), model)
    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value, message=response_dict[status_code]
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )


@user_router.post("/login")
async def login_router(model: OAuth2PasswordRequestForm = Depends()):
    response_dict = {
        ResponseStatusCode.SUCCESS: "로그인에 성공하였습니다.",
        ResponseStatusCode.FAIL: "로그인에 실패하였습니다.",
    }

    status_code, detail = login(DBObject(), model)  # type: ignore

    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            token=detail,
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,  # type: ignore
        )


@user_router.post("/forgot/password")
async def forgot_password_router(model: ForgotPasswordModel):
    response_dict = {
        ResponseStatusCode.SUCCESS: "성공적으로 비밀번호를 변경하였습니다!",
        ResponseStatusCode.FAIL: "비밀번호 변경에 실패하였습니다!",
    }

    status_code, detail = forgot_password(DBObject(), model)
    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value, message=response_dict[status_code]
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )


@user_router.post("/check/duplicate")
async def check_duplicate_info(
    option: Literal["user_id", "nickname", "email"], value: str
):
    response_dict = {
        ResponseStatusCode.SUCCESS: f"사용할 수 있는 {option}입니다!",
        ResponseStatusCode.CONFLICT: f"사용할 수 없는 {option}입니다! 다른 {option}을 입력해주세요",
    }
    status_code, detail = eval(f"check_duplicate(DBObject(), {option}=value)")
    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value, message=response_dict[status_code]
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )


@user_router.get("/profile")
async def get_user_profile(access_token: str):
    response_dict = {
        ResponseStatusCode.SUCCESS: "성공적으로 정보를 조회하였습니다.",
        ResponseStatusCode.NOT_FOUND: "유저 조회에 실패하였습니다.",
    }
    status_code, detail = get_profile(DBObject(), access_token)

    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            user_info=detail.get_attributes(),  # type: ignore
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )


@user_router.post("/update/avatar")
async def update_user_avatar(access_token: str, file: UploadFile = File(None)):
    response_dict = {
        ResponseStatusCode.SUCCESS: "프로필 이미지를 성공적으로 변경하였습니다!",
        ResponseStatusCode.FAIL: "프로필 이미지 변경에 실패하였습니다!",
    }

    status_code, detail = update_avatar(DBObject(), access_token, await file.read())
    if status_code == ResponseStatusCode.SUCCESS:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
        )

    else:
        return ResponseModel.show_json(
            status_code=status_code.value,
            message=response_dict[status_code],
            detail=detail.text,
        )
