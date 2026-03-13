from sqlalchemy import Column, Integer, String
from connections import Base

class Products(Base):
    __tablename__ = "products_tbl"

    id = Column(Integer, primary_key=True)
    pname = Column(String(100))
    qty = Column(String(100))
   

    def __init__(self, pname, qty):
       self.pname=pname
       self.qty=qty
