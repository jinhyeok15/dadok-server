from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas, crud, models
from .schemas import response
from .database import SessionLocal, engine
from .validations import *
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

admin_key = "ee0c1915-8251-4db6-8794-86e23f47d461"

# admin
@app.get("/admin/users")
def read_users(skip: int, limit: int, admin: str, db: Session=Depends(get_db)):
    if admin_key != admin:
        return response(403, "UNAUTHORIZED")
    users = crud.get_users(db, skip, limit)
    return response(200, "OK", users)

@app.get("/admin/challanges")
def read_challange_progresses(challange_id: int, skip: int, limit: int, admin: str, db: Session=Depends(get_db)):
    if admin_key != admin:
        return response(403, "UNAUTHORIZED")
    challange_progresses = crud.get_challange_progresses(db, challange_id, skip, limit)
    return response(
        200,
        "OK",
        challange_progresses
    )

@app.get("/admin/challange")
def read_challange_progress(challange_id: int, user_name: str, back_phone_number: str, admin: str, db: Session=Depends(get_db)):
    if admin_key != admin:
        return response(403, "UNAUTHORIZED")
    challange_progress = crud.get_challange_progress(db, challange_id, user_name, back_phone_number)
    if not challange_progress:
        return response(
            404,
            "NOT_FOUND"
        )
    return response(
        200,
        "OK",
        challange_progress
    )

# user
@app.get("/user")
def read_user(user_name: str, back_phone_number: str, db: Session=Depends(get_db)):
    user = crud.get_user_by_name_and_bpn(db, user_name, back_phone_number)
    if not user:
        raise HTTPException(404, "NOT_FOUND")

    return response(200, "OK", user)

@app.get("/user/participate")
def read_user_participate(user_name: str, back_phone_number: str, challange_id: int, db: Session=Depends(get_db)):
    user = crud.get_user_by_name_and_bpn(db, user_name, back_phone_number)
    if not user:
        return response(
            403, "UNAUTHORIZED"
        )

    challange_progress = crud.get_challange_progress(db, challange_id, user_name, back_phone_number)
    if not challange_progress:
        return response(
            404, "FAIL"
        )

    challange = crud.get_challange_info(db, challange_id)
    total_days = int(challange.end_date.split('-')[-1])-int(challange.start_date.split('-')[-1])
    
    if challange_progress.success_count<(total_days-challange.out_count_limit):
        return response(404, "FAIL")
    
    return response(200, "OK", user)

@app.get("/user/{user_id}")
def read_user_by_id(user_id: str, db: Session=Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        return response(404, "NOT_FOUND")
    return response(200, "OK", user)

@app.post("/user")
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    return crud.create_user(db, user)

# shop
@app.get("/shop/pocket/{user_id}")
def read_user_pocket_by_id(user_id: str, db: Session=Depends(get_db)):
    pocket = crud.get_user_pocket(db, user_id)
    if not pocket:
        return response(200, "NO_POCKET")
    return response(200, "OK", pocket)

@app.get("/shop/items")
def read_shop_items(skip: int, limit: int, db: Session=Depends(get_db)):
    items = crud.get_shop_items(db, skip, limit)
    return response(200, "OK", items)

@app.post("/shop/purchase")
async def create_shop_purchases(purchase: schemas.PurchaseCreate, db: Session=Depends(get_db)):
    user_id = purchase.user_id
    items = purchase.items
    status = purchase.status

    pocket = crud.get_user_pocket(db, user_id)
    if not pocket:
        raise HTTPException(404, "NOT_FOUND")
    
    ticket_amount = pocket.ticket_amount

    for item_id in items:
        item = crud.get_item(db, item_id)
        if status=="CONFIRM":
            item_ticket_amount = item.ticket_num
            if item_ticket_amount==0:
                if crud.is_purchased_item(db, user_id, item_id):
                    db.rollback()
                    return response(111, "CANNOT_PURCHASE")

            ticket_amount -= item_ticket_amount
            
            if ticket_amount < 0:
                db.rollback()
                return response(400, "OVER_AMOUNT")
        units = item.units-1

        if units<0:
            db.rollback()
            return response(112, "NO_UNIT")

        await crud.update_item_units(db, item_id, units)
        await crud.add_shop_purchase(db, user_id, item_id, status)

    await crud.update_user_pocket(db, user_id, ticket_amount)
    db.commit()
    return response(200, "OK")

@app.get("/shop/purchases/{user_id}")
def read_shop_purchases(user_id: str, status: str, db: Session=Depends(get_db)):
    purchases = crud.get_shop_purchases(db, user_id, status)
    return response(200, "OK", purchases)

@app.put("/shop/purchases/{user_id}")
async def update_shop_purchases(purchase: schemas.PurchaseRequest, db: Session=Depends(get_db)):
    user_id = purchase.user_id
    purchases = purchase.purchases
    status = purchase.status
    for purchase_id in purchases:
        await crud.update_shop_purchase(db, user_id, purchase_id, status)
    db.commit()
    data = crud.get_shop_purchases(db, user_id, status)
    return response(200, "OK", data)

@app.put("/shop/user/essential/{user_id}")
def update_shop_user_essential(user_id: str, essential: schemas.PurchaseUserEssential, db: Session=Depends(get_db)):
    if not validate_phone_number(essential.phone_number):
        return response(111, "NOT_VALID_PHONE_NUMBER")
    
    if not essential.naver_id or not essential.phone_number:
        return response(112, "NO_DATA")

    if crud.update_shop_user_essential(db, user_id, essential):
        return response(200, "OK")

    return response(404, "NOT_FOUND")

@app.delete("/shop/purchase")
async def delete_shop_purchase(item_delete: schemas.ItemDelete, db: Session=Depends(get_db)):
    user_id = item_delete.user_id
    purchase_id = item_delete.purchase_id
    purchase = crud.get_shop_purchase(db, purchase_id)
    item_id = purchase.item_id

    pocket = crud.get_user_pocket(db, user_id)
    if not pocket:
        raise HTTPException(404, "NOT_FOUND")
    user_ticket_amount = pocket.ticket_amount

    item = crud.get_item(db, item_id)
    item_ticket_amount = item.ticket_num
    ticket_amount = user_ticket_amount+item_ticket_amount

    if not crud.delete_shop_purchase(db, item_delete):
        return response(404, "NOT_FOUND")
    await crud.update_user_pocket(db, user_id, ticket_amount)
    await crud.update_item_units(db, item_id, item.units+1)

    db.commit()
    purchases = crud.get_shop_purchases(db, item_delete.user_id, "CONFIRM")
    return response(200, "OK", purchases)

# challange
@app.post("/challange/participate")
def create_challange_participate(challange: schemas.ChallangeParticipate, db: Session=Depends(get_db)):
    challange_id = challange.challange_id
    user_id = challange.user_id
    now_date = challange.now_date
    status = challange.status

    if crud.exists_challange_log(db, challange_id, user_id, now_date, status):
        if not challange.is_duplicate:
            return response(200, "CANNOT_CREATE")

    if crud.create_challange_participate(db, challange):
        return response(200, "OK")
    raise HTTPException(400, "INVALID_REQUEST")
