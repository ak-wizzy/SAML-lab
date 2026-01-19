from flask import Flask, request, redirect, render_template, session, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from datetime import datetime
import os
import json

from config import Config

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY


# -------- Helpers --------

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
    """
    Initialise SAML auth using:
    - settings.json for SP structure
    - environment variables for IdP-sensitive values

    This avoids python3-saml's internal get_settings() mutation pitfalls.
    """
    base_path = os.path.join(os.path.dirname(__file__), "saml")

    # Load raw settings.json (authoritative schema)
    with open(os.path.join(base_path, "settings.json"), "r") as f:
        settings_dict = json.load(f)

    # Overlay IdP values from environment variables
    settings_dict["idp"]["entityId"] = Config.SAML_IDP_ENTITY_ID
    settings_dict["idp"]["singleSignOnService"]["url"] = Config.SAML_IDP_SSO_URL
    settings_dict["idp"]["x509cert"] = Config.SAML_IDP_X509CERT

    # Build validated settings object
    settings = OneLogin_Saml2_Settings(
        settings=settings_dict,
        custom_base_path=base_path
    )

    return OneLogin_Saml2_Auth(req, settings)


# -------- Routes --------

@app.route("/")
def index():
    return render_template(
        "index.html",
        authenticated="samlUserdata" in session,
        nameid=session.get("samlNameId"),
        login_time=session.get("login_time"),
        debug=session.get("debug", False)
    )


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
    session["login_time"] = datetime.utcnow().isoformat()

    # Default debug state from env
    session["debug"] = Config.SAML_DEBUG

    return redirect(url_for("claims"))


@app.route("/claims")
def claims():
    if "samlUserdata" not in session:
        return redirect(url_for("index"))

    return render_template(
        "claims.html",
        attributes=session["samlUserdata"],
        nameid=session.get("samlNameId"),
        session_index=session.get("samlSessionIndex"),
        debug=session.get("debug", False)
    )


@app.route("/toggle-debug")
def toggle_debug():
    session["debug"] = not session.get("debug", False)
    return redirect(request.referrer or url_for("index"))


@app.route("/logout")
def logout():
    # Local logout only
    session.clear()
    return redirect(url_for("index"))


@app.route("/slo")
def slo():
    if not Config.SAML_ENABLE_SLO:
        return "Single Logout (SLO) is disabled by configuration.", 403

    if "samlNameId" not in session or "samlSessionIndex" not in session:
        session.clear()
        return redirect(url_for("index"))

    req = prepare_flask_request(request)
    auth = init_saml_auth(req)

    return redirect(
        auth.logout(
            name_id=session["samlNameId"],
            session_index=session["samlSessionIndex"]
        )
    )


# -------- Entrypoint --------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
