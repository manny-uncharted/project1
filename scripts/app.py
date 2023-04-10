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

    os.environ['OPENAI_API_KEY'] = openai_api_key
    os.environ['ELEVEN_LABS_API_KEY'] = eleven_labs_api_key

    process = subprocess.Popen(['python', 'scripts/main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate(input=b"default_name\n")

    # Open a new terminal window and run main.py
    subprocess.Popen(['xterm', '-e', 'python', 'scripts/main.py'])

    return jsonify({"result": "App is starting up.", "stdout": stdout.decode('utf-8'), "stderr": stderr.decode('utf-8')})

