from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes.api import api_bp

# Initialize Flask app
app = Flask(__name__, static_folder=None)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def serve_frontend():
    """Serve frontend index.html"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_frontend_files(path):
    """Serve frontend static files"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, path)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 CAREER PATH RECOMMENDER API STARTING...")
    print("=" * 60)
    print("\n📊 Backend Features:")
    print("   ✅ ML-based recommendation engine")
    print("   ✅ Skill gap analysis")
    print("   ✅ REST API endpoints")
    print("   ✅ Career database with 8+ roles")
    print("\n🌐 API Endpoints:")
    print("   • GET  /api/health          - Health check")
    print("   • GET  /api/careers         - Get all careers")
    print("   • GET  /api/career/<id>     - Get career details")
    print("   • POST /api/recommend       - Get recommendations")
    print("   • POST /api/skill-gap       - Analyze skill gaps")
    print("\n🔗 Frontend URL: http://localhost:5000")
    print("📁 Backend URL:  http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, port=5000)