from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))


@app.route('/')
def hello_world():
    return 'Welcome to the dark side!'

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

    result = subprocess.run(['python', 'scripts/main.py', '--speak'], capture_output=True, text=True)

    return jsonify({"result": result.stdout})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
