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

    def to_html(self) -> str:
        raise NotImplementedError

    def properties_to_html(self) -> str:
        if self.properties is not None:
            html = ""
            for key, val in self.properties.items():
                html += f' {key}="{val}"'
            return html
        else:
            return ""

    def __repr__(self) -> str:
        return (
            f"HTMLNode:\n{self.tag}\n{self.content}\n{self.children}\n{self.properties}"
        )


class LeafNode(HTMLNode):

    def __init__(
        self, tag: str | None, content: str, properties: Dict | None = None
    ) -> None:
        super().__init__(tag, content, None, properties)

    def to_html(self) -> str:
        if self.content is None:
            raise ValueError
        else:

            if self.tag is not None:
                html = f"<{self.tag}{self.properties_to_html()}>{self.content}</{self.tag}>"
            else:
                html = self.content

            return html


class ParentNode(HTMLNode):

    def __init__(
        self, tag: str, children: List, properties: Dict | None = None
    ) -> None:
        super().__init__(tag, None, children, properties)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        elif self.children is None or not self.children:
            raise ValueError("ParentNode must have children")
        else:
            html = ""
            html += f"<{self.tag}>"
            for child in self.children:
                html += child.to_html()
            html += f"</{self.tag}>"
            return html
