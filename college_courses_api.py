import json

from fastapi import FastAPI, HTTPException, status

import models


app = FastAPI()

filename = "courses.json"
with open(filename, "r") as f:
    json_data = json.load(f)

departments: dict[models.DepartmentName, models.Department] = {}

# Loop through all JSON departments and create the dataclass versions of everything
for dept_name_str, courses in json_data.items():

    # Course list that will be attached to a Department
    course_list = []
    # Turn all the courses into a Course dataclass
    for course_json in courses:
        course = models.Course(
            name=course_json["name"], level=course_json["level"], semester=course_json["semester"])
        course_list.append(course)

    dept_name = models.DepartmentName(dept_name_str)

    departments[dept_name] = models.Department(
        name=dept_name, courses=course_list)


@app.get("/departments")
async def list_departments() -> list[str]:
    return departments.keys()


@app.get("/departments/{dept_name}")
async def get_department(dept_name: models.DepartmentName) -> models.Department | dict:
    error = {"error": f"You gave me {
        dept_name}, but I don't have that department"}
    return departments.get(dept_name, error)

    # if dept_name in departments:
    #    return departments[dept_name].courses
    # else:
    #    return "Department Not Found"


@app.get("/departments/{dept_name}/courses")
async def list_courses(dept_name: models.DepartmentName) -> list[str]:
    return [course.name for course in departments[dept_name].courses]


@app.get("/departments/{dept_name}/courses/{course_name}")
async def get_course_info(dept_name: models.DepartmentName, course_name: str) -> models.Course:
    courses = departments[dept_name].courses

    for course in courses:
        if course.name == course_name:
            return course

    raise HTTPException(status_code=404, detail="No course found")


@app.post("/departments/{dept_name}/courses", status_code=status.HTTP_201_CREATED)
async def create_course(dept_name: models.DepartmentName, course: models.Course):
    departments[dept_name].courses.append(course)
    return "Course Created Successfully"


@app.put("/departments/{department_name}/courses/{course_name}")
async def update_course(dept_name: models.DepartmentName,
                        course_name: str,
                        updated_course: models.Course) -> str:
    # Find the course
    # Replace the course
    # return saying "Course updated successfully"

    courses = departments[dept_name].courses

    for course in courses:
        if course.name.casefold() == course_name.casefold():
            course.name = updated_course.name
            course.level = updated_course.level
            course.semester = updated_course.semester
            return "Course Updated Successfully"

    # Another Way:
    # for i, course in enumerate(courses):
            # if course.name.casefold() == course_name.casefold():
            # courses[i] = updated_course
            # return "Course updated successfully"

    courses.append(update_course)
    return "Course Created Successfully"


@app.delete("/departments/{department_name}/courses/{course_name}")
async def delete_course(dept_name: models.DepartmentName,
                        course_name: str) -> str:
    # Find the course
    # Delete the course
    # return saying "Course Deleted Successfully"

    courses = departments[dept_name].courses

    for course in courses:
        if course.name.casefold() == course_name.casefold():
            courses.remove(course)
            return "Course Deleted Successfully"

    # Another Way:
    # for i, course in enumerate(courses):
            # if course.name.casefold() == course_name.casefold():
            # courses[i] = updated_course
            # return "Course updated successfully"

    return "No course with that name exists"
