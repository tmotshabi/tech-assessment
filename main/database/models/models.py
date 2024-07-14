from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, String
from main.app import db

class Property(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    rate_number = Column(String, nullable=False)
    legal_description = Column(String(200), nullable=False)
    address = Column(String(200), nullable=False)
    first_owner = Column(String(100), nullable=False)
    use_code = Column(String(50), nullable=False)
    rating_category = Column(String(50), nullable=False)
    market_value = Column(Float, nullable=False)
    registered_extent = Column(String(100), nullable=False)
    roll = Column(String(100), nullable=False)


    def json(self):
       return {
            "rate_number": self.rate_number,
            "legal_description": self.legal_description,
            "address": self.address,
            "first_owner": self.first_owner,
            "use_code": self.use_code,
            "rating_category": self.rating_category,
            "market_value": float(self.market_value),
            "registered_extent": self.registered_extent,
            "roll": self.roll,      
        }