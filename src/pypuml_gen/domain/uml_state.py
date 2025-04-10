import random
import string
import dataclasses
from dataclasses import dataclass
from typing import Protocol

from pypuml_gen.domain.umlable import Umlable


class UmlStateProto(Protocol):
    def to_uml_lines(self) -> str: ...

    def requires(self, needed_state: "UmlState"): ...

    def implies(self, needed_state: "UmlState"): ...


class UmlStateProtoCls(Protocol):
    def __call__(*args, **kwargs) -> UmlStateProto: ...


class AndedStates:
    def __init__(self, *args):
        self.states = args
        # print("constructed anded state of", self.states)


class OredStates:
    def __init__(self, *args):
        self.states = args
        print("constructed ored state of", self.states)


class EmptyConditionalLink:
    def __and__(self, other):
        if isinstance(other, EmptyConditionalLink):
            return AndedStates()
        return AndedStates(other)

    def __or__(self, other):
        if isinstance(other, EmptyConditionalLink):
            return OredStates()
        return OredStates(other)


@dataclass
class UmlState(Umlable):
    fqdn: str = dataclasses.field(default_factory=lambda: "".join(random.choices(string.ascii_uppercase, k=5)))
    title: str | None = None
    is_join: bool = False
    style: str = ""

    def to_uml_lines(self) -> str:
        title_part = ('"' + self.title + '" as ') if self.title else ""
        style_part: str = (" " + self.style) if self.style else ""
        return "state " + title_part + self.fqdn + style_part

    def transition_from(self, needed_state: "UmlState", cond: bool = None):
        if cond is not None:
            if not cond:
                return self
        coll = self.get_collection()
        link_class = coll.known_classes["UmlLink"]

        if isinstance(needed_state, EmptyConditionalLink):
            return self

        if isinstance(needed_state, AndedStates):
            # print("got anded states", needed_state)
            fork_class = coll.known_classes["UmlFork"]
            join = fork_class(fqdn="".join(random.choices(string.ascii_uppercase, k=5)))
            link_class(join, self)
            for requrements_state in needed_state.states:
                link_class(requrements_state, join)
            return join
        if isinstance(needed_state, OredStates):
            # print("got anded states", needed_state)
            choice_class = coll.known_classes["UmlChoice"]
            choice = choice_class(
                fqdn="".join(random.choices(string.ascii_uppercase, k=5))
            )
            link_class(choice, self)
            for requrements_state in needed_state.states:
                link_class(requrements_state, choice)
            return choice
        link = link_class(needed_state, self)
        return link

    def transition_to(self, implied_state: "UmlState"):
        """
        just like requires, but other direction
        """
        coll = self.get_collection()
        link_class = coll.known_classes["UmlLink"]
        link = link_class(self, implied_state)
        return link

    def __and__(self, other):
        if isinstance(other, EmptyConditionalLink):
            return self
        return AndedStates(self, other)

    def __or__(self, other):
        if isinstance(other, EmptyConditionalLink):
            return self
        return OredStates(self, other)


@dataclass
class UmlFork(UmlState):
    def to_uml_lines(self) -> str:
        return "state " + self.fqdn + " <<fork>>"


@dataclass
class UmlJoin(UmlState):
    def to_uml_lines(self) -> str:
        return "state " + self.fqdn + " <<join>>"


@dataclass
class UmlChoice(UmlState):
    def to_uml_lines(self) -> str:
        return "state " + self.fqdn + " <<choice>>"
