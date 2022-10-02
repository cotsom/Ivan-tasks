import os
import time

from flask import Flask, render_template, redirect, request, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
    filename = request.args.get('file')

    if filename is None:
        filename = "text.txt"
    filename = "files/" + filename
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, "r") as f:
            content = f.read()
            create = str(time.ctime(os.path.getmtime(filename)))
            filename = f.name.split('/')[-1]
        file = {
            "filename": f"Имя Файла: {filename}",
            "create": f"Дата создания: {create}",
            "file": content
        }
    else:
        file = {
            "filename": f'Файл "{ filename.split("/")[-1] }" не найден',
        }
    return render_template("index.html", file=file)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
