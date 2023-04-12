from flask import Flask, request, jsonify, render_template
from multiprocessing import Process
import os
import time
import webbrowser
from ai_config import AIConfig
from main import main_file
import openai
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def launch_terminal(command):
    subprocess.call(['gnome-terminal', '--', 'bash', '-c', command])

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

    openai.api_key = env['OPENAI_API_KEY']
    # openai.eleven_labs_api_key = env['ELEVEN_LABS_API_KEY']

    ai_name = request.form.get('ai_name')
    ai_role = request.form.get('ai_role')
    goal1 = request.form.get('goal1')
    goal2 = request.form.get('goal2')
    goal3 = request.form.get('goal3')
    goal4 = request.form.get('goal4')
    goal5 = request.form.get('goal5')

    ai_goals = [goal1, goal2, goal3, goal4, goal5]

    result = main_file(ai_name, ai_role, ai_goals)

    # Launch terminal and run command
    launch_terminal('python3 scripts/main.py')

    return result

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)






