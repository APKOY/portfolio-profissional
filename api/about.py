from flask import Blueprint, request, jsonify

about_bp = Blueprint("about_api", __name__)

about_data = {
    "name": "Alexsander Motta",
    "role": "Desenvolvedor",
    "description": "",
}

@about_bp.get("/admin/api/about")
def get_about():
    return jsonify(about_data)

@about_bp.post("/admin/api/about")
def update_about():
    data = request.json
    about_data.update(data)
    return jsonify({"message": "Sobre atualizado", "about": about_data})
