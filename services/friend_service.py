from models.friend import Friend, FriendStatus
from sqlalchemy.orm.session import Session
from typing import List
import traceback
import logging


def request_friend_service(
    se: Session, transmit_user_uuid: str, receive_user_uuid: str
) -> bool:
    try:
        friend = Friend(transmit_user_uuid, receive_user_uuid)
        se.add(friend)
        se.commit()
        se.refresh(friend)
        return True

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def load_friend_request(
    se: Session, user_uuid: str, is_receive: bool = False
) -> List[Friend]:
    try:
        if is_receive:
            result = (
                se.query(Friend)
                .filter_by(transmit_user_uuid=user_uuid, status=FriendStatus.pending)
                .all()
            )

        else:
            result = (
                se.query(Friend)
                .filter_by(recieve_user_uuid=user_uuid, status=FriendStatus.pending)
                .all()
            )

        return result

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def load_friend_list(se: Session, user_uuid: str) -> List[Friend]:
    try:
        result = (
            se.query(Friend)
            .filter_by(status=FriendStatus.accepted)
            .filter(
                (Friend.transmit_user_uuid == user_uuid)
                | (Friend.receive_user_uuid == user_uuid)
            )
            .all()
        )

        return result

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def change_friend_request(
    se: Session,
    transmit_user_uuid: str,
    receive_user_uuid: str,
    set_status: FriendStatus,
) -> bool:
    try:
        friend = (
            se.query(Friend)
            .filter_by(
                transmit_user_uuid=transmit_user_uuid,
                receive_user_uuid=receive_user_uuid,
            )
            .first()
        )

        if not friend:
            raise KeyError("Friend request not founded")

        friend.status = set_status
        se.commit()
        return True

    except KeyError as e:
        return False

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def load_block_friend_uuid_list(se: Session, user_uuid: str) -> List[Friend]:
    try:
        result = (
            se.query(Friend)
            .filter_by(status=FriendStatus.block)
            .filter(
                (Friend.transmit_user_uuid == user_uuid)
                | (Friend.receive_user_uuid == user_uuid)
            )
            .all()
        )

        return [row[0] for row in result]

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e
