from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime


class ResponseBase(BaseModel):
    code: int
    status: str


def response(code: int, status: str, data=None):
    if data:
        return {
            "code": code,
            "status": status,
            "data": data
        }
    return {
            "code": code,
            "status": status,
        }


class UserCreate(BaseModel):
    user_name: str
    back_phone_number: str


class UserBase(BaseModel):
    id: str
    user_name: str
    back_phone_number: str
    naver_id: Optional[str] = None
    instagram_id: Optional[str] = None
    is_active: bool


class PurchaseRequest(BaseModel):
    user_id: str
    status: str
    purchases: List[int]


class PurchaseCreate(BaseModel):
    user_id: str
    items: List[int]
    status: str


class PurchaseUserEssential(BaseModel):
    naver_id: str
    phone_number: str


class ItemDelete(BaseModel):
    user_id: str
    purchase_id: int


class ChallangeParticipate(BaseModel):
    challange_id: int
    user_id: str
    now_date: str
    link: Optional[str] = None
    status: str
    is_duplicate: bool = False
