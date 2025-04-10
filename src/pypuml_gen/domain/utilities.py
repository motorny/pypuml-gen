from pypuml_gen.domain.uml_state import EmptyConditionalLink, UmlStateProto


def condition_if(state: UmlStateProto, cond: bool):
    if cond:
        return state
    else:
        return EmptyConditionalLink()
