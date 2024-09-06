from domain.entity_property import EntityProperty


class EntityClass:
    def __init__(self, name: str, attributes: list[EntityProperty]) -> None:
        self.name = name
        self.attributes = attributes

    def get_context(self, project_name: str | None) -> dict:
        context = {
            "class_name": self.name,
            "properties": [prop.get_context() for prop in self.attributes],
        }
        if project_name:
            context["project_name"] = project_name

        return context

    def get_plural_name(self) -> str:
        if self.name.endswith("s"):
            return f"{self.name}es"
        return f"{self.name}s"
