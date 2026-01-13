from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Sample career data
CAREER_DATA = [
    {
        "id": 1,
        "title": "Data Scientist",
        "category": "Technology",
        "description": "Analyze complex data using machine learning and statistics to help organizations make better decisions.",
        "required_skills": ["python", "machine learning", "sql", "statistics", "data analysis"],
        "average_salary": "$120,000 - $160,000",
        "growth_rate": "22%",
        "experience_needed": "3-5 years",
        "education": "Master's in Computer Science/Statistics",
        "match_score": 0
    },
    {
        "id": 2,
        "title": "Machine Learning Engineer",
        "category": "Technology",
        "description": "Design, build, and deploy machine learning models for production systems.",
        "required_skills": ["python", "deep learning", "tensorflow", "aws", "docker"],
        "average_salary": "$140,000 - $180,000",
        "growth_rate": "28%",
        "experience_needed": "4-6 years",
        "education": "Bachelor's/Master's in Computer Science",
        "match_score": 0
    },
    {
        "id": 3,
        "title": "Frontend Developer",
        "category": "Technology",
        "description": "Build responsive and interactive user interfaces for web applications.",
        "required_skills": ["javascript", "react", "css", "html", "typescript"],
        "average_salary": "$85,000 - $130,000",
        "growth_rate": "13%",
        "experience_needed": "2-4 years",
        "education": "Bachelor's in Computer Science",
        "match_score": 0
    },
    {
        "id": 4,
        "title": "Backend Developer",
        "category": "Technology",
        "description": "Develop server-side logic, databases, and APIs for web applications.",
        "required_skills": ["python", "java", "node.js", "sql", "mongodb"],
        "average_salary": "$95,000 - $140,000",
        "growth_rate": "15%",
        "experience_needed": "3-5 years",
        "education": "Bachelor's in Computer Science",
        "match_score": 0
    },
    {
        "id": 5,
        "title": "DevOps Engineer",
        "category": "Technology",
        "description": "Automate and streamline software deployment and infrastructure management.",
        "required_skills": ["docker", "kubernetes", "aws", "linux", "python"],
        "average_salary": "$110,000 - $150,000",
        "growth_rate": "21%",
        "experience_needed": "3-5 years",
        "education": "Bachelor's in Computer Science",
        "match_score": 0
    }
]

def calculate_match_score(user_skills, career, experience_years):
    """Simple match score calculation"""
    user_skills_set = set([s.lower().strip() for s in user_skills.split(',')])
    career_skills_set = set([s.lower() for s in career["required_skills"]])
    
    # Calculate skill match
    common_skills = len(user_skills_set.intersection(career_skills_set))
    skill_match = (common_skills / len(career_skills_set)) * 70
    
    # Experience adjustment
    exp_needed = int(career["experience_needed"].split('-')[0].split()[0])
    exp_adjustment = min(experience_years / exp_needed, 1.5) * 30
    
    return min(skill_match + exp_adjustment, 99.9)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Career API Running'})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    user_skills = data.get('skills', '')
    user_interests = data.get('interests', '')
    experience_years = int(data.get('experience_years', 2))
    
    # Calculate scores for all careers
    for career in CAREER_DATA:
        career["match_score"] = round(calculate_match_score(user_skills, career, experience_years), 1)
    
    # Sort by match score
    sorted_careers = sorted(CAREER_DATA, key=lambda x: x["match_score"], reverse=True)
    
    return jsonify({
        'status': 'success',
        'recommendations': sorted_careers[:3]
    })

@app.route('/api/careers', methods=['GET'])
def get_careers():
    return jsonify({
        'status': 'success',
        'careers': CAREER_DATA
    })

# Serve frontend
@app.route('/')
def serve_index():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, path)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 CAREER PATH RECOMMENDER")
    print("=" * 60)
    print("\n✅ Backend running on http://localhost:5000")
    print("📊 Features:")
    print("   • 5 career paths")
    print("   • Skill-based matching")
    print("   • REST API")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
    application = app
