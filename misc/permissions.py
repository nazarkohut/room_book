from misc.db_misc import session
from model.table.user import User


def is_hotel_owner(user_id: int) -> bool:
    hotel_owner = session.query(User.hotel_owner).filter(User.id == user_id).first()
    return hotel_owner.hotel_owner
