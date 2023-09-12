from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.student_routes import student_router

from controllers.playwright_results import login_and_extract_students
from controllers.results_to_dict import convert_tuples_to_dict

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

@app.get('/')
def root():
    return {'message' : 'student data for JCCorman'}


if __name__ == "__main__":
    uvicorn.run(reload=True, app="main:app")