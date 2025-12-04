from flask import Flask, render_template, jsonify, request, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ---------------------------------------------
# CONFIGURAÇÃO DO BANCO
# ---------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "portfolio.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------------------------------------
# MODELOS
# ---------------------------------------------
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    github_url = db.Column(db.String(250))
    demo_url = db.Column(db.String(250))
    date = db.Column(db.String(20))  # ex: 11/2025
    status = db.Column(db.String(50))  # ex: Em andamento, Concluído

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "technologies": self.technologies,
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "date": self.date,
            "status": self.status,
        }


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50))      # Iniciante, Intermediário, Avançado
    category = db.Column(db.String(100))  # Linguagem, Framework, Ferramenta

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "category": self.category,
        }


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150))
    description = db.Column(db.Text)
    start_date = db.Column(db.String(20))  # ex: 08/2024
    end_date = db.Column(db.String(20))    # ex: Atual ou 11/2025
    location = db.Column(db.String(150))
    current = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "company": self.company,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "current": self.current,
        }


# ---------------------------------------------
# ROTAS PÚBLICAS
# ---------------------------------------------
@app.route("/")
def index():
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.order_by(Skill.name).all()
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return render_template(
        "index.html",
        projects=projects,
        skills=skills,
        experiences=experiences,
    )


@app.route("/admin")
def admin():
    return render_template("admin.html")


# ---------------------------------------------
# DOWNLOAD DO CURRÍCULO
# ---------------------------------------------
@app.route("/download/curriculo")
def download_curriculo():
    uploads_path = os.path.join(app.root_path, "static", "uploads")
    return send_from_directory(
        uploads_path,
        "curriculo.pdf",
        as_attachment=True  # força o download
    )


# ---------------------------------------------
# API REST - PROJETOS
# ---------------------------------------------
@app.route("/api/projects", methods=["GET"])
def get_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return jsonify([p.to_dict() for p in projects])


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())


@app.route("/api/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        abort(400, description="Campos obrigatórios: title, description")

    project = Project(
        title=data["title"],
        description=data["description"],
        technologies=data.get("technologies", ""),
        github_url=data.get("github_url", ""),
        demo_url=data.get("demo_url", ""),
        date=data.get("date", ""),
        status=data.get("status", ""),
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@app.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json() or {}

    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.technologies = data.get("technologies", project.technologies)
    project.github_url = data.get("github_url", project.github_url)
    project.demo_url = data.get("demo_url", project.demo_url)
    project.date = data.get("date", project.date)
    project.status = data.get("status", project.status)

    db.session.commit()
    return jsonify(project.to_dict())


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Projeto excluído com sucesso"})


# ---------------------------------------------
# API REST - HABILIDADES
# ---------------------------------------------
@app.route("/api/skills", methods=["GET"])
def api_get_skills():
    skills = Skill.query.order_by(Skill.name).all()
    return jsonify([s.to_dict() for s in skills])


@app.route("/api/skills/<int:skill_id>", methods=["GET"])
def api_get_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    return jsonify(skill.to_dict())


@app.route("/api/skills", methods=["POST"])
def api_create_skill():
    data = request.get_json()
    if not data or "name" not in data:
        abort(400, description="Campo obrigatório: name")

    skill = Skill(
        name=data["name"],
        level=data.get("level", ""),
        category=data.get("category", ""),
    )
    db.session.add(skill)
    db.session.commit()
    return jsonify(skill.to_dict()), 201


@app.route("/api/skills/<int:skill_id>", methods=["PUT"])
def api_update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json() or {}

    skill.name = data.get("name", skill.name)
    skill.level = data.get("level", skill.level)
    skill.category = data.get("category", skill.category)

    db.session.commit()
    return jsonify(skill.to_dict())


@app.route("/api/skills/<int:skill_id>", methods=["DELETE"])
def api_delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({"message": "Habilidade excluída com sucesso"})


# ---------------------------------------------
# API REST - EXPERIÊNCIAS
# ---------------------------------------------
@app.route("/api/experiences", methods=["GET"])
def api_get_experiences():
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return jsonify([e.to_dict() for e in experiences])


@app.route("/api/experiences/<int:exp_id>", methods=["GET"])
def api_get_experience(exp_id):
    experience = Experience.query.get_or_404(exp_id)
    return jsonify(experience.to_dict())


@app.route("/api/experiences", methods=["POST"])
def api_create_experience():
    data = request.get_json()
    if not data or "role" not in data:
        abort(400, description="Campo obrigatório: role")

    experience = Experience(
        role=data["role"],
        company=data.get("company", ""),
        description=data.get("description", ""),
        start_date=data.get("start_date", ""),
        end_date=data.get("end_date", ""),
        location=data.get("location", ""),
        current=data.get("current", False),
    )
    db.session.add(experience)
    db.session.commit()
    return jsonify(experience.to_dict()), 201


@app.route("/api/experiences/<int:exp_id>", methods=["PUT"])
def api_update_experience(exp_id):
    experience = Experience.query.get_or_404(exp_id)
    data = request.get_json() or {}

    experience.role = data.get("role", experience.role)
    experience.company = data.get("company", experience.company)
    experience.description = data.get("description", experience.description)
    experience.start_date = data.get("start_date", experience.start_date)
    experience.end_date = data.get("end_date", experience.end_date)
    experience.location = data.get("location", experience.location)
    experience.current = data.get("current", experience.current)

    db.session.commit()
    return jsonify(experience.to_dict())


@app.route("/api/experiences/<int:exp_id>", methods=["DELETE"])
def api_delete_experience(exp_id):
    experience = Experience.query.get_or_404(exp_id)
    db.session.delete(experience)
    db.session.commit()
    return jsonify({"message": "Experiência excluída com sucesso"})


# ---------------------------------------------
# INICIALIZAÇÃO
# ---------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
