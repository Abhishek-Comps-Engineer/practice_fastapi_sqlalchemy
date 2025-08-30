from fastapi import FastAPI
from app.routers import auth
from . routers import post, user, vote
from fastapi.middleware.cors import CORSMiddleware

# Create tables in database
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def get():
   return {"data": "Successfully"}


