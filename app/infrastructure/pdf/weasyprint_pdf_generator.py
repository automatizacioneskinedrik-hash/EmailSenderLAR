from app.infrastructure.templates.jinja_renderer import JinjaTemplateRenderer


class WeasyPrintPDFGenerator:
    def __init__(self, renderer: JinjaTemplateRenderer) -> None:
        self.renderer = renderer

    def generate(self, template_name: str, context: dict) -> bytes:
        try:
            from weasyprint import HTML
        except OSError as exc:  # pragma: no cover - depends on local native libs
            raise RuntimeError(
                "WeasyPrint necesita librerias nativas de sistema para generar PDFs."
            ) from exc

        html = self.renderer.render(template_name, context)
        return HTML(string=html).write_pdf()
