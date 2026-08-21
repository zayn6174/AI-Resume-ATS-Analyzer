from typing import Any, Dict, List

import requests
import streamlit as st


DEFAULT_BACKEND_URL = "http://127.0.0.1:8000"


def _backend_url() -> str:
    try:
        url = st.secrets["backend"]["url"]
        st.sidebar.write("DEBUG BACKEND:", url)
        return url
    except (KeyError, FileNotFoundError):
        st.sidebar.write("DEBUG USING LOCAL BACKEND")
        return DEFAULT_BACKEND_URL


def _auth_headers(access_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def health_check() -> Dict[str, Any]:
    response = requests.get(f"{_backend_url()}/api/v1/health", timeout=10)
    response.raise_for_status()
    return response.json()


def analyze_resume(
    resume_file,
    access_token: str,
    job_description: str = "",
) -> Dict[str, Any]:

    print("=== ANALYZE RESUME CALLED ===")
    print("TOKEN LENGTH:", len(access_token))
    print("TOKEN START:", access_token[:20])

    backend = _backend_url()
    print("USING BACKEND:", backend)

    files = {
        "resume": (
            resume_file.name,
            resume_file.getvalue(),
            resume_file.type,
        ),
    }

    data = {
        "job_description": job_description
    }

    print("SENDING REQUEST TO:", f"{backend}/api/v1/analyze-resume")
    print("🚀 BEFORE BACKEND REQUEST")

    response = requests.post(
        f"{backend}/api/v1/analyze-resume",
        files=files,
        data=data,
        headers=_auth_headers(access_token),
        timeout=(10,180)
    )
    print("✅ AFTER BACKEND REQUEST:", response.status_code)

    print("BACKEND STATUS:", response.status_code)
    print("BACKEND RESPONSE:", response.text[:500])

    response.raise_for_status()

    result = response.json()

    print("========== API CLIENT DEBUG ==========", flush=True)
    print("KEYS:", result.keys(), flush=True)
    print("COMPONENT SCORES:", result.get("component_scores"), flush=True)
    print("ATS SCORE:", result.get("ats_score"), flush=True)
    print("======================================", flush=True)

    return result


def get_history(access_token: str) -> List[Dict[str, Any]]:
    response = requests.get(
        f"{_backend_url()}/api/v1/history",
        headers=_auth_headers(access_token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def delete_history_entry(analysis_id: str, access_token: str) -> None:
    response = requests.delete(
        f"{_backend_url()}/api/v1/history/{analysis_id}",
        headers=_auth_headers(access_token),
        timeout=30,
    )
    response.raise_for_status()


def generate_pdf(analysis_data: Dict[str, Any], access_token: str) -> bytes:
    response = requests.post(
        f"{_backend_url()}/api/v1/generate-pdf",
        json=analysis_data,
        headers=_auth_headers(access_token),
        timeout=60,
    )
    response.raise_for_status()
    return response.content


def get_history_pdf(analysis_id: str, access_token: str) -> bytes:
    response = requests.get(
        f"{_backend_url()}/api/v1/history/{analysis_id}/pdf",
        headers=_auth_headers(access_token),
        timeout=60,
    )
    response.raise_for_status()
    return response.content
