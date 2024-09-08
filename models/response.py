from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime, timedelta
from enum import Enum
import jwt
import os

class ResponseStatusCode(Enum):
    SUCCESS = 200  # 성공
    FAIL = 401  # 실패
    FORBIDDEN = 403  # 접근 권한 없음
    NOT_FOUND = 404  # 경로 또는 자료를 찾을 수 없음 (보통 경로)
    TIME_OUT = 408  # 세션 만료됨
    CONFLICT = 409  # 데이터 충돌
    ENTITY_ERROR = 422  # 입력 데이터 타입이 잘못됨
    INTERNAL_SERVER_ERROR = 500  # 서버 내부 에러


class ExistErrorCode(Enum):
    USEFUL = 1  # 사용가능
    USERID = 2  # 아이디가 중복됨
    NICKNAME = 3  # 닉네임이 중복됨
    EMAIL = 4  # 이메일이 중복됨


class Detail:
    text: str | None

    def __init__(self, text: str | None):
        self.text = text


class ResponseModel:
    status_code: int

    @staticmethod
    def show_json(status_code: int, **kwargs):
        show_dict = {"status_code": status_code}
        for key in kwargs.keys():
            if kwargs[key]:
                show_dict[key] = kwargs[key]

        return JSONResponse(show_dict, status_code=status_code)

    @staticmethod
    def show_image(image_path: str):
        return FileResponse(path=image_path, media_type="image/png")


class TokenModel:
    access_token: str

    def __init__(self, user_uuid: str):
        acem = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        sk = os.getenv("SECRET_KEY")
        al = os.getenv("ALGORITHM")

        if acem and sk and al:
            self.access_token = jwt.encode(
                {
                    "sub": user_uuid,
                    "exp": datetime.now() + timedelta(minutes=float(acem)),
                },
                sk,
                algorithm=al,
            )
        else:
            raise FileNotFoundError(
                ".env파일에서 ACCESS_TOKEN_EXPIRE_MINUTES과 SECRET_KEY 환경 변수를 찾을 수 없습니다!"
            )

    @staticmethod
    def decode_token(access_token: str) -> str:
        acem = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        sk = os.getenv("SECRET_KEY")
        al = os.getenv("ALGORITHM")

        if acem and sk and al:
            payload = jwt.decode(access_token, sk, algorithms=[al])
            user_uuid = payload.get("sub")
            return user_uuid

        else:
            raise FileNotFoundError(
                ".env파일에서 ACCESS_TOKEN_EXPIRE_MINUTES과 SECRET_KEY 환경 변수를 찾을 수 없습니다!"
            )
