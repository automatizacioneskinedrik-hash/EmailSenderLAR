from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


class JinjaTemplateRenderer:
    def __init__(self) -> None:
        templates_dir = Path(__file__).resolve().parents[2] / "templates"
        self.environment = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def render(self, template_name: str, context: dict) -> str:
        template = self.environment.get_template(template_name)
        return template.render(**context)
