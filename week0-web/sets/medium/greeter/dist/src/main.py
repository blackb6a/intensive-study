from flask import Flask, request, current_app
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from selenium import webdriver
import os
import time

H_SITEKEY = os.getenv(
    "H_SITEKEY", '"><script>document.write("hCaptcha is broken")</script>'
)
H_SECRET = os.getenv("H_SECRET", "???")
app = Flask(__name__, static_url_path="")

chal = {
    "title": "Greeter",
    "init_url": os.getenv("INIT_URL", "http://localhost:3000/"),
    "flag": os.getenv("FLAG", "fakeflag{zzz}"),
    "sleep": 1,
}

def visit(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(chal["init_url"])
        driver.add_cookie({"name": "flag", "value": chal["flag"]})
        driver.get("about:blank")
        driver.get(url)
        time.sleep(chal["sleep"])
        return "Your URL has been visited by the " + chal["title"] + " bot."
    except Exception as e:
        print(url, flush=True)
        print(e, flush=True)
        return "The " + chal["title"] + " bot did not handle your URL properly."
    finally:
        driver.quit()

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST" and request.remote_addr != "127.0.0.1":
        if "url" not in request.form or request.form.get("url") == "":
            return "Please enter a URL"
        if (
            "h-captcha-response" not in request.form
            or request.form["h-captcha-response"] == ""
        ):
            return "Bad hCaptcha"
        data = urlencode(
            {"secret": H_SECRET, "response": request.form["h-captcha-response"]}
        ).encode("ascii")
        try:
            fetch = (
                urlopen("https://hcaptcha.com/siteverify", data).read().decode("utf-8")
            )
            if '"success":true' not in fetch:
                return "hCaptcha is broken"
            return visit(request.form.get("url"))
        except Exception as e:
            return str(e)
    else: 
        out = """<html>
    <head>
        <title>XSS Bot - %s</title>
        <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
    </head>
    <body>
        <h1>XSS Bot - %s</h1>
        <form method="POST">
        <table>
        <tr>
            <td>URL</td>
            <td>
            <input name="url" size="70" />
            </td>
        </tr>
        </table>
        <div class="h-captcha" data-sitekey="%s"></div>
        <input type="submit" />
        </form>
    </body>
    </html>""" % (
            chal["title"],
            chal["title"],
            H_SITEKEY,
        )

        return out


@app.route("/")
def index():
    return current_app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)