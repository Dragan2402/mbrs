class EntityProperty:
    def __init__(
        self,
        name: str,
        property_type: str,
        is_single_reference: bool = False,
        is_reference: bool = False,
    ) -> None:
        name = name[0].upper() + name[1:]
        self.name = name
        self.type = property_type
        self.is_single_reference = is_single_reference
        self.is_reference = is_reference
        self.displayed_in_reference = False
        self.include = False
        self.label = name

    def get_context(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "is_single_reference": self.is_single_reference,
            "is_reference": self.is_reference,
            "displayed_in_reference": self.displayed_in_reference,
            "include": self.include,
            "label": self.label,
        }
