from app.services.project_service import(
    get_projects_by_owner,
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
)
from app.schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from typing import List, Optional

projects_bp = Blueprint("projects", __name__, url_prefix="/api/v1/projects")


@projects_bp.route("/", methods=["GET"])
def projects_list():
    """
    Retrieve a paginated list of projects filtered by owner.

    Query Parameters:
        owner_id (int): The ID of the project owner to filter by.
        limit (int): Maximum number of projects to return.
        offset (int): Number of projects to skip for pagination.

    Returns:
        dict: JSON response containing a list of project dictionaries.

    Example:
        GET /api/v1/projects?owner_id=1&limit=10&offset=0
    """
    owner_id = request.args.get("owner_id")
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    projects = get_projects_by_owner(owner_id=owner_id, limit=limit, offset=offset)

    data = [project.model_dump() for project in projects]

    return jsonify(data)


@projects_bp.route("/<int:project_id>", methods=["GET"])
def project_details(project_id: int):
    """
    Retrieve details of a specific project by ID.

    Args:
        project_id (int): The ID of the project to retrieve.

    Returns:
        dict: JSON response containing project details if found.
        tuple: JSON error response with 404 status if project not found.

    Raises:
        404: Project with given ID does not exist.

    Example:
        GET /api/v1/projects/1
    """
    project = get_project_by_id(project_id=project_id)

    if not project:
        return jsonify({"error:Project Not Found"}), 404

    return jsonify(project.model_dump), 200


@projects_bp.route("/", methods=["POST"])
def project_create():
    """
    Create a new project with provided data.

    Request Body:
        dict: JSON object containing project creation data conforming to ProjectCreate schema.

    Returns:
        dict: JSON response containing the created project with 201 status.
        tuple: JSON error response with 400 status if no data provided.

    Raises:
        400: No JSON data provided in request body.
        ValidationError: Request data does not match ProjectCreate schema.

    Example:
        POST /api/v1/projects
        Body: {"name": "My Project", "description": "..."}
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


@projects_bp.route("/<int:project_id>", methods=["PUT"])
def project_update(project_id):
    """
    Update an existing project with new data.

    Args:
        project_id (int): The ID of the project to update.

    Request Body:
        dict: JSON object containing project update data conforming to ProjectUpdate schema.

    Returns:
        dict: JSON response containing the updated project with 201 status.
        tuple: JSON error response with 400 status if no data provided.
        tuple: JSON error response with 404 status if project not found.

    Raises:
        400: No JSON data provided in request body.
        404: Project with given ID does not exist.
        ValidationError: Request data does not match ProjectUpdate schema.

    Example:
        PUT /api/v1/projects/1
        Body: {"name": "Updated Project Name"}
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


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
def project_delete(project_id):
    """
    Delete a project by ID.

    Args:
        project_id (int): The ID of the project to delete.

    Returns:
        dict: JSON success response with 200 status if deletion successful.
        tuple: JSON error response with 404 status if project not found or deletion failed.

    Raises:
        404: Project with given ID does not exist or deletion failed.

    Example:
        DELETE /api/v1/projects/1
    """
    deleted_project = delete_project(project_id=project_id)

    if not deleted_project:
        return jsonify({"error": "Failed to delete project"}), 404

    return jsonify({"Project Deleted Successuflly!"}), 200
