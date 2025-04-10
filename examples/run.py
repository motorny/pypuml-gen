import random
import string
from typing import Callable

from pypuml_gen.domain.exporter import LinesExporter
from pypuml_gen.domain.utilities import condition_if
from pypuml_gen.domain.uml_collection import UmlCollection
from pypuml_gen.domain.uml_link import UmlLink
from pypuml_gen.domain.uml_state import (
    UmlChoice,
    UmlFork,
    UmlJoin,
    UmlState,
    UmlStateProto,
)

condition1 = True
condition2 = False

uml_colleciton = UmlCollection()
UmlStateC = uml_colleciton.assoc(UmlState)
UmlLinkC = uml_colleciton.assoc(UmlLink)

a = UmlStateC(title="A")
b = UmlStateC(title="BB")
c = UmlStateC(title="CCC")

a.transition_to(b)
c.transition_from(b)


exporter = LinesExporter()
content = exporter.export(uml_colleciton)

TPL = """@startuml example-diag
{content}
@enduml
"""


with open("out.puml", "wt") as fout:
    fout.write(TPL.format(content=content, X=condition1, Y=condition2))
