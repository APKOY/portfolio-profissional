from flask import Blueprint, request, jsonify

projects_bp = Blueprint("projects_api", __name__)

projects = []
next_id = 1

@projects_bp.get("/admin/api/projects")
def get_projects():
    return jsonify(projects)

@projects_bp.post("/admin/api/projects")
def create_project():
    global next_id
    data = request.json
    data["id"] = next_id
    next_id += 1
    projects.append(data)
    return jsonify({"message": "Projeto criado com sucesso", "project": data})

@projects_bp.put("/admin/api/projects/<int:project_id>")
def update_project(project_id):
    data = request.json
    for project in projects:
        if project["id"] == project_id:
            project.update(data)
            return jsonify({"message": "Projeto atualizado", "project": project})
    return jsonify({"error": "Projeto não encontrado"}), 404

@projects_bp.delete("/admin/api/projects/<int:project_id>")
def delete_project(project_id):
    global projects
    projects = [p for p in projects if p["id"] != project_id]
    return jsonify({"message": "Projeto removido"})
