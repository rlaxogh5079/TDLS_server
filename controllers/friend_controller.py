from services.friend_service import (
    request_friend_service,
    load_friend_list,
    load_friend_request,
    change_friend_request,
    load_block_friend_uuid_list,
)
from models.response import (
    ResponseStatusCode,
    Detail,
    TDLSException,
    TokenModel,
)
from services.user_service import read_user_by_uuid
from models.friend import FriendStatus, Friend
from database.connection import DBObject
from typing import Tuple, List, Dict, Any
from models.user import User


def request_friend(
    db: DBObject, access_token: str, receive_user_uuid: str
) -> Tuple[ResponseStatusCode, Detail]:
    try:
        transmit_user_uuid = TokenModel.decode_token(access_token)
        result = request_friend_service(
            db.session, transmit_user_uuid, receive_user_uuid
        )
        if result:
            return (ResponseStatusCode.SUCCESS, Detail(None))

        else:
            return (ResponseStatusCode.FAIL, Detail(None))

    except Exception as e:
        raise TDLSException(str(e))


def update_friend_status(
    db: DBObject, access_token: str, receive_user_uuid: str, status: FriendStatus
) -> Tuple[ResponseStatusCode, Detail]:
    try:
        transmit_user_uuid = TokenModel.decode_token(access_token)
        result = change_friend_request(
            db.session, transmit_user_uuid, receive_user_uuid, status
        )

        if result:
            return (ResponseStatusCode.SUCCESS, Detail(None))

        else:
            return (ResponseStatusCode.FAIL, Detail(None))

    except Exception as e:
        raise TDLSException(str(e))


def get_friend_list(
    db: DBObject, access_token: str
) -> Tuple[ResponseStatusCode, Detail | List[User]]:
    try:
        user_uuid = TokenModel.decode_token(access_token)
        friend_uuid_list = load_friend_list(db.session, user_uuid)
        friend_list = list(
            map(lambda x: read_user_by_uuid(db.session, x), friend_uuid_list)
        )

        return (ResponseStatusCode.SUCCESS, friend_list)

    except Exception as e:
        raise TDLSException(str(e))


def get_transmit_friend_list(
    db: DBObject,
    access_token: str,
) -> Tuple[ResponseStatusCode, Detail | List[Dict[str, Any]]]:
    try:
        user_uuid = TokenModel.decode_token(access_token)
        request_friend_list = load_friend_request(db.session, user_uuid, True)
        return (
            ResponseStatusCode.SUCCESS,
            list(
                map(
                    lambda x: {
                        "friend": (
                            read_user_by_uuid(
                                db.session, x.transmit_user_uuid
                            ).get_attributes()
                            if user_uuid == x.receive_user_uuid
                            else read_user_by_uuid(
                                db.session, x.receive_user_uuid
                            ).get_attributes()
                        ),
                        "status": Friend.convert_status_korean(x.status),
                        "created_at": x.created_at.strftime("%Y/%m/%d %H:%M:%S"),
                    },
                    request_friend_list,
                )
            ),
        )

    except Exception as e:
        raise TDLSException(str(e))


def get_receive_friend_list(
    db: DBObject,
    access_token: str,
) -> Tuple[ResponseStatusCode, Detail | List[Dict[str, Any]]]:
    try:
        user_uuid = TokenModel.decode_token(access_token)
        request_friend_list = load_friend_request(db.session, user_uuid, False)
        return (
            ResponseStatusCode.SUCCESS,
            list(
                map(
                    lambda x: {
                        "friend": (
                            read_user_by_uuid(
                                db.session, x.transmit_user_uuid
                            ).get_attributes()
                            if user_uuid == x.receive_user_uuid
                            else read_user_by_uuid(
                                db.session, x.receive_user_uuid
                            ).get_attributes()
                        ),
                        "status": Friend.convert_status_korean(x.status),
                        "created_at": x.created_at.strftime("%Y/%m/%d %H:%M:%S"),
                    },
                    request_friend_list,
                )
            ),
        )

    except Exception as e:
        raise TDLSException(str(e))


def get_block_friend_list(
    db: DBObject,
    access_token: str,
) -> Tuple[ResponseStatusCode, Detail | List[Dict[str, Any]]]:

    try:
        user_uuid = TokenModel.decode_token(access_token)
        block_friend_list = load_block_friend_uuid_list(db.session, user_uuid)
        return (
            ResponseStatusCode.SUCCESS,
            list(
                map(
                    lambda x: {
                        "friend": (
                            read_user_by_uuid(
                                db.session, x.transmit_user_uuid
                            ).get_attributes()
                            if user_uuid == x.receive_user_uuid
                            else read_user_by_uuid(
                                db.session, x.receive_user_uuid
                            ).get_attributes()
                        ),
                        "status": Friend.convert_status_korean(x.status),
                        "created_at": x.created_at.strftime("%Y/%m/%d %H:%M:%S"),
                    },
                    block_friend_list,
                )
            ),
        )

    except Exception as e:
        raise TDLSException(str(e))
