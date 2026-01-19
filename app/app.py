from flask import Flask, request, redirect, render_template, session, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import os

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

def prepare_flask_request(req):
    return {
        "https": "on" if req.scheme == "https" else "off",
        "http_host": req.host,
        "script_name": req.path,
        "server_port": req.environ.get("SERVER_PORT"),
        "get_data": req.args.copy(),
        "post_data": req.form.copy()
    }

def init_saml_auth(req):
    return OneLogin_Saml2_Auth(
        req,
        custom_base_path=os.path.join(os.path.dirname(__file__), "saml")
    )

@app.route("/")
def index():
    return render_template("index.html", authenticated="samlUserdata" in session)

@app.route("/login")
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route("/acs", methods=["POST"])
def acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()

    errors = auth.get_errors()
    if errors:
        return f"SAML error: {errors}", 400

    if not auth.is_authenticated():
        return "Not authenticated", 403

    session["samlUserdata"] = auth.get_attributes()
    session["samlNameId"] = auth.get_nameid()
    session["samlSessionIndex"] = auth.get_session_index()

    return redirect(url_for("claims"))

@app.route("/claims")
def claims():
    if "samlUserdata" not in session:
        return redirect(url_for("index"))

    return render_template(
        "claims.html",
        attributes=session["samlUserdata"],
        nameid=session.get("samlNameId")
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
