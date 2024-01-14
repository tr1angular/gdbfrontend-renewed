import os
from flask import Flask, render_template, request, jsonify
from main import GdbControllerInterface


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.form.get('command')
    filename = request.form.get('filename')
    gdbi = GdbControllerInterface(filename)
    response = gdbi.write(command)
    return jsonify(response)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        gdbi = GdbControllerInterface(filename)
        return render_template('index.html', loaded_code=gdbi.get_source_code())


if __name__ == '__main__':
    app.run()
