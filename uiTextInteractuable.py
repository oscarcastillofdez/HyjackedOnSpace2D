class uiTextInteractuable():
    def __init__(self) -> None:
        pass
    
    def update(self, observable):
        self.setInteractualeText(observable.getInteractuableText(), "black")