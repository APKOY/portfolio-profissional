from flask import Blueprint, request, jsonify

experiences_bp = Blueprint("experiences_api", __name__)

experiences = []
next_id = 1

@experiences_bp.get("/admin/api/experiences")
def get_experiences():
    return jsonify(experiences)

@experiences_bp.post("/admin/api/experiences")
def create_experience():
    global next_id
    data = request.json
    data["id"] = next_id
    next_id += 1
    experiences.append(data)
    return jsonify({"message": "Experiência criada", "experience": data})

@experiences_bp.put("/admin/api/experiences/<int:exp_id>")
def update_experience(exp_id):
    data = request.json
    for exp in experiences:
        if exp["id"] == exp_id:
            exp.update(data)
            return jsonify({"message": "Experiência atualizada", "experience": exp})
    return jsonify({"error": "Experiência não encontrada"}), 404

@experiences_bp.delete("/admin/api/experiences/<int:exp_id>")
def delete_experience(exp_id):
    global experiences
    experiences = [e for e in experiences if e["id"] != exp_id]
    return jsonify({"message": "Experiência removida"})
