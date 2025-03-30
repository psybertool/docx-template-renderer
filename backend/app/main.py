from flask import Flask, request, send_file, jsonify
from processor import process_template, extract_variables
import os
import uuid
import tempfile
import json

app = Flask(__name__)

@app.route("/render", methods=["POST"])
def render_docx():
    if "template" not in request.files:
        return jsonify({"error": "No template file provided"}), 400

    template_file = request.files["template"]

    if "variables" not in request.form:
        return jsonify({"error": "No variables provided"}), 400

    try:
        variables = json.loads(request.form["variables"])
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON for variables"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = os.path.join(tmpdir, f"template_{uuid.uuid4()}.docx")
        output_path = os.path.join(tmpdir, f"output_{uuid.uuid4()}.docx")

        template_file.save(template_path)
        process_template(template_path, variables, output_path)

        return send_file(output_path, as_attachment=True, download_name="rendered.docx")

@app.route("/extract", methods=["POST"])
def extract_docx_variables():
    if "template" not in request.files:
        return jsonify({"error": "No template file provided"}), 400

    template_file = request.files["template"]

    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = os.path.join(tmpdir, f"template_{uuid.uuid4()}.docx")
        template_file.save(template_path)
        variables = extract_variables(template_path)
        return jsonify(variables)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
