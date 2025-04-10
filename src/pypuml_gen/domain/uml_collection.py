from pypuml_gen.domain.umlable import Umlable


class UmlCollection:
    def __init__(self) -> None:
        self.umlable_items: list[Umlable] = []
        self.known_classes = {}

    def assoc(self, floating_class: type) -> type:
        """
        Returns new class that on each instance creation links this instance to the collection
        by adding it to the umlable_items
        """
        if Umlable not in floating_class.mro():
            raise ValueError(f"{floating_class} is non umlable - don't push it here")

        def get_collection(slf):
            return self

        class NewMeta(type):
            def __init__(cls, name, bases, namespace):
                super().__init__(name, bases, namespace)
                cls.get_collection = get_collection
                # print(cls)
                # print(cls.__dict__)
                # print("UmlCollection is creating new class: {}".format(cls))

            def __call__(cls, *args, **kwargs):
                """
                https://stackoverflow.com/a/67523758
                """
                new_instance = super().__call__(*args, **kwargs)
                # print("Class {} producing new instance: {}".format(cls, new_instance))
                self.umlable_items.append(new_instance)
                return new_instance

        new_uml_linked_class = NewMeta(
            floating_class.__name__ + "C", (floating_class,), {}
        )
        self.known_classes[floating_class.__name__] = new_uml_linked_class
        return new_uml_linked_class

    def associated_items_iter(self):
        return iter(self.umlable_items)
