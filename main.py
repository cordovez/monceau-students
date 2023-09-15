from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.student_routes import student_router
from routers.events_routes import events_router


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(CORSMiddleware, 
                   allow_origins= origins, 
                   allow_credentials = True, 
                   allow_methods=["*"], 
                   allow_headers=["*"], )


app.include_router(student_router, prefix='/students')
app.include_router(events_router, prefix='/events')

@app.get('/')
def root():
    return {'message' : 'student data for JCCorman'}


if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app")