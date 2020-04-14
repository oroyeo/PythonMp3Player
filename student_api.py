from flask import Flask, request
from student_manager import StudentManager
from student import Student
import json
import random

app = Flask(__name__)

student_mgr = StudentManager('student_db.sqlite')


@app.route('/student', methods=['POST'])
def add_student():
    """ Add a student to the database    """
    content = request.json

    try:
        student = Student(content['student_id'],
                          content['first_name'],
                          content['last_name'])
        student_mgr.add_student(student)

        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=400
        )
    return response


@app.route('/student/<string:student_id>', methods=['GET'])
def get_student(student_id):
    """ Get a student from the database """
    try:
        student = student_mgr.get_student(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} does not exist")

        response = app.response_class(
                status=200,
                response=json.dumps(student.to_dict()),
                mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
        return response


@app.route('/student/random', methods=['GET'])
def random_student():
    """ Return a random student from the database """
    try:
        names = student_mgr.get_all_students()

        if len(names) > 0:
            idx = random.randint(0, len(names) - 1)
            random_student = names[idx]
        else:
            raise ValueError("No Students in DB")

        response = app.response_class(
                status=200,
                response=json.dumps(random_student.to_dict()),
                mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
        return response


@app.route('/student/<string:student_name>', methods=['DELETE'])
def delete_student(student_name):
    """ Delete a student from the DB   """
    try:
        student_mgr.delete_student(student_name)

        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
    return response


@app.route('/student/names', methods=['GET'])
def get_all_names():
    """ Return a list of all student names    """
    names = student_mgr.get_all_students()

    response = app.response_class(
            status=200,
            response=json.dumps([s.to_dict() for s in names]),
            mimetype='application/json'
    )

    return response


@app.route('/student/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    """ Update the student information  """
    content = request.json

    try:
        student = student_mgr.get_student(student_id)
        student.first_name = content['first_name']
        student.last_name = content['last_name']
        student_mgr.update_student(student)
        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=400
        )

    return response

@app.route('/student/all', methods=['DELETE'])
def delete_all_students():
     """ Delete a student from the DB """
     try:
         student_mgr.delete_all_students()

         response = app.response_class(
             status=200
         )
     except ValueError as e:
         response = app.response_class(
             response=str(e),
             status=404
     )
     return response

if __name__ == "__main__":
    app.run(debug=True)
