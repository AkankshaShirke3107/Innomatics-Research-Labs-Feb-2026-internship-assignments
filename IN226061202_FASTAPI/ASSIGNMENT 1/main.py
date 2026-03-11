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

@app.put("/update-product/{product_id}")
def update_product(product_id: int, updated_product: Product):

    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product.dict()
            return {
                "message": "Product updated successfully",
                "product": updated_product
            }

    return {"error": "Product not found"}

@app.delete("/delete-product/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    return {"error": "Product not found"}

@app.put("/update-product/{product_id}")
def update_product(product_id: int, updated_product: Product):

    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product.dict()
            return {"message": "Product updated successfully"}

    return {"error": "Product not found"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# ----- Existing product list -----
products = [
    {"id": 1, "name": "Laptop", "price": 45000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 599, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 199, "category": "Stationery", "in_stock": True}
]

class Product(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool

# ----- Q1: Add new products -----
@app.post("/products")
def add_product(product: Product):
    # Check for duplicate by name
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    new_product = product.dict()
    new_product["id"] = new_id
    products.append(new_product)
    return {"message": "Product added successfully", "product": new_product}

# ----- Q5: Inventory Audit (Put before /products/{product_id}) -----
@app.get("/products/audit")
def inventory_audit():
    total_products = len(products)
    in_stock_count = sum(1 for p in products if p["in_stock"])
    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]
    total_stock_value = sum(p["price"] * 10 for p in products if p["in_stock"])  # assuming 10 units each
    most_expensive = max(products, key=lambda x: x["price"])
    
    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {"name": most_expensive["name"], "price": most_expensive["price"]}
    }

# ----- Q2: Update product (stock / price) -----
@app.put("/products/{product_id}")
def update_product(product_id: int, price: Optional[float] = None, in_stock: Optional[bool] = None):
    for p in products:
        if p["id"] == product_id:
            if price is not None:
                p["price"] = price
            if in_stock is not None:
                p["in_stock"] = in_stock
            return {"message": "Product updated", "product": p}
    raise HTTPException(status_code=404, detail="Product not found")

# ----- Q3: Delete a product -----
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            deleted = products.pop(i)
            return {"message": "Product deleted", "product": deleted}
    raise HTTPException(status_code=404, detail="Product not found")

# ----- Get all products -----
@app.get("/products")
def get_products():
    return products

# ----- Get single product by ID -----
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")