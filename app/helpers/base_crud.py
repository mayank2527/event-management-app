from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base


class BaseCrud:
    """
    Base class for all the crud db operations.
    """

    def __init__(self, model: Base):
        self.Model = model

    def read_all(self, db: Session, offset: int = 0, limit: int = 100) -> List[Base]:
        return db.query(self.Model).offset(offset).limit(limit).all()

    def read(self, db: Session, key: int) -> Base:
        return db.query(self.Model).filter(self.Model.id == key).first()

    def create(self, db: Session, schema_obj: BaseModel) -> Base:
        db_obj = self.Model(**schema_obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Base, schema_obj: BaseModel) -> Base:
        obj_data: dict = schema_obj.dict()
        for field, data in obj_data.items():
            setattr(db_obj, field, data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Base) -> Base:
        db.delete(db_obj)
        db.commit()
        return db_obj
