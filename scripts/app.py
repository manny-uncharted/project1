from flask import Flask, request, jsonify, render_template
from multiprocessing import Process
import subprocess
import os
import time
import webbrowser
from ai_config import AIConfig
from main import main_file
import openai
from flask_socketio import SocketIO, emit
from terminal import launch_terminal

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
    command = f"python3 scripts/main.py {ai_name} {ai_role}"

    launch_terminal(command)

    return result
    
    # return jsonify({"result": "App is starting up."})

# @app.route('/userdata', methods=['GET', 'POST'])
# def user_data():

#     if request.method == 'GET':
#         return render_template('userdata.html')
#     ai_name = request.form.get('ai_name')
#     ai_role = request.form.get('ai_role')
#     goal1 = request.form.get('goal1')
#     goal2 = request.form.get('goal2')
#     goal3 = request.form.get('goal3')
#     goal4 = request.form.get('goal4')
#     goal5 = request.form.get('goal5')

#     ai_goals = [goal1, goal2, goal3, goal4, goal5]

#     result = main_file(ai_name, ai_role, ai_goals)
    
#     return result



# @app.route('/run', methods=['GET', 'POST'])
# def run_app():
#     if request.method == 'GET':
#         return render_template('form.html')

#     openai_api_key = request.form.get('openai_api_key')
#     eleven_labs_api_key = request.form.get('eleven_labs_api_key')

#     if not openai_api_key or not eleven_labs_api_key:
#         return jsonify({"error": "API keys are required."}), 400

#     env = {'OPENAI_API_KEY': openai_api_key, 'ELEVEN_LABS_API_KEY': eleven_labs_api_key}
    
#     return jsonify({"result": "App is starting up."})

# @app.route('/open_terminal', methods=['GET', 'POST'])
# def open_terminal():
#     # Get user input from the form data
#     user_input = request.form.get('user_input')
#     if user_input is None:
#         return jsonify({"error": "user_input is required."}), 400


#     # Build the command to run in the terminal
#     command = 'echo {}'.format(user_input)

#     # Open a new terminal window and run the command
#     subprocess.Popen(['gnome-terminal', '-e', command])

#     # Return a response to the user
#     return 'Command executed in terminal: {}'.format(command)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)





