from flask import Blueprint, request, jsonify

skills_bp = Blueprint("skills_api", __name__)

skills = []
next_id = 1

@skills_bp.get("/admin/api/skills")
def get_skills():
    return jsonify(skills)

@skills_bp.post("/admin/api/skills")
def create_skill():
    global next_id
    data = request.json
    data["id"] = next_id
    next_id += 1
    skills.append(data)
    return jsonify({"message": "Habilidade criada", "skill": data})

@skills_bp.put("/admin/api/skills/<int:skill_id>")
def update_skill(skill_id):
    data = request.json
    for skill in skills:
        if skill["id"] == skill_id:
            skill.update(data)
            return jsonify({"message": "Habilidade atualizada", "skill": skill})
    return jsonify({"error": "Habilidade não encontrada"}), 404

@skills_bp.delete("/admin/api/skills/<int:skill_id>")
def delete_skill(skill_id):
    global skills
    skills = [s for s in skills if s["id"] != skill_id]
    return jsonify({"message": "Habilidade removida"})
