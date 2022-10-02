from flask import Flask, render_template, request
import requests

app = Flask(__name__)
allow_addsresses = ("https://ipinfo.io/ip", "https://ifconfig.me/ip", "https://api.ipify.org")

@app.route('/', methods=["GET", "POST"])
def index():
    result = dict()
    if request.method == "POST":
        address = request.form.get('address', '')

        if address != '':
            if address not in allow_addsresses:
                return "flag{s3rv3r_s1d3_r3qu3st_f0rd3n@ry}"
            r = requests.get(address)
            result['ip'] = r.content.decode()
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
