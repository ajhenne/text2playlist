import base64
import streamlit as st
import requests


def get_svg_html(path):

    with open(path, "rb") as f:
        base64_svg = base64.b64encode(f.read()).decode("utf-8")

    return f'<img src="data:image/svg+xml;base64,{base64_svg}" width="25">'


def record_pageview(page_path):
    headers = st.context.headers

    user_agent = headers.get("User-Agent", "Streamlit-App")
    ip = headers.get("X-Forwarded-For", "0.0.0.0").split(",")[0]

    url = "https://ajhenne.goatcounter.com/api/v0/count"
    token = st.secrets["goatcounter_key"]

    payload = {
        "no_sessions": False,
        "hits": [
            {
                "path": page_path,
                "title": page_path.strip("/").replace("-", " ").title(),
                "event": False,
                "ip": ip,
                "user_agent": user_agent,
            }
        ],
    }

    try:
        requests.post(
            url, json=payload, headers={"Authorization": f"Bearer {token}"}, timeout=1
        )
    except Exception:
        pass
