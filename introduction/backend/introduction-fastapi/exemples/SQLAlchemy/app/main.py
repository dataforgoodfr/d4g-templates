from fastapi import FastAPI
from app.api.product import router as product_router

app = FastAPI(
    title="Product API",
    description="API for managing products"
)

app.include_router(product_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)