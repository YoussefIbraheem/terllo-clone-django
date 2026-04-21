from app.services.project_service import (
    get_projects_by_owner,
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
)
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
)
from flask import Blueprint, request, jsonify

project_bp = Blueprint("project", __name__, url_prefix="/api/v1/projects")


@project_bp.route("/", methods=["GET"])
def projects_list():
    """
    Retrieve a paginated list of projects filtered by owner.
    """
    try:
        owner_id = request.args.get("owner_id")
        limit = request.args.get("limit")
        offset = request.args.get("offset")

        projects = get_projects_by_owner(owner_id=owner_id, limit=limit, offset=offset)
        data = [project.model_dump() for project in projects]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


@project_bp.route("/<int:project_id>", methods=["GET"])
def project_details(project_id: int):
    """
    Retrieve details of a specific project by ID.
    """
    try:
        project = get_project_by_id(project_id=project_id)
        return jsonify(project.model_dump()), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve project: {e}"}), 500


@project_bp.route("/", methods=["POST"])
def project_create():
    """
    Create a new project with provided data.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data found"}), 400

        project_data = ProjectCreate(**data)
        project = create_project(project_data=project_data)
        return jsonify(project.model_dump()), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create project:{str(e)}"})


@project_bp.route("/<int:project_id>", methods=["PUT"])
def project_update(project_id):
    """
    Update an existing project with new data.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data found"}), 400

        project_data = ProjectUpdate(**data)
        project = update_project(project_id=project_id, project_data=project_data)

        if not project:
            return jsonify({"error": {"project not found"}}), 404

        return jsonify(project.model_dump()), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create project:{str(e)}"})


@project_bp.route("/<int:project_id>", methods=["DELETE"])
def project_delete(project_id):
    """
        Delete a project by ID.
    """
    try:
        delete_project(project_id=project_id)
        return jsonify({"Project Deleted Successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete project: {str(e)}"}), 404
