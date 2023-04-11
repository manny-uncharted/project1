from flask import Flask, request, jsonify, render_template

import subprocess
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))

@app.route('/')
def hello_world():
    return 'Welcome to the Afterflea!'

@app.route('/run', methods=['GET', 'POST'])
def run_app():
    if request.method == 'GET':
        return render_template('form.html')

    openai_api_key = request.form.get('openai_api_key')
    eleven_labs_api_key = request.form.get('eleven_labs_api_key')

    if not openai_api_key or not eleven_labs_api_key:
        return jsonify({"error": "API keys are required."}), 400

    env = {'OPENAI_API_KEY': openai_api_key, 'ELEVEN_LABS_API_KEY': eleven_labs_api_key}

    try:
        subprocess.Popen(['python', 'scripts/main.py'], env=env)
    except FileNotFoundError:
        # Fallback to gnome-terminal
        subprocess.Popen(['gnome-terminal', '--', 'python', 'scripts/main.py'])

    return jsonify({"result": "App is starting up."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
