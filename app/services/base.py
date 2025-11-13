# app/services/base.py
from sqlalchemy.orm import Session

class BaseService:
    def __init__(self, repo):
        self.repo = repo

    def get_db(self, db: Session):
        return db
