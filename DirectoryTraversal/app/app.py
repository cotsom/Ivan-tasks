import os
from flask import Flask, request, abort, jsonify, url_for, render_template, redirect, send_from_directory

DIRECTORY = "./material"

app = Flask(__name__, static_folder='assets')


@app.route("/files/")
def list_dirs():
    files = []
    directory = request.args.get("dir")
    filename = request.args.get("filename")
    if directory is None and filename is None:
        vuln_dir = DIRECTORY
        for filename in os.listdir(vuln_dir):
            path = os.path.join(vuln_dir, filename)
            files.append(filename)
        return render_template("lib.html", files=files)
    elif directory is not None and filename is None:
        vuln_dir = DIRECTORY + "/" + directory
        for filename in os.listdir(vuln_dir):
            files.append(filename)
        return render_template("files.html", files=files, dir=directory)
    elif directory is not None and filename is not None:

        return "<a href='/download?dir=%s&filename=%s'>download</a> %s" % (directory, filename, filename)
    return redirect(url_for("index"), 302)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download")
def download():
    directory = request.args.get("dir")
    filename = request.args.get("filename")
    vuln_dir = DIRECTORY + "/" + directory
    return send_from_directory(directory=vuln_dir, filename=filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
