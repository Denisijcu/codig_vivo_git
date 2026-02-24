from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelos Pydantic para validar los datos de entrada
class Product(BaseModel):
    id: int
    name: str
    price: float


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Order(BaseModel):
    order_id: int
    items: List[CartItem]


# Simulamos una base de datos en memoria para este ejemplo
products = [
    {"id": 1, "name": "Product A", "price": 20.99},
    {"id": 2, "name": "Product B", "price": 34.50}
]


# Función para simular la autenticación JWT (en un entorno real, esto sería más complejo)
def get_current_user():
    return "current-user-token"


@app.get("/products")
async def read_products(current_user=Depends(get_current_user)):
    return products


@app.post("/products", response_model=Product)
async def create_product(product: Product):
    if product.id <= 0:
        raise HTTPException(status_code=422, detail="Invalid ID for the product.")
    products.append(product.dict())
    return {"message": "Product created successfully."}


@app.get("/cart")
async def read_cart(current_user=Depends(get_current_user)):
    # Aquí iría la lógica para leer el carrito del usuario
    return []


@app.post("/cart", response_model=CartItem)
async def add_to_cart(cart_item: CartItem):
    # Aquí iría la lógica para agregar un producto al carrito
    return {"message": "Product added to cart successfully."}


# Para este ejemplo, no implementamos las funciones de pedidos y autenticación JWT en el backend.