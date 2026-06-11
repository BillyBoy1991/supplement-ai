from types import SimpleNamespace
from unittest.mock import MagicMock

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

CHUNKS = [
    SimpleNamespace(
        content="El magnesio modula el eje GABA-glutamato y favorece el sueño.",
        source="PubMed 2021 · PMID:34883514",
    ),
    SimpleNamespace(
        content="La forma glicinato presenta alta biodisponibilidad.",
        source="PubMed 2022 · PMID:35184264",
    ),
]


def _db_with_chunks(chunks):
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = chunks
    return db


def _no_embedding(monkeypatch):
    """Sin embeddings: la búsqueda de evidencia degrada y la DB no se toca."""
    monkeypatch.setattr(explanations, "get_embedding", MagicMock(side_effect=RuntimeError("no key")))


def _ok_response(_url, **_kwargs):
    return httpx.Response(
        200,
        request=httpx.Request("POST", _url),
        json={"choices": [{"message": {"content": "  El magnesio encaja con tu perfil.  "}}]},
    )


def test_ok_returns_text(monkeypatch):
    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _ok_response)
    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None)
    assert result == "El magnesio encaja con tu perfil."


def test_timeout_returns_none(monkeypatch):
    def _raise(_url, **_kwargs):
        raise httpx.TimeoutException("timed out")

    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _raise)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None) is None


def test_401_returns_none(monkeypatch):
    def _unauthorized(_url, **_kwargs):
        return httpx.Response(401, request=httpx.Request("POST", _url), json={"error": "invalid key"})

    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _unauthorized)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None) is None


def test_broken_json_returns_none(monkeypatch):
    def _broken(_url, **_kwargs):
        return httpx.Response(200, request=httpx.Request("POST", _url), json={"unexpected": "shape"})

    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _broken)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None) is None


def test_429_retries_once_then_succeeds(monkeypatch):
    calls = {"n": 0}

    def _post(_url, **_kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, request=httpx.Request("POST", _url), json={"error": "rate limit"})
        return _ok_response(_url)

    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _post)
    monkeypatch.setattr(explanations.time, "sleep", lambda _s: None)
    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None)
    assert result == "El magnesio encaja con tu perfil."
    assert calls["n"] == 2


def test_429_twice_returns_none(monkeypatch):
    calls = {"n": 0}

    def _post(_url, **_kwargs):
        calls["n"] += 1
        return httpx.Response(429, request=httpx.Request("POST", _url), json={"error": "rate limit"})

    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _post)
    monkeypatch.setattr(explanations.time, "sleep", lambda _s: None)
    assert explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=None) is None
    assert calls["n"] == 2  # un intento + un único retry


def test_evidence_chunks_injected_in_system_prompt(monkeypatch):
    captured = {}

    def _capture_post(_url, **kwargs):
        captured["payload"] = kwargs["json"]
        return _ok_response(_url)

    monkeypatch.setattr(explanations, "get_embedding", MagicMock(return_value=[0.0] * 384))
    monkeypatch.setattr(explanations.httpx, "post", _capture_post)

    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=_db_with_chunks(CHUNKS))

    assert result == "El magnesio encaja con tu perfil."
    system_msg = captured["payload"]["messages"][0]["content"]
    assert "Evidencia relevante:" in system_msg
    for chunk in CHUNKS:
        assert chunk.content in system_msg
        assert chunk.source in system_msg


def test_embedding_failure_degrades_to_no_evidence(monkeypatch):
    captured = {}

    def _capture_post(_url, **kwargs):
        captured["payload"] = kwargs["json"]
        return _ok_response(_url)

    db = _db_with_chunks(CHUNKS)
    _no_embedding(monkeypatch)
    monkeypatch.setattr(explanations.httpx, "post", _capture_post)

    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=db)

    assert isinstance(result, str)
    assert result == "El magnesio encaja con tu perfil."
    assert "Evidencia relevante:" not in captured["payload"]["messages"][0]["content"]
    db.query.assert_not_called()


def test_db_failure_degrades_to_no_evidence(monkeypatch):
    captured = {}

    def _capture_post(_url, **kwargs):
        captured["payload"] = kwargs["json"]
        return _ok_response(_url)

    db = MagicMock()
    db.query.side_effect = RuntimeError("pgvector no disponible")
    monkeypatch.setattr(explanations, "get_embedding", MagicMock(return_value=[0.0] * 384))
    monkeypatch.setattr(explanations.httpx, "post", _capture_post)

    result = explanations.generate_explanation(PROFILE, SUPPLEMENT, BREAKDOWN, db=db)

    assert isinstance(result, str)
    assert "Evidencia relevante:" not in captured["payload"]["messages"][0]["content"]
