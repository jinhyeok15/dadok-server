from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base, create_now, modified_now


class User(Base):
    __tablename__ = "users"

    id = Column(String(120), primary_key=True, index=True)
    user_name = Column(String(20))
    gender = Column(String(4), nullable=True)
    back_phone_number = Column(String(4))
    phone_number = Column(String(16), nullable=True)
    email = Column(String(25), nullable=True)
    naver_id = Column(String(60), nullable=True)
    instagram_id = Column(String(60), nullable=True)
    is_active = Column(Boolean, default=True)

    created = Column(DateTime(timezone=True), default=create_now)
    modified = Column(DateTime(timezone=True), onupdate=modified_now)

    items = relationship("Purchase", back_populates="user")
    pocket = relationship("Pocket", back_populates="user")
    challange_books = relationship("ChallangeBook", back_populates='user')
    challange_logs = relationship("ChallangeLog", back_populates='user')

    @staticmethod
    def generate_id(user_name, phone_number) -> str:
        user_name_id = "".join([str(ord(s)) for s in user_name])
        return user_name_id + phone_number


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String(60))
    title = Column(String(60), index=True)
    discount_level = Column(String(10), comment="퍼센트 할인 50 p; 가격 할인 p 5000 (무료면 100 p)")
    price = Column(Integer)
    certification = Column(Boolean)
    item_point = Column(Integer, nullable=True)
    units = Column(Integer)
    ticket_num = Column(Integer, nullable=True)
    link = Column(String(500))
    image_url = Column(String(500))
    fee = Column(Integer, nullable=True)

    users = relationship("Purchase", back_populates="item")


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'))
    item_id = Column(ForeignKey('items.id'))
    status = Column(String(12), comment="CONFIRM/SUBMIT/DELETE/PURCHASED")

    created = Column(DateTime(timezone=True), default=create_now)
    modified = Column(DateTime(timezone=True), onupdate=modified_now)

    user = relationship("User", back_populates="items")
    item = relationship("Item", back_populates="users")


class Pocket(Base):
    __tablename__ = 'pockets'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(120), ForeignKey('users.id'))
    ticket_amount = Column(Integer)

    user = relationship("User", back_populates="pocket")


class Challange(Base):
    __tablename__ = 'challanges'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), comment="1차")
    start_date = Column(String(12), comment="2022-03-14")
    end_date = Column(String(12), comment="2022-03-28")
    out_count_limit = Column(Integer)

    challange_books = relationship("ChallangeBook", back_populates='challange')


class ChallangeBook(Base):
    __tablename__ = 'challange_books'

    id = Column(Integer, primary_key=True)
    book_name = Column(String(80))
    publisher = Column(String(80), nullable=True)
    user_id = Column(String(120), ForeignKey('users.id'))
    challange_id = Column(Integer, ForeignKey('challanges.id'))

    user = relationship("User", back_populates='challange_books')
    challange = relationship("Challange", back_populates='challange_books')


class ChallangeLog(Base):
    __tablename__ = 'challange_logs'

    id = Column(Integer, primary_key=True)
    challange_id = Column(Integer, ForeignKey('challanges.id'))
    user_id = Column(String(120), ForeignKey('users.id'))
    now_date = Column(String(12), comment="2022-03-15")
    link = Column(String(500), comment="챌린지 인증 링크")
    status = Column(String(10), comment="SUCCESS/FAIL")

    user = relationship("User", back_populates='challange_logs')
