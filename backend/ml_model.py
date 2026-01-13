import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import json
from typing import List, Dict, Any

class CareerRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.career_data = self.load_career_data()
        self.fit_model()
    
    def load_career_data(self) -> List[Dict]:
        """Load career data from database"""
        return [
            {
                "id": 1,
                "title": "Data Scientist",
                "category": "Technology",
                "description": "Analyze complex data to help organizations make better decisions using statistical models and machine learning algorithms.",
                "required_skills": ["python", "machine learning", "sql", "statistics", "data analysis", "pandas", "numpy"],
                "recommended_skills": ["deep learning", "cloud computing", "big data", "docker", "kubernetes"],
                "average_salary": "$120,000 - $160,000",
                "growth_rate": "22% (Much faster than average)",
                "experience_needed": "3-5 years",
                "education": "Master's in Computer Science/Statistics/Mathematics",
                "companies": ["Google", "Microsoft", "Amazon", "Facebook", "Netflix"],
                "learning_path": ["Python Basics", "Statistics", "ML Algorithms", "Deep Learning", "MLOps"],
                "job_market": "High demand with 31% projected growth",
                "match_score": 0
            },
            {
                "id": 2,
                "title": "Machine Learning Engineer",
                "category": "Technology",
                "description": "Design, build, and deploy machine learning models and systems for production environments.",
                "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "docker", "aws"],
                "recommended_skills": ["kubernetes", "mlops", "ci/cd", "apache spark", "hadoop"],
                "average_salary": "$140,000 - $180,000",
                "growth_rate": "28% (Much faster than average)",
                "experience_needed": "4-6 years",
                "education": "Bachelor's/Master's in Computer Science/AI",
                "companies": ["Tesla", "OpenAI", "NVIDIA", "Uber", "Airbnb"],
                "learning_path": ["ML Fundamentals", "Deep Learning", "Cloud Platforms", "MLOps", "System Design"],
                "job_market": "Very high demand with AI boom",
                "match_score": 0
            },
            {
                "id": 3,
                "title": "Frontend Developer",
                "category": "Technology",
                "description": "Build responsive and interactive user interfaces for web applications using modern frameworks.",
                "required_skills": ["javascript", "react", "html", "css", "typescript", "redux"],
                "recommended_skills": ["next.js", "graphql", "webpack", "jest", "cypress"],
                "average_salary": "$85,000 - $130,000",
                "growth_rate": "13% (Faster than average)",
                "experience_needed": "2-4 years",
                "education": "Bachelor's in Computer Science or related field",
                "companies": ["Meta", "Spotify", "Shopify", "Stripe", "Twitter"],
                "learning_path": ["HTML/CSS", "JavaScript", "React", "State Management", "Testing"],
                "job_market": "Steady demand with good opportunities",
                "match_score": 0
            },
            {
                "id": 4,
                "title": "Backend Developer",
                "category": "Technology",
                "description": "Develop server-side logic, databases, and APIs to support web and mobile applications.",
                "required_skills": ["python", "java", "node.js", "sql", "mongodb", "docker", "aws"],
                "recommended_skills": ["microservices", "kafka", "redis", "kubernetes", "graphql"],
                "average_salary": "$95,000 - $140,000",
                "growth_rate": "15% (Faster than average)",
                "experience_needed": "3-5 years",
                "education": "Bachelor's in Computer Science",
                "companies": ["Amazon", "Google", "Microsoft", "PayPal", "LinkedIn"],
                "learning_path": ["Backend Fundamentals", "Databases", "APIs", "Cloud Services", "DevOps"],
                "job_market": "High demand across all industries",
                "match_score": 0
            },
            {
                "id": 5,
                "title": "DevOps Engineer",
                "category": "Technology",
                "description": "Bridge development and operations teams to automate and streamline software deployment.",
                "required_skills": ["docker", "kubernetes", "aws", "ci/cd", "linux", "python", "bash"],
                "recommended_skills": ["terraform", "ansible", "prometheus", "grafana", "jenkins"],
                "average_salary": "$110,000 - $150,000",
                "growth_rate": "21% (Much faster than average)",
                "experience_needed": "3-5 years",
                "education": "Bachelor's in Computer Science/IT",
                "companies": ["Netflix", "Uber", "Airbnb", "Slack", "Atlassian"],
                "learning_path": ["Linux Basics", "Containerization", "Cloud Platforms", "CI/CD", "Monitoring"],
                "job_market": "Very high demand with cloud adoption",
                "match_score": 0
            },
            {
                "id": 6,
                "title": "Data Analyst",
                "category": "Business & Analytics",
                "description": "Interpret data and turn it into information for business decision-making through reports and visualizations.",
                "required_skills": ["sql", "excel", "python", "tableau", "power bi", "statistics"],
                "recommended_skills": ["r", "snowflake", "looker", "google analytics", "airflow"],
                "average_salary": "$70,000 - $110,000",
                "growth_rate": "18% (Much faster than average)",
                "experience_needed": "1-3 years",
                "education": "Bachelor's in Business/Statistics/Computer Science",
                "companies": ["Amazon", "IBM", "Accenture", "Deloitte", "McKinsey"],
                "learning_path": ["SQL", "Data Visualization", "Statistics", "Python", "Business Intelligence"],
                "job_market": "High demand across all sectors",
                "match_score": 0
            },
            {
                "id": 7,
                "title": "Cybersecurity Analyst",
                "category": "Security",
                "description": "Protect computer systems and networks from cyber threats and security breaches.",
                "required_skills": ["network security", "linux", "python", "siem", "firewalls", "encryption"],
                "recommended_skills": ["ethical hacking", "cloud security", "compliance", "threat intelligence", "soc"],
                "average_salary": "$90,000 - $130,000",
                "growth_rate": "33% (Much faster than average)",
                "experience_needed": "2-4 years",
                "education": "Bachelor's in Cybersecurity/Computer Science",
                "companies": ["CrowdStrike", "Palo Alto Networks", "Cisco", "IBM Security", "McAfee"],
                "learning_path": ["Networking", "Security Fundamentals", "Tools & Technologies", "Threat Analysis", "Compliance"],
                "job_market": "Extremely high demand with increasing threats",
                "match_score": 0
            },
            {
                "id": 8,
                "title": "Cloud Architect",
                "category": "Cloud & Infrastructure",
                "description": "Design and implement cloud computing strategies and solutions for organizations.",
                "required_skills": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "python"],
                "recommended_skills": ["serverless", "microservices", "devsecops", "cost optimization", "multi-cloud"],
                "average_salary": "$130,000 - $190,000",
                "growth_rate": "25% (Much faster than average)",
                "experience_needed": "5-8 years",
                "education": "Bachelor's/Master's in Computer Science",
                "companies": ["Amazon Web Services", "Microsoft Azure", "Google Cloud", "Oracle", "VMware"],
                "learning_path": ["Cloud Fundamentals", "Infrastructure as Code", "Networking", "Security", "Architecture Patterns"],
                "job_market": "Very high demand with cloud migration",
                "match_score": 0
            }
        ]
    
    def fit_model(self):
        """Train the recommendation model"""
        all_texts = []
        for career in self.career_data:
            text = " ".join(career["required_skills"]) + " " + career["description"] + " " + career["category"]
            all_texts.append(text)
        
        self.tfidf_matrix = self.vectorizer.fit_transform(all_texts)
    
    def recommend_careers(self, user_skills: str, user_interests: str, experience_years: int = 2, education_level: str = "Bachelor's") -> List[Dict]:
        """Recommend careers based on user profile"""
        user_text = user_skills.lower() + " " + user_interests.lower()
        
        # Transform user input
        user_vector = self.vectorizer.transform([user_text])
        
        # Calculate similarity
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Adjust scores based on experience and education
        for i, career in enumerate(self.career_data):
            base_score = similarities[i] * 100
            
            # Experience adjustment
            exp_needed = career["experience_needed"]
            min_exp = int(exp_needed.split("-")[0].split()[0])
            exp_adjustment = min(experience_years / min_exp, 1.5) * 20
            
            # Education adjustment
            education_match = 1.0 if education_level in career["education"] else 0.8
            
            # Final score
            career["match_score"] = round(base_score * education_match + exp_adjustment, 2)
            career["match_score"] = min(career["match_score"], 99.9)  # Cap at 99.9
        
        # Sort by match score
        sorted_careers = sorted(self.career_data, key=lambda x: x["match_score"], reverse=True)
        
        return sorted_careers[:5]
    
    def get_skill_gap_analysis(self, user_skills: List[str], target_career_id: int) -> Dict:
        """Analyze skill gaps for a target career"""
        target_career = next((c for c in self.career_data if c["id"] == target_career_id), None)
        
        if not target_career:
            return {"error": "Career not found"}
        
        user_skill_set = set([skill.lower().strip() for skill in user_skills])
        required_skills = set([skill.lower() for skill in target_career["required_skills"]])
        recommended_skills = set([skill.lower() for skill in target_career["recommended_skills"]])
        
        missing_required = list(required_skills - user_skill_set)
        missing_recommended = list(recommended_skills - user_skill_set)
        existing_skills = list(user_skill_set & (required_skills | recommended_skills))
        
        match_percentage = len(user_skill_set & required_skills) / len(required_skills) * 100
        
        return {
            "target_career": target_career["title"],
            "match_percentage": round(match_percentage, 1),
            "existing_skills": existing_skills,
            "missing_required": missing_required,
            "missing_recommended": missing_recommended,
            "learning_path": target_career["learning_path"],
            "time_to_proficiency": self.calculate_time_to_proficiency(len(missing_required), len(missing_recommended))
        }
    
    def calculate_time_to_proficiency(self, missing_req: int, missing_rec: int) -> str:
        """Estimate time needed to learn missing skills"""
        total_missing = missing_req + missing_rec
        if total_missing <= 2:
            return "1-3 months"
        elif total_missing <= 5:
            return "3-6 months"
        elif total_missing <= 8:
            return "6-12 months"
        else:
            return "1-2 years"
    
    def save_model(self, filepath: str = "career_recommender.joblib"):
        """Save trained model to file"""
        joblib.dump(self, filepath)
    
    @staticmethod
    def load_model(filepath: str = "career_recommender.joblib"):
        """Load model from file"""
        return joblib.load(filepath)