from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel

app = FastAPI(title="Module3.1", version="1.0")

class StudentCreate(BaseModel):
    name: str
    course: str
    gpa: Optional[float] = None

class StudentInDB(StudentCreate):
    id: int

student_db: List[StudentInDB] = []
student_id_counter = 0

def _find_student_index(student_id: int) -> Optional[int]:
    for idx, student in enumerate(student_db):
        if student.id == student_id:
            return idx
    return None

@app.post("/students", response_model=StudentInDB, status_code=201)
def create_student(student: StudentCreate):
    global student_id_counter
    student_id_counter += 1
    new_student = StudentInDB(id=student_id_counter, **student.dict())
    student_db.append(new_student)
    return new_student

@app.get("/students", response_model=List[StudentInDB])
def read_students(course: Optional[str] = Query(None, description="Filter by course")):
    if course:
        return [s for s in student_db if s.course.lower() == course.lower()]
    return student_db

@app.get("/students/{student_id}", response_model=StudentInDB)
def read_student(student_id: int = Path(..., description="The ID of the student to retrieve")):
    idx = _find_student_index(student_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_db[idx]

@app.put("/students/{student_id}", response_model=StudentInDB)
def update_student(student: StudentCreate, student_id: int = Path(..., description="The ID of the student to update")):
    idx = _find_student_index(student_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = StudentInDB(id=student_id, **student.dict())
    student_db[idx] = updated
    return updated

@app.delete("/students/{student_id}")
def delete_student(student_id: int = Path(..., description="The ID of the student to delete")):
    idx = _find_student_index(student_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student_db.pop(idx)
    return {"message": "Student deleted successfully"}
