from fastapi import FastAPI


def init_app():
    server = FastAPI()
    from chat.customer_router import router as customer_router
    from chat.shop_owner_router import router as shop_owner_router
    from chat.router import router
    server.include_router(customer_router)
    server.include_router(shop_owner_router)
    server.include_router(router)

    return server


app = init_app()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
