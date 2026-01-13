const API_BASE = '/api';

// DOM Elements
const skillsInput = document.getElementById('skills');
const interestsInput = document.getElementById('interests');
const experienceInput = document.getElementById('experience');
const educationInput = document.getElementById('education');
const resultsContainer = document.getElementById('results');
const careersContainer = document.getElementById('careers');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    getRecommendations();
    loadCareers();
});

// Get recommendations
async function getRecommendations() {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    resultsContainer.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                skills: skillsInput.value,
                interests: interestsInput.value,
                experience_years: parseInt(experienceInput.value),
                education_level: educationInput.value
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Error:', error);
        displayDemoResults();
    } finally {
        loading.style.display = 'none';
    }
}

// Display recommendations
function displayRecommendations(recommendations) {
    let html = '<h3>Your Top Matches:</h3>';
    
    recommendations.forEach(career => {
        html += `
            <div class="career-card">
                <div class="career-header">
                    <span class="career-category">${career.category}</span>
                    <h3>${career.title}</h3>
                    <div class="match-score">${career.match_score}% Match</div>
                </div>
                <div class="career-body">
                    <p>${career.description}</p>
                    <div class="career-stats">
                        <div><i class="fas fa-money-bill-wave"></i> ${career.average_salary}</div>
                        <div><i class="fas fa-chart-line"></i> ${career.growth_rate} growth</div>
                    </div>
                    <div class="skills">
                        <strong>Skills:</strong>
                        ${career.required_skills.map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// Load all careers
async function loadCareers() {
    try {
        const response = await fetch(`${API_BASE}/careers`);
        const data = await response.json();
        
        if (data.status === 'success') {
            displayAllCareers(data.careers);
        }
    } catch (error) {
        console.error('Error:', error);
        displayDemoCareers();
    }
}

// Display all careers
function displayAllCareers(careers) {
    let html = '';
    
    careers.forEach(career => {
        html += `
            <div class="career-card">
                <div class="career-header">
                    <span class="career-category">${career.category}</span>
                    <h3>${career.title}</h3>
                </div>
                <div class="career-body">
                    <p>${career.description}</p>
                    <div class="skills">
                        ${career.required_skills.slice(0, 3).map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    });
    
    careersContainer.innerHTML = html;
}

// Demo fallbacks
function displayDemoResults() {
    const demoData = [
        {
            title: "Data Scientist",
            category: "Technology",
            description: "Analyze data using machine learning",
            average_salary: "$120,000+",
            growth_rate: "22%",
            required_skills: ["python", "ml", "sql", "statistics"],
            match_score: 92.5
        },
        {
            title: "Web Developer",
            category: "Technology",
            description: "Build websites and applications",
            average_salary: "$85,000+",
            growth_rate: "13%",
            required_skills: ["javascript", "html", "css", "react"],
            match_score: 78.9
        }
    ];
    
    displayRecommendations(demoData);
}

function displayDemoCareers() {
    const demoCareers = [
        {
            title: "Data Scientist",
            category: "Technology",
            description: "Analyze complex data",
            required_skills: ["python", "ml", "sql"]
        },
        {
            title: "ML Engineer",
            category: "Technology",
            description: "Build ML systems",
            required_skills: ["python", "tensorflow", "aws"]
        },
        {
            title: "Frontend Dev",
            category: "Technology",
            description: "Build user interfaces",
            required_skills: ["javascript", "react", "css"]
        }
    ];
    
    displayAllCareers(demoCareers);
}