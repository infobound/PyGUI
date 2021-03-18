class Child(object):
    def __init__(self):
        self._library=""
        self._class=""
        self._properties=dict()
        self._children=[]
        self._widget=None

    def get_library(self):
        return self._library
    def set_library(self,value):
        self._library=value
    Library = property(get_library,set_library)

    def get_class(self):
        return self._class
    def set_class(self,value):
        self._class=value
    Class = property(get_class,set_class)

    def get_children(self):
        return self._children
    def set_children(self,value):
        self._children=value
    Children = property(get_children,set_children)

    def get_properties(self):
        return self._properties
    def set_properties(self,value):
        self._properties=value
    Properties = property(get_properties,set_properties)

    def get_widget(self):
        return self._widget
    def set_widget(self,value):
        self._widget=value
    Widget = property(get_widget,set_widget)