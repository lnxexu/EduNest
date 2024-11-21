import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profilepage():
    return render_template('profile.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/register')
def registerpage():
    return render_template('register.html')

@app.route('/quiz')
def quizpage():
    return render_template('quiz.html')

@app.route('/get_questions')
def get_questions():
    category = request.args.get('category', 'geography')
    file_map = {
        'geography': 'geoQ.json',
        'mathematics': 'mathQ.json',
        'reading': 'readingQ.json',
        'science': 'scienceQ.json'
    }
    
    file_name = file_map.get(category, 'geoQ.json')
    
    with open(file_name, 'r') as file:
        questions = json.load(file)
    
    return jsonify(questions)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    user_answers = request.json['answers']
    category = request.json['category']
    
    file_map = {
        'geography': 'geoQ.json',
        'mathematics': 'mathQ.json',
        'reading': 'readingQ.json',
        'science': 'scienceQ.json'
    }
    
    file_name = file_map.get(category, 'geoQ.json')
    
    with open(file_name, 'r') as file:
        questions = json.load(file)
    
    results = []
    for i, question in enumerate(questions):
        result = {
            'question': question['question'],
            'correct_answer': question['answer'],
            'user_answer': user_answers[i] if i < len(user_answers) else None,
            'is_correct': user_answers[i] == question['answer'] if i < len(user_answers) else False
        }
        results.append(result)
    
    return render_template('results.html', results=results)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    # Check if the user exists in the database
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return jsonify({'message': 'User not found'}), 404
    
    for user in users:
        if user['email'] == email and user['password'] == password:
            return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'User not found'}), 404


@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    name = data['name']
    age = data['age']
    level = data['level']
    
    # Here you can add code to save the updated data to a database or a file
    # For demonstration, we'll save it to a JSON file
    profile_data = {
        'name': name,
        'age': age,
        'level': level
    }
    
    with open('profile.json', 'w') as file:
        json.dump(profile_data, file, indent=4)
    
    return jsonify({'message': 'Profile updated successfully'})


@app.route('/get_profile', methods=['GET'])
def get_profile():
    try:
        with open('profile.json', 'r') as file:
            profile = json.load(file)
    except FileNotFoundError:
        profile = {}

    return jsonify(profile)




@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data['role']
    name = data['name']
    email = data['email']
    password = data['password']
    new_password = data['new-password']
    
    user_data = {
        'role': role,
        'name': name,
        'email': email,
        'password': password,
        'new_password': new_password
    }
    
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    
    users.append(user_data)
    
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)
    
    return f"Registered {role} with name {name}, email {email}"

if __name__ == '__main__':
    app.run(debug=True)