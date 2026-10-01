from fastapi import FastAPI

from controllers import pecas_controller, vendas_controller


app = FastAPI()

app.include_router(pecas_controller.router)
app.include_router(vendas_controller.router)

@app.get("/")
async def root():
    return None