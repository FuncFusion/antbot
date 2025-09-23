from discord import ui


class LazyLayout(ui.LayoutView):
    def __init__(self, *components, container=True):
        super().__init__(timeout=None)
        if container:
            self.add_item(ui.Container(*components, id=1))
        else:
            for component in components:
                self.add_item(component)


