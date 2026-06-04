"""
Grafo LangGraph del cuestionario.

15 nodos (uno por pregunta) en flujo lineal, con una bifurcación condicional tras
la pregunta de medicación. LangGraph SOLO orquesta el flujo: las preguntas son
fijas y no interviene ningún LLM. El estado se persiste en Postgres mediante el
checkpointer oficial de LangGraph, usando el id de sesión como thread_id.
"""
from typing import TypedDict

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from agent.questions import ORDER, has_meaningful_text, needs_for, payload
from core.config import settings


class QState(TypedDict):
    responses: dict
    medication_reported: bool


def _make_question_node(question_id: str):
    def node(state: QState) -> dict:
        answer = interrupt(payload(question_id))
        return {"responses": {**state["responses"], question_id: answer}}

    return node


def _safety_notice(state: QState) -> dict:
    return {"medication_reported": True}


def _route_medication(state: QState) -> str:
    return "safety_notice" if has_meaningful_text(state["responses"].get("medication")) else "next"


def _build():
    builder = StateGraph(QState)
    for qid in ORDER:
        builder.add_node(qid, _make_question_node(qid))
    builder.add_node("safety_notice", _safety_notice)

    builder.add_edge(START, ORDER[0])
    for i, qid in enumerate(ORDER):
        nxt = ORDER[i + 1] if i + 1 < len(ORDER) else END
        if qid == "medication":
            builder.add_conditional_edges(
                qid, _route_medication, {"safety_notice": "safety_notice", "next": nxt}
            )
            builder.add_edge("safety_notice", nxt)
        else:
            builder.add_edge(qid, nxt)
    return builder


_conninfo = settings.database_url.replace("+psycopg", "")
_pool = ConnectionPool(
    _conninfo,
    max_size=10,
    kwargs={"autocommit": True, "row_factory": dict_row},
    open=False,
)
_checkpointer = PostgresSaver(_pool)
APP = _build().compile(checkpointer=_checkpointer)


def setup_checkpointer() -> None:
    """Abre el pool y crea las tablas del checkpointer. Llamar al arrancar la app."""
    _pool.open()
    _checkpointer.setup()


def _cfg(session_id: str) -> dict:
    return {"configurable": {"thread_id": str(session_id)}}


def _interpret(result: dict) -> dict:
    responses = result.get("responses", {})
    interrupts = result.get("__interrupt__")
    if interrupts:
        return {"finished": False, "question": interrupts[0].value, "responses": responses}
    return {"finished": True, "question": None, "responses": responses}


def start_session(session_id: str) -> dict:
    result = APP.invoke({"responses": {}, "medication_reported": False}, _cfg(session_id))
    return _interpret(result)


def submit_answer(session_id: str, answer: object) -> dict:
    result = APP.invoke(Command(resume=answer), _cfg(session_id))
    return _interpret(result)
