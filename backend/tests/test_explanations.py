from types import SimpleNamespace

import httpx

from engine import explanations

SUPPLEMENT = SimpleNamespace(
    slug="magnesium-glycinate",
    name="Magnesio Glicinato",
    category="minerales",
    mechanisms=["relajacion_muscular"],
)
BREAKDOWN = {"category_contributions": {"sleep": 0.9, "stress": 0.8}}
PROFILE = {"sleep": 1.3, "stress": 1.7}


def _ok_response(_url, **_kwargs):
    return httpx.Response(
        200,
        request=httpx.Request("POST", _url),
        json={"choices": [{"message": {"content": "  El magnesio encaja con tu perfil.  "}}]},
    )


def test_ok_returns_text(monkeypatch):
    monkeypatch.setattr(explanations.httpx, "post", _ok_response)
    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN)
    assert result == "El magnesio encaja con tu perfil."


def test_timeout_returns_none(monkeypatch):
    def _raise(_url, **_kwargs):
        raise httpx.TimeoutException("timed out")

    monkeypatch.setattr(explanations.httpx, "post", _raise)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN) is None


def test_401_returns_none(monkeypatch):
    def _unauthorized(_url, **_kwargs):
        return httpx.Response(401, request=httpx.Request("POST", _url), json={"error": "invalid key"})

    monkeypatch.setattr(explanations.httpx, "post", _unauthorized)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN) is None


def test_broken_json_returns_none(monkeypatch):
    def _broken(_url, **_kwargs):
        return httpx.Response(200, request=httpx.Request("POST", _url), json={"unexpected": "shape"})

    monkeypatch.setattr(explanations.httpx, "post", _broken)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN) is None


def test_429_retries_once_then_succeeds(monkeypatch):
    calls = {"n": 0}

    def _post(_url, **_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, request=httpx.Request("POST", _url), json={"error": "rate limit"})
        return _ok_response(_url)

    monkeypatch.setattr(explanations.httpx, "post", _post)
    monkeypatch.setattr(explanations.time, "sleep", lambda _s: None)
    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN)
    assert result == "El magnesio encaja con tu perfil."
    assert calls["n"] == 2


def test_429_twice_returns_none(monkeypatch):
    calls = {"n": 0}

    def _post(_url, **_kwargs):
        calls["n"] += 1
        return httpx.Response(429, request=httpx.Request("POST", _url), json={"error": "rate limit"})

    monkeypatch.setattr(explanations.httpx, "post", _post)
    monkeypatch.setattr(explanations.time, "sleep", lambda _s: None)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN) is None
    assert calls["n"] == 2  # un intento + un único retry
