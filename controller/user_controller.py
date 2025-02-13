from model.user import CreateUserModel, LoginModel, UpdateUserModel, User
from model.response import ResponseModel, ResponseStatusCode, Detail
from fastapi.security import OAuth2PasswordRequestForm
from service.user_service import UserService
from fastapi import APIRouter, Depends
from typing import Tuple

user_controller = APIRouter(
    prefix='/user',
    tags=['user']
)


@user_controller.get("", name="프로필 조회")
async def get_profile(result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저 정보를 성공적으로 불러왔습니다.", user=result.get_attributes())


@user_controller.post("", name="회원가입")
async def signup(user: CreateUserModel):
    status_code, result = UserService.signup(user)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="회원가입에 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저가 성공적으로 생성되었습니다.")


@user_controller.patch("", name="회원정보 업데이트")
async def update(form_data: UpdateUserModel, result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    status_code, result = UserService.update_user(
        result, form_data.password, form_data.nickname, form_data.email, form_data.avatar_path)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 수정하는데 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저 정보를 성공적으로 변경하였습니다.", user=result.get_attributes())


@user_controller.delete("", name="회원탈퇴")
async def signout(password: str, result: Tuple[ResponseStatusCode, User | Detail] = Depends(UserService.get_current_user)):
    status_code, result = result
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="유저 정보를 불러오는데 실패하였습니다.", detail=result.text)

    status_code, result = UserService.delete_user(result, password)
    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="회원탈퇴에 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="유저가 성공적으로 제거되었습니다.")


@user_controller.post("/auth/login", name="로그인")
async def login(form_data: LoginModel):
    status_code, result = UserService.login(
        form_data.user_id, form_data.password)

    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="아이디 또는 비밀번호가 잘못 입력되었습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="로그인에 성공하였습니다.", token={"access_token": result.access_token, "token_type": result.token_type})


@user_controller.post("/email/send", name="이메일 인증 코드 전송")
async def send_email(email: str):
    status_code, result = UserService.send_email_service(email)

    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="인정번호를 전송하는데 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="인증번호를 성공적으로 발송하였습니다.")


@user_controller.post("/email/verify", name="이메일 인증")
async def verify_email(email: str, verify_code: str):
    status_code, result = UserService.verify_email_service(email, verify_code)

    if isinstance(result, Detail):
        return ResponseModel.show_json(status_code=status_code, message="이메일 인증에 실패하였습니다.", detail=result.text)

    return ResponseModel.show_json(status_code=status_code, message="성공적으로 이메일 인증을 완료하였습니다.")


@user_controller.post("/token", name="토큰 발급")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    _, result = UserService.login(
        form_data.username, form_data.password
    )

    if isinstance(result, Detail):
        return None

    return {"access_token": result.access_token, "token_type": result.token_type}
