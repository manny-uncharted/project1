from flask import Flask, request, jsonify, render_template
from multiprocessing import Process
import subprocess
import os
import time
import webbrowser
from flask_socketio import SocketIO, emit

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

    try:
        subprocess.Popen(['python', './scripts/main.py'], env=env)
        print('Subprocess started.')
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 500

    webbrowser.open_new_tab('http://localhost:5000/main')

    return jsonify({"result": "App is starting up."})

@app.route('/main')
def main():
    return render_template('js.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)




