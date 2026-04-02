from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.faculty_routes import faculty_bp
from routes.courses_routes import courses_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(student_bp)
app.register_blueprint(faculty_bp, url_prefix='/api')
app.register_blueprint(courses_bp)

@app.route('/')
def home():
    return jsonify({
        "message": "Student Management API",
        "version": "1.0.0",
        "endpoints": {
            "students": {
                "create": "POST /student/create",
                "get_all": "GET /student/",
                "get_by_id": "GET /student/<student_id>",
                "delete": "DELETE /student/<student_id>"
            },
            "faculty": {
                "create": "POST /api/faculty/create",
                "get_all": "GET /api/faculty/",
                "get_by_id": "GET /api/faculty/<faculty_id>",
                "delete": "DELETE /api/faculty/<faculty_id>"
            },
            "courses": {
                "create": "POST /courses/create",
                "get_all": "GET /courses/",
                "get_by_code": "GET /courses/<course_code>",
                "delete": "DELETE /courses/<course_code>"
            }
        }
        
    })

@app.route('/debug/routes')
def debug_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({'routes': routes})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)