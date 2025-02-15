from dataclasses import dataclass

from pypuml_gen.domain.uml_state import UmlState
from pypuml_gen.domain.umlable import Umlable


@dataclass
class UmlLink(Umlable):
    from_: UmlState
    to_: UmlState
    length: int = 2

    def to_uml_lines(self) -> str:
        arrow_part = "-" * self.length + ">"
        return f"{self.from_.fqdn} {arrow_part} {self.to_.fqdn}"
