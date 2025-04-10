
from pypuml_gen.domain.uml_collection import UmlCollection


class LinesExporter:
    def export(self, collection: UmlCollection):
        return "\n".join(l.to_uml_lines() for l in collection.associated_items_iter())
