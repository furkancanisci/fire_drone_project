from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Her yerden erişim için (test amaçlı)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Örnek olarak drone konumları değiştirilebilir.
drone_positions = {
    "drone1": {"latitude": 41.01, "longitude": 28.97},
    "drone2": {"latitude": 41.015, "longitude": 28.975},
}

@app.get("/positions")
async def get_positions():
    # Burada konumları dinamik güncelleyebiliriz (örneğin her çağrıda konumu biraz değiştir)
    # Ama şu an statik olarak bırakıyoruz.
    return JSONResponse(content=drone_positions)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
