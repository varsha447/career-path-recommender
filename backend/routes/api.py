from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model import CareerRecommender

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize recommender
recommender = CareerRecommender()

@api_bp.route('/recommend', methods=['POST'])
def recommend_careers():
    """Get career recommendations based on user profile"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('skills'):
            return jsonify({'error': 'Skills are required'}), 400
        
        recommendations = recommender.recommend_careers(
            user_skills=data.get('skills', ''),
            user_interests=data.get('interests', ''),
            experience_years=int(data.get('experience_years', 2)),
            education_level=data.get('education_level', "Bachelor's")
        )
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/skill-gap', methods=['POST'])
def analyze_skill_gap():
    """Analyze skill gaps for a specific career"""
    try:
        data = request.json
        
        if not data.get('skills') or not data.get('target_career_id'):
            return jsonify({'error': 'Skills and target career ID are required'}), 400
        
        skills = [s.strip() for s in data['skills'].split(',')]
        
        analysis = recommender.get_skill_gap_analysis(
            user_skills=skills,
            target_career_id=int(data['target_career_id'])
        )
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/careers', methods=['GET'])
def get_all_careers():
    """Get all available careers"""
    try:
        careers = recommender.career_data
        simplified_careers = [
            {
                'id': c['id'],
                'title': c['title'],
                'category': c['category'],
                'description': c['description'][:100] + '...' if len(c['description']) > 100 else c['description']
            }
            for c in careers
        ]
        
        return jsonify({
            'status': 'success',
            'careers': simplified_careers
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/career/<int:career_id>', methods=['GET'])
def get_career_detail(career_id):
    """Get detailed information about a specific career"""
    try:
        career = next((c for c in recommender.career_data if c['id'] == career_id), None)
        
        if not career:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({
            'status': 'success',
            'career': career
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Career Recommender API is running',
        'total_careers': len(recommender.career_data)
    })