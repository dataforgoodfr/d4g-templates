from app.infra.repositories.product import ProductRepository

class ProductUsecase:
    def get_products(self):
        return ProductRepository().get_products() 