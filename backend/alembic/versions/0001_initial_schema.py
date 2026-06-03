"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("subscription_tier", sa.String(20), nullable=False, server_default="free"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "supplements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100)),
        sa.Column("evidence_level", sa.String(1)),
        sa.Column("mechanisms", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("standard_dose", sa.String(100)),
        sa.Column("contraindications", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("known_interactions", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("need_weights", postgresql.JSONB(), nullable=False, server_default="{}"),
    )

    op.create_table(
        "questionnaire_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("responses", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("graph_state", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "user_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("need_scores", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("risk_flags", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("computed_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("supplement_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("score_breakdown", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("llm_explanation", sa.Text(), nullable=True),
        sa.Column("disclaimer_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("model_version", sa.String(50), nullable=False, server_default="1.0.0"),
    )


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("user_profiles")
    op.drop_table("questionnaire_sessions")
    op.drop_table("supplements")
    op.drop_table("users")
