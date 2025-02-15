import random
import string
from typing import Callable

from pypuml_gen.domain.condition_if import condition_if
from pypuml_gen.domain.uml_collection import UmlCollection
from pypuml_gen.domain.uml_link import UmlLink
from pypuml_gen.domain.uml_state import (
    UmlChoice,
    UmlFork,
    UmlJoin,
    UmlState,
    UmlStateProto,
)

uml_colleciton = UmlCollection()

condition1 = True
condition2 = False


UmlStateC: Callable[..., UmlStateProto] = uml_colleciton.assoc(UmlState)
UmlLinkC: type = uml_colleciton.assoc(UmlLink)
UmlForkC: type = uml_colleciton.assoc(UmlFork)
UmlJoinC: type = uml_colleciton.assoc(UmlJoin)
UmlChoiceC = uml_colleciton.assoc(UmlChoice)

a: UmlStateProto = UmlStateC(title="A", fqdn="a", style="#line:red;line.bold")
b = UmlStateC(
    title="B",
    fqdn="b",
)


c = UmlStateC(
    title="C",
    fqdn="c",
)

d = UmlStateC(
    title="D",
    fqdn="d",
)

e = UmlStateC(
    title="E",
    fqdn="e",
)

f = UmlStateC(
    title="F",
    fqdn="f",
)

a.requires(b)
c.implies(a)


d.requires(e & f).requires(
    condition_if(a, cond=condition1) | condition_if(b, cond=condition2)
)

join3 = UmlJoinC(fqdn="".join(random.choices(string.ascii_uppercase, k=5)))

content = uml_colleciton.export_lines()

TPL = """@startuml example-diag
note as N1
    Some note
end note

note as N2
    X - {X}
    Y - {Y}
end note

{content}

state choice_example <<choice>>
note left of choice_example : "one of"
state join_example <<join>>
note left of join_example : "all"
@enduml
"""


with open("out.puml", "wt") as fout:
    fout.write(TPL.format(content=content, X=condition1, Y=condition2))
