"""Management CLI for the RMW API.

Usage:
    python cli.py create-superadmin
    python cli.py promote-superadmin
"""
import typer
from db.db_setup import SessionLocal
from db.models import User
from db.audit import log_action
from auth.crud import get_user_by_email
from auth.handler_password import generate_password_hash

app = typer.Typer(help="RMW-API management commands", add_completion=False)


def _abort_if_superadmin_exists(db) -> None:
    """Enforce the single super admin constraint shared by both commands."""
    if db.query(User).filter(User.role == "admin").first():
        typer.secho("A super admin already exists. Only one is allowed.", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("create-superadmin")
def create_superadmin(
    first_name: str = typer.Option(..., prompt=True),
    last_name: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, hide_input=True, confirmation_prompt=True
    ),
    created_by: str = typer.Option(
        ..., prompt="Your name/email (recorded in the audit log for this action)"
    ),
):
    """Create a new super admin (role='admin') user.

    Only one super admin is allowed; the command refuses to run if one
    already exists. `--created-by` identifies who ran the command and is
    stored on the resulting audit log entry so super admin creation stays
    traceable.
    """
    db = SessionLocal()
    try:
        _abort_if_superadmin_exists(db)

        if get_user_by_email(email=email, db=db):
            typer.secho(f"A user with email '{email}' already exists.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
            role="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        log_action(
            db=db,
            entity_type="user",
            entity_uuid=user.uuid,
            action="cli_create_superadmin",
            actor_id=None,
            changes={"role": {"from": None, "to": "admin"}, "created_by": created_by},
        )

        typer.secho(
            f"Super admin '{user.email}' created successfully by '{created_by}'.",
            fg=typer.colors.GREEN,
        )
    finally:
        db.close()


@app.command("promote-superadmin")
def promote_superadmin(
    email: str = typer.Option(..., prompt=True),
    promoted_by: str = typer.Option(
        ..., prompt="Your name/email (recorded in the audit log for this action)"
    ),
):
    """Promote an existing user to super admin (role='admin').

    Only one super admin is allowed; the command refuses to run if one
    already exists. `--promoted-by` identifies who ran the command and is
    stored on the resulting audit log entry so the promotion stays traceable.
    """
    db = SessionLocal()
    try:
        _abort_if_superadmin_exists(db)

        user = get_user_by_email(email=email, db=db)
        if not user:
            typer.secho(f"No user found with email '{email}'.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        old_role = user.role
        user.role = "admin"
        db.add(user)
        db.commit()
        db.refresh(user)

        log_action(
            db=db,
            entity_type="user",
            entity_uuid=user.uuid,
            action="cli_promote_superadmin",
            actor_id=None,
            changes={"role": {"from": old_role, "to": "admin"}, "promoted_by": promoted_by},
        )

        typer.secho(
            f"User '{user.email}' promoted to super admin by '{promoted_by}'.",
            fg=typer.colors.GREEN,
        )
    finally:
        db.close()


if __name__ == "__main__":
    app()
