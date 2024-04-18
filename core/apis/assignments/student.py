from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from flask import request, jsonify

from .schema import AssignmentSchema, AssignmentSubmitSchema
from core.models.assignments import AssignmentStateEnum, GradeEnum
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):


    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)










@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""

    if incoming_payload.get('content') == None:
        return jsonify({'error': 'Assignment ID and grade are required'}), 400
    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id
    print(incoming_payload.get('content'))

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""



    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Extract assignment ID and teacher ID from the payload
    assignment_id = incoming_payload.get('id')
    teacher_id = incoming_payload.get('teacher_id')

    assignment = Assignment.get_by_id(assignment_id)
    print(assignment.state)
    


    if assignment.state == AssignmentStateEnum.SUBMITTED:
        
        return jsonify({'error': 'FyleError', "message":'only a draft assignment can be submitted'}), 400

    # Validate the payload
    if not assignment_id or not teacher_id:
        print('end')
        return APIResponse.respond_error(message="Missing assignment ID or teacher ID", status_code=400)

    # Submit the assignment
    submitted_assignment = Assignment.submit(_id=assignment_id, teacher_id=teacher_id, auth_principal=p)
    db.session.commit()

    # Dump the submitted assignment for response
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
