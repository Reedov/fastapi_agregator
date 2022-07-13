from models.models_orm import RequestsLog
from models.database import get_session
from fastapi import Depends
from sqlalchemy.orm import Session


class LogRequestService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, **kwargs):
        log = RequestsLog(**kwargs)
        self.session.add(log)
        self.session.commit()
