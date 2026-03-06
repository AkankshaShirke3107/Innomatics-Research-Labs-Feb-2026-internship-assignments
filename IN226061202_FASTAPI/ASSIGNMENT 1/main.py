from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 2, "name": "Pen", "price": 10, "category": "Stationery", "in_stock": True}
]

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool

@app.get("/products")
def get_products():
    return products

@app.post("/add-product")
def add_product(product: Product):
    products.append(product.dict())
    return {"message": "Product added successfully"}


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    
    result = [p for p in products if p["category"] == category_name]

    if not result:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }



@app.get("/products/instock")
def get_instock_products():

    available = [p for p in products if p["in_stock"] == True]

    return {
        "in_stock_products": available,
        "count": len(available)
    }

@app.get("/store/summary")
def store_summary():

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return {"error": "Product not found"}