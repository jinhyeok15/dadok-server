from sqlalchemy.orm import Session
from sqlalchemy import func, and_, exists
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()

def get_user_by_name_and_bpn(db: Session, user_name: str, back_phone_number: str):
    return db.query(models.User).filter_by(
            user_name=user_name, 
            back_phone_number=back_phone_number
        ).one_or_none()

def get_user_by_naver_id(db: Session, naver_id: str):
    return db.query(models.User).filter(models.User.naver_id == naver_id).one_or_none()

def get_users(db: Session, skip: int=0, limit: int=10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    user_name = user.user_name
    back_phone_number = user.back_phone_number
    user_id = models.User.generate_id(user_name, back_phone_number)
    if get_user(db, user_id):
        return None
    db_user = models.User(id=user_id, user_name=user_name, back_phone_number=back_phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_challange_progresses(db: Session, challange_id: int, skip: int=0, limit: int=30):
    return db.query(
                models.Challange.title.label("challange_title"),
                models.User.user_name,
                models.User.back_phone_number,
                func.count(models.ChallangeLog.user_id).label("success_count")
            ).join(
                models.Challange, models.ChallangeLog.challange_id==models.Challange.id
            ).join(
                models.User, models.ChallangeLog.user_id==models.User.id
            ).filter(
                and_(
                    models.ChallangeLog.challange_id==challange_id,
                    models.ChallangeLog.status.in_(['SUCCESS', 'EXCEPT'])
                )
        ).group_by(models.ChallangeLog.user_id).offset(skip).limit(limit).all()

def get_challange_progress(db: Session, challange_id: int, user_name: str, back_phone_number):
    user = get_user_by_name_and_bpn(db, user_name, back_phone_number)
    user_id = user.id
    return db.query(
                models.Challange.title.label("challange_title"),
                models.User.user_name,
                models.User.back_phone_number,
                models.User.id,
                func.count(models.ChallangeLog.user_id).label("success_count")
            ).join(
                models.Challange, models.ChallangeLog.challange_id==models.Challange.id
            ).join(
                models.User, models.ChallangeLog.user_id==models.User.id
            ).filter(
                and_(
                    models.ChallangeLog.challange_id==challange_id,
                    models.ChallangeLog.status.in_(['SUCCESS', 'EXCEPT']),
                    models.User.id==user_id
                )
        ).group_by(models.ChallangeLog.user_id).one_or_none()

def get_challange_info(db: Session, challange_id: int):
    return db.query(models.Challange).filter(models.Challange.id==challange_id).one_or_none()

def create_challange_participate(db: Session, challange: schemas.ChallangeParticipate) -> bool:
    challange_id = challange.challange_id
    user_id = challange.user_id
    link = challange.link
    now_date = challange.now_date
    status = challange.status
    db_challange_log = models.ChallangeLog(
        challange_id=challange_id,
        user_id=user_id,
        link=link,
        now_date=now_date,
        status=status
    )
    try:
        db.add(db_challange_log)
        db.commit()
        db.refresh(db_challange_log)
        return True
    except:
        return False

def exists_challange_log(db: Session, challange_id: int, user_id: str, now_date: str, status: str):
    return db.query(exists().where(
        models.ChallangeLog.challange_id==challange_id,
        models.ChallangeLog.user_id==user_id,
        models.ChallangeLog.now_date==now_date,
        models.ChallangeLog.status==status
    )).scalar()

def get_user_pocket(db: Session, user_id: str):
    pocket = db.query(models.Pocket).filter(models.Pocket.user_id==user_id).one_or_none()
    return pocket

async def update_user_pocket(db: Session, user_id: str, ticket_amount: int) -> bool:
    pocket = db.query(models.Pocket).filter(models.Pocket.user_id==user_id).one_or_none()
    if pocket:
        pocket.ticket_amount = ticket_amount
        return True
    return False

def get_shop_items(db: Session, skip: int=0, limit: int=8):
    return db.query(models.Item).order_by(models.Item.ticket_num).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id==item_id).one_or_none()

async def update_item_units(db: Session, item_id: int, units: int):
    item = db.query(models.Item).filter(models.Item.id==item_id).one_or_none()
    if item:
        item.units = units
        return True
    return False

async def add_shop_purchase(db: Session, user_id: str, item_id: int, status: str):
    db_purchase = models.Purchase(user_id=user_id, item_id=item_id, status=status)
    db.add(db_purchase)
    return

def get_shop_purchases(db: Session, user_id: str, status: str):
    return db.query(models.Purchase, models.Item).join(
        models.Item, models.Purchase.item_id==models.Item.id
    ).filter(
            and_(
                models.Purchase.user_id==user_id,
                models.Purchase.status==status
            )
        ).all()

def is_purchased_item(db: Session, user_id: str, item_id: int):
    return db.query(
        exists().where(
            models.Purchase.user_id==user_id,
            models.Purchase.status!="DELETE",
            models.Purchase.item_id==item_id
        )
    ).scalar()

def get_shop_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.id==purchase_id).one_or_none()

async def update_shop_purchase(db: Session, user_id: str, purchase_id: int, status: str):
    try:
        purchase = db.query(models.Purchase).filter(
            and_(
                models.Purchase.id==purchase_id,
                models.Purchase.user_id==user_id
            )
        ).one_or_none()

        purchase.status = status
    except:
        db.rollback()

def update_shop_user_essential(db: Session, user_id: str, essential: schemas.PurchaseUserEssential) -> bool:
    user = db.query(models.User).filter(models.User.id==user_id).one_or_none()
    if not user:
        return False
    user.naver_id = essential.naver_id
    user.phone_number = essential.phone_number
    db.commit()
    return True

def delete_shop_purchase(db: Session, item_delete: schemas.ItemDelete) -> bool:
    item = db.query(models.Purchase).filter(
        models.Purchase.id==item_delete.purchase_id
    ).one_or_none()
    
    if not item:
        return False

    item.status = "DELETE"
    db.commit()
    return True
