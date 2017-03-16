import os, os.path
from flask import Flask
from flask import request, render_template, make_response
import subprocess


def config_check():
    config_file = os.environ.get("HTTPCLIP_SETTINGS")
    if not config_file:
        return
    if not os.path.isfile(config_file):
        with open(config_file, mode="w", encoding="utf-8") as conf_file:
            conf_file.write("")

config_check()


def copy_text(text):
    p = subprocess.Popen(["xsel", "-b", "-i"], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode("utf-8"))

def paste_text():
    p = subprocess.Popen(["xsel", "-b", "-o"], stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode("utf-8")


app = Flask("httpclip")
if os.environ.get("HTTPCLIP_SETTINGS"):
    app.config.from_envvar("HTTPCLIP_SETTINGS")
if app.config.get("HTTPCLIP_LOGFILE", None):
    from logging import WatchedFileHandler
    app.logger.addHandler(WatchedFileHandler(app.config.get("HTTPCLIP_LOGFILE"), encoding="utf-8"))
verbose_logging = app.config.get("HTTPCLIP_VERBOSELOGGING", False):

@app.route("/", methods=["GET"])
def index():
    response = make_response(render_template("index.html"), 200)
    response.headers["Content-type"] = "text/html"
    return response

@app.route("/clipboard/get", methods=["GET"])
def clipboard_get():
    text = paste_text()
    if verbose_logging:
        app.logger.debug("Text in clipboard", {"text": text})
    response = make_response(text, 200)
    response.headers["Content-type"] = "text/plain"
    return response

@app.route("/clipboard/set", methods=["POST"])
def clipboard_set():
    text = request.data.decode("utf-8")
    copy_text(text)
    if verbose_logging:
        app.logger.debug("Text now in clipboard", {"text": text})
    copy_text(request.data.decode("utf-8"))
    response = make_response("", 200)
    response.headers["Content-type"] = "text/plain"
    return response


if __name__ == "__main__":
    app.run(
        # Use a safe default, even if it's less convenient
        host=app.config.get("HTTPCLIP_HOST", "127.0.0.1"),
        port=app.config.get("HTTPCLIP_PORT", 5000),
        threaded=True
    )
