from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, func, exists
from OCR_Shared.db import Db
from OCR_Shared.db import Base

class TaskState(Enum):
    NEW = 'NEW'
    PENDING = 'PENDING'
    DONE = 'DONE'
    FAILED = 'FAILED'

class OcrTaskModel(Base):
    __tablename__ = 'ocrTasks'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    awsid = Column('awsid', String(500))
    status = Column('status', String(40))
    created = Column('created', DateTime, default=func.now())

    @classmethod
    def find_by_id(cls, task_id):
        session = Db.get_db_session()
        task = session.query(cls).filter_by(id=task_id).first()
        session.close()
        return task

    @classmethod
    def delete_by_id(cls, task_id):
        session = Db.get_db_session()
        obj=session.query(cls).filter(cls.id==task_id).first()
        session.delete(obj)
        session.commit()
        session.close()
        return obj
    
    @classmethod
    def change_status(cls, task_id, status):
        session = Db.get_db_session()
        obj=session.query(cls).filter(cls.id==task_id).first()
        obj.status = status
        session.commit()   
        session.close()            

    @classmethod
    def check_if_exists(cls, task_id):
        session = Db.get_db_session()
        (ret, ) = session.query(exists().where(cls.id==task_id))
        session.close()        
        return ret


