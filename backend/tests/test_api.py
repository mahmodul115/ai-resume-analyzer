from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_analyze_text():
    response = client.post('/analyze', json={
        'resume_text': 'Python React FastAPI Docker Git projects experience education email test@example.com',
        'job_description': 'Software engineer using Python React Docker'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'ats_score' in data
    assert 'Python' in data['skills_found']
