from app.domain.models import CampusPayload
from app.infrastructure.templates.jinja_renderer import JinjaTemplateRenderer


def test_campus_payload_accepts_email_variable_aliases() -> None:
    campus = CampusPayload(
        USERNAME="carlos.perez",
        USERPASSWORD="Temporal123",
        PLATFORM_URL="https://campus.example.com",
        CERTIFICATE_URL="https://docs.example.com/matricula.pdf",
        CONTRACT_URL="https://docs.example.com/contrato.pdf",
    )

    assert campus.username == "carlos.perez"
    assert campus.password == "Temporal123"
    assert campus.platform_url == "https://campus.example.com"
    assert campus.enrollment_certificate_url == "https://docs.example.com/matricula.pdf"
    assert campus.educational_services_contract_url == "https://docs.example.com/contrato.pdf"


def test_welcome_email_renders_dynamic_variables() -> None:
    renderer = JinjaTemplateRenderer()
    campus = CampusPayload(
        username="carlos.perez",
        password="Temporal123",
        platform_url="https://campus.example.com",
        enrollment_certificate_url="https://docs.example.com/matricula.pdf",
        educational_services_contract_url="https://docs.example.com/contrato.pdf",
    )

    html = renderer.render(
        "emails/welcome.html",
        {
            "first_name": "Carlos",
            "user": {"name": "Carlos Perez", "email": "carlos@example.com"},
            "convocatoria": {"name": "Diplomado Seguridad"},
            "campus": campus,
        },
    )

    assert "Carlos" in html
    assert "Diplomado Seguridad" in html
    assert "carlos.perez" in html
    assert "Temporal123" in html
    assert "https://campus.example.com" in html
    assert "https://docs.example.com/matricula.pdf" in html
    assert "https://docs.example.com/contrato.pdf" in html
