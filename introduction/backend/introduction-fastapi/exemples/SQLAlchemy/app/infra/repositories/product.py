from sqlalchemy.orm import sessionmaker
from app.domain.product import Product

# Assuming the session is already configured
Session = sessionmaker()
session = Session()

class ProductRepository:
    def get_products(self):
        db_products = session.query(Product).all()
        return [self.map_to_domain(product) for product in db_products]
    
    def map_to_domain(self, product):
        return Product(id=product.id, name=product.name, price=product.price) 