from sqlalchemy import Column, Integer, String
from db_config import Base

# EyeColorModel implementation
class EyeColorModel(Base):
    __tablename__ = "eye_color"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(255))
