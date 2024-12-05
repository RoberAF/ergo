# models.py

from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DiarioEntry(Base):
    __tablename__ = 'diario_entries'

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    audio = Column(Text, nullable=True)  # Almacena audio en base64 (opcional)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "description": self.description,
            "content": self.content,
            "audio": self.audio
        }
