from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import literature

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the literature router
app.include_router(literature.router)

# Add after including the router
for route in app.routes:
    print(f"Registered route: {route.path}")

@app.get("/")
async def root():
    return {"message": "API is running"}

# ... rest of your FastAPI app configuration ... 