from dataclasses import dataclass
from classes.dto.element import Element


@dataclass
class Selector:
    title: Element
    contents: Element
    write_date: Element
    writer: Element

    def __init__(self, title, contents, write_date, writer):
        self.title = title
        self.contents = contents
        self.write_date = write_date
        self.writer = writer

        if not self.title:
            raise ValueError("title이 없음!")
        if not isinstance(self.title, Element):
            raise TypeError("title should be of type Element")

        if not self.contents:
            raise ValueError(f"contents이 없음!")
        if not isinstance(self.contents, Element):
            raise TypeError("contents should be of type Element")

        if not self.write_date:
            raise ValueError(f"write_date이 없음!")
        if not isinstance(self.write_date, Element):
            raise TypeError("write_date should be of type Element")

        if not self.writer:
            raise ValueError(f"writer이 없음!")
        if not isinstance(self.writer, Element):
            raise TypeError("writer should be of type Element")
