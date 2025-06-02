from sqlalchemy import Column, DateTime, Integer, String, func

from src.database import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    city = Column(String)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return self.user_id
