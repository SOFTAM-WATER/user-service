from app.database.db import Base

class BaseModel(Base):
    __abstract__ = True