"""Characterization tests — pin the observable behaviour of the legacy HMS before modernization.

These tests describe what the app DOES today (including its bugs), not what it should do.
They must stay green through S1–S3 (ADR-001). Known defects are marked xfail with a reason.
"""
from __future__ import annotations

import pytest
from flask.testing import FlaskClient

PUBLIC_GET = ["/", "/doctors", "/signup", "/login", "/test"]
PROTECTED_GET = ["/patients", "/bookings", "/details", "/search", "/logout"]


@pytest.mark.parametrize("path", PUBLIC_GET)
def test_public_pages_render(client: FlaskClient, path: str) -> None:
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("path", PROTECTED_GET)
def test_protected_pages_redirect_to_login(client: FlaskClient, path: str) -> None:
    resp = client.get(path)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_db_connectivity_probe(client: FlaskClient) -> None:
    assert client.get("/test").data == b"My database is Connected"


def test_doctor_registration_persists(client: FlaskClient) -> None:
    resp = client.post(
        "/doctors", data={"email": "d@example.com", "doctorname": "Dr. House", "dept": "Diagnostics"}
    )
    assert resp.status_code == 200
    assert b"Information is Stored" in resp.data


def test_signup_then_login_then_logout(client: FlaskClient) -> None:
    resp = client.post(
        "/signup",
        data={"username": "u1", "usertype": "Patient", "email": "u1@example.com", "password": "pw"},
    )
    assert b"Signup Succes" in resp.data
    dup = client.post(
        "/signup",
        data={"username": "u1", "usertype": "Patient", "email": "u1@example.com", "password": "pw"},
    )
    assert b"Email Already Exist" in dup.data
    login = client.post("/login", data={"email": "u1@example.com", "password": "pw"})
    assert login.status_code == 302
    bad = client.post("/login", data={"email": "u1@example.com", "password": "wrong"})
    assert b"invalid credentials" in bad.data
    assert client.get("/logout").status_code == 302


def test_patient_sees_booking_page_with_doctors(patient_client: FlaskClient) -> None:
    patient_client.post(
        "/doctors", data={"email": "d2@example.com", "doctorname": "Dr. Who", "dept": "Cardio"}
    )
    resp = patient_client.get("/patients")
    assert resp.status_code == 200
    assert b"Dr. Who" in resp.data or b"Cardio" in resp.data


@pytest.mark.xfail(
    reason="Legacy bug: booking POST references ast.Param['gmail-user'] -> TypeError (mail never sent)",
    strict=True,
)
def test_booking_post_confirms(patient_client: FlaskClient) -> None:
    resp = patient_client.post(
        "/patients",
        data={
            "email": "pat@example.com", "name": "Pat", "gender": "F", "slot": "Morning",
            "disease": "Flu", "time": "10:00", "date": "2026-10-20", "dept": "Cardio", "number": "123",
        },
    )
    assert b"Booking Confirmed" in resp.data


def test_bookings_and_details_render_for_doctor(doctor_client: FlaskClient) -> None:
    assert doctor_client.get("/bookings").status_code == 200
    assert doctor_client.get("/details").status_code == 200


def test_search_reports_doctor_availability(patient_client: FlaskClient) -> None:
    patient_client.post(
        "/doctors", data={"email": "d3@example.com", "doctorname": "Dr. Strange", "dept": "Neuro"}
    )
    found = patient_client.post("/search", data={"search": "Dr. Strange"})
    assert b"Doctor is Available" in found.data
    missing = patient_client.post("/search", data={"search": "Nobody"})
    assert b"Doctor is Not Available" in missing.data


def test_delete_redirects_to_bookings(doctor_client: FlaskClient) -> None:
    resp = doctor_client.get("/delete/999")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/bookings")


class TestSecurityBaseline:
    """Documents the CURRENT security posture. Expected to flip after S1."""

    @pytest.mark.xfail(reason="S1 target: SQL injection in /doctors INSERT (f-string)", strict=True)
    def test_sql_injection_in_doctor_registration_is_blocked(self, client: FlaskClient) -> None:
        payload = "x', 'y'); DELETE FROM doctors; --"
        resp = client.post("/doctors", data={"email": "a", "doctorname": payload, "dept": "z"})
        assert resp.status_code == 200
        # A hardened app stores the literal string instead of executing it.
        assert b"Information is Stored" in resp.data
        import main  # noqa: E402

        with main.app.app_context():
            rows = main.db.engine.execute("SELECT doctorname FROM doctors").fetchall()
        assert any(payload in r[0] for r in rows)

    @pytest.mark.xfail(reason="S1 target: secret_key hardcoded as 'mayank'", strict=True)
    def test_secret_key_is_not_hardcoded(self, legacy_app) -> None:
        assert legacy_app.secret_key != "mayank"
