from typing import Dict, List


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        content: str | None = None,
        children: List | None = None,
        properties: Dict | None = None,
    ) -> None:
        self.tag = tag
        self.content = content
        self.children = children
        self.properties = properties

    def to_html(self):
        raise NotImplementedError

    def properties_to_html(self) -> str:
        if self.properties is not None:
            html = ""
            for key, val in self.properties.items():
                html += f' {key}="{val}"'
            return html
        else:
            raise TypeError("Properties is None")

    def __repr__(self) -> str:
        return (
            f"HTMLNode:\n{self.tag}\n{self.content}\n{self.children}\n{self.properties}"
        )
