from flask import session


def test_app_factory_creates_app(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_default_test_user_can_login(client):
    response = client.post('/auth/login/', data={
        'username': 'test',
        'password': '12345678',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data


def test_dashboard_requires_authentication(client):
    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/auth/login/?next=%2Fdashboard%2F')

    root_response = client.get('/', follow_redirects=False)
    assert root_response.status_code == 302
    assert root_response.headers['Location'].endswith('/auth/login/')


def test_user_registration_and_dashboard(client):
    response = client.post('/auth/register/', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'Dashboard' in response.data


def test_create_seminar_and_list(client):
    client.post('/auth/register/', data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)

    response = client.post('/seminar/create/', data={
        'date': '2026-05-15',
        'topic': 'Introduction to Machine Learning',
        'speaker': 'Dr. Sarah Chen',
        'hours': '3.0',
        'organizer': 'Data Science Institute',
        'notes': 'Covered supervised learning basics',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Introduction to Machine Learning' in response.data


def test_create_seminar_redirects_to_dashboard(client):
    client.post('/auth/register/', data={
        'username': 'dave',
        'email': 'dave@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)

    response = client.post('/seminar/create/', headers={'HX-Request': 'true'}, data={
        'date': '2026-05-15',
        'topic': 'Leadership Seminar',
        'speaker': 'Ms. Rivera',
        'hours': '4.0',
        'organizer': 'People Team',
        'notes': 'Great session',
    })
    assert response.status_code == 200
    assert response.headers.get('HX-Redirect') == '/dashboard/'


def test_edit_and_delete_seminar_via_dashboard(client):
    client.post('/auth/register/', data={
        'username': 'erin',
        'email': 'erin@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)

    create_response = client.post('/seminar/create/', data={
        'date': '2026-05-15',
        'topic': 'Original Topic',
        'speaker': 'Dr. Original',
        'hours': '2.0',
        'organizer': 'Org A',
        'notes': 'Original notes',
    }, follow_redirects=True)
    assert create_response.status_code == 200

    seminar = client.get('/dashboard/').data.decode()
    assert 'Original Topic' in seminar

    edit_response = client.get('/seminar/1/edit/')
    assert edit_response.status_code == 200
    assert b'Update Seminar' in edit_response.data

    update_response = client.post('/seminar/1/edit/', headers={'HX-Request': 'true'}, data={
        'date': '2026-05-16',
        'topic': 'Updated Topic',
        'speaker': 'Dr. Updated',
        'hours': '3.5',
        'organizer': 'Org B',
        'notes': 'Updated notes',
    })
    assert update_response.status_code == 200
    assert update_response.headers.get('HX-Redirect') == '/dashboard/'

    delete_response = client.delete('/seminar/1/delete/', headers={'HX-Request': 'true'})
    assert delete_response.status_code == 200
    assert delete_response.headers.get('HX-Redirect') == '/dashboard/'


def test_dashboard_search_and_sort(client):
    client.post('/auth/register/', data={
        'username': 'frank',
        'email': 'frank@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)

    client.post('/seminar/create/', data={
        'date': '2026-05-15',
        'topic': 'Alpha Talk',
        'speaker': 'Jane Doe',
        'hours': '2.0',
        'organizer': 'North Team',
        'notes': 'First note',
    }, follow_redirects=True)
    client.post('/seminar/create/', data={
        'date': '2026-05-17',
        'topic': 'Beta Seminar',
        'speaker': 'John Smith',
        'hours': '5.0',
        'organizer': 'South Team',
        'notes': 'Second note',
    }, follow_redirects=True)

    response = client.get('/dashboard/?q=beta&sort_by=topic&direction=asc')
    assert response.status_code == 200
    assert b'Beta Seminar' in response.data
    assert b'Alpha Talk' not in response.data

    sorted_response = client.get('/dashboard/?sort_by=hours&direction=desc')
    assert sorted_response.status_code == 200
    html = sorted_response.data.decode()
    assert html.index('Beta Seminar') < html.index('Alpha Talk')


def test_dashboard_inline_edit(client):
    client.post('/auth/register/', data={
        'username': 'gina',
        'email': 'gina@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)

    client.post('/seminar/create/', data={
        'date': '2026-05-15',
        'topic': 'Inline Edit Topic',
        'speaker': 'Dr. Original',
        'hours': '2.0',
        'organizer': 'Org A',
        'notes': 'Original notes',
    }, follow_redirects=True)

    edit_page = client.get('/seminar/1/inline_edit/')
    assert edit_page.status_code == 200
    assert b'Inline Edit Topic' in edit_page.data

    update_response = client.post('/seminar/1/inline_edit/', data={
        'date': '2026-05-16',
        'topic': 'Updated Inline Topic',
        'speaker': 'Dr. Updated',
        'hours': '3.5',
        'organizer': 'Org B',
        'notes': 'Updated notes',
    })
    assert update_response.status_code == 200
    assert b'Updated Inline Topic' in update_response.data


def test_export_excel_download(client):
    client.post('/auth/register/', data={
        'username': 'carol',
        'email': 'carol@example.com',
        'password': 'secretpass',
        'confirm_password': 'secretpass',
    }, follow_redirects=True)
    client.post('/seminar/create/', data={
        'date': '2026-05-15',
        'topic': 'Data Ethics',
        'speaker': 'Dr. Marr',
        'hours': '2.0',
        'organizer': 'Research Center',
        'notes': 'Notes',
    }, follow_redirects=True)

    response = client.get('/seminar/export')
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    assert 'attachment; filename=' in response.headers['Content-Disposition']
