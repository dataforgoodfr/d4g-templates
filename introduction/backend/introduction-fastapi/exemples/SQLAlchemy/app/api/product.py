from fastapi import APIRouter
from app.usecases.product import ProductUsecase

router = APIRouter()    

@router.get("/products")
def get_products():
    return ProductUsecase().get_products() 