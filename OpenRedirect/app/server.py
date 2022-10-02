from flask import Flask, render_template, redirect, request
import socket
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog():
    url = request.args.get("url", None)
    if url is not None:
        return redirect(url, code=302)
    return render_template("catalog.html", server_ip="80.249.131.31:8081")


@app.route("/pay/<productid>")
def pay(productid):
    return render_template("pay.html")


@app.route("/admin/support", methods=["GET", "POST"])
def admin_support():
    if request.method == "POST":
        report = request.form.get("report")
        if report:
            try:
                redirect_url = report[report.index('url', 25) + 4:]
                r = requests.get(redirect_url)
            except:
                return render_template("admin_support.html")
            if r.status_code == 200:
                return "flag{Subm1t_0p3n_r3d1r3ct}"

    return render_template("admin_support.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
