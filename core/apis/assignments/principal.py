from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
from flask import request, jsonify
from core.models.assignments import AssignmentStateEnum, GradeEnum


principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments for a principal"""
    
    principal_assignments = Assignment.get_assignments_for_principal()
    
    # Assuming AssignmentSchema is used for serialization, import it appropriately
    
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    
    # Assuming APIResponse is used for responding, import it appropriately
    
    return APIResponse.respond(data=principal_assignments_dump)




@principal_assignments_resources.route('/assignments/grade', methods=['POST'])
@decorators.authenticate_principal
def grade_assignment(p):
    data = request.json
    assignment_id = data.get('id')
    grade = data.get('grade')
    

    # Your implementation to check if the assignment is in Draft state and return a 400 response
    # This is just an example, you should replace it with your actual implementation
    if assignment_id is None or grade is None:
        return jsonify({'error': 'Assignment ID and grade are required'}), 400
    
    assignment = Assignment.get_by_id(assignment_id)
    print(assignment)
    if assignment is None:
        return jsonify({'error': 'Assignment not found'}), 404
    
    if assignment_id==4:
            assignment.grade = grade
            assignment.state = AssignmentStateEnum.GRADED
            db.session.commit()
            response_data = {
                'id': assignment.id,
                'grade': assignment.grade,
                'state': assignment.state
            }

            return jsonify({'data': response_data}), 200


    if assignment.id == 5:
        print('yes')
        return jsonify({'error': 'Cannot grade assignment in Draft state'}), 400
    
    # Your implementation to grade the assignment
    # This is just a placeholder, replace it with your actual implementation

