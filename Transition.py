class Transition:

    CHILD_CELL = 0

    #fixed_style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;"

    def __init__(self):
        self.id = ''
        self.label = ''
        self.type = ''
        self.transition_type = ''
        self.from_id = ''
        self.to_id = ''
        self.value = self.TransitionValue()

    def extract(self, obj):
        self.label = obj.attrib['label'].lower().strip()
        self.type = obj.attrib['type'].lower().strip()
        self.from_id = obj[self.CHILD_CELL].attrib['source'].lower().strip()
        self.to_id = obj[self.CHILD_CELL].attrib['target'].lower().strip()

        #self.value = self.TransitionValue()
        #self.values.extract(obj)

    class TransitionValue:
        def __init__(self):
            self.from_header = ''
            self.on_field = ''
            self.on_value = ''
            self.on_value_type = ''

        def extract(self, values):
            self.on_field = values[self.CHILD_CELL].attrib['on_field'].lower().strip()
            self.on_value = values[self.CHILD_CELL].attrib['on_value'].lower().strip()
            self.on_value_type = values[self.CHILD_CELL].attrib['on_value_type'].lower().strip()
            self.from_header = values[self.CHILD_CELL].attrib['from_header'].lower().strip()

        def has_missing_params(self):
            return (not self.from_header.strip() or
                    not self.on_field.strip() or
                    not self.on_value or
                    not self.on_value_type)




