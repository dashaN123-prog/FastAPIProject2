from fastapi import FastAPI

from routers import category_router, product_router, user_router, admin_router, cart_router, size_router

app = FastAPI()
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(user_router.router)
app.include_router(admin_router.router)
app.include_router(cart_router.router)
app.include_router(size_router.router)