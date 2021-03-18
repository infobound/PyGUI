class Form():
    def __init__(self):
        self._properties=dict()
        self._children=[]
        self._widget=None

        self._properties.update({"name": "Form"})
        self._properties.update({"width": 500})
        self._properties.update({"height": 500})
        self._properties.update({"left": 0})
        self._properties.update({"top": 0})
        self._properties.update({"text": "New Form"})
        self._properties.update({"drawmode": "Place"})

    def get_properties(self):
        return self._properties
    def set_properties(self,value):
        self._properties=value
    Properties = property(get_properties,set_properties)

    def get_children(self):
        return self._children
    def set_children(self,value):
        self._children=value
    Children = property(get_children,set_children)

    def get_widget(self):
        return self._widget
    def set_widget(self,value):
        self._widget=value
    Widget = property(get_widget,set_widget)
