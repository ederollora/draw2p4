from Transition import Transition


class State:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.stage = 0
        self.label = ''
        self.parse_name = ''
        self.parse_headers = []
        self.type = None
        self.default_trans = {}
        self.transition_to = []

    def extract(self, obj):
        self.id = obj.get('id').lower().strip()
        self.name = obj.get('name').lower().strip()
        self.label = obj.get('label').strip().lower()
        self.parse_name = (obj.get('parse_name') or "parse_" + obj.get('name')).lower().strip()
        self.type = obj.get('type').lower().strip()

        self.parse_headers = []

        p_t = [v for k, v in obj.attrib.items() if k.startswith('trans_prev')]

        for t in p_t:
            if len(t.split(":")) == 4:
                header, field, value_type, value = t.split(":")

                tr = Transition.TransitionValue()

                tr.from_header = header
                tr.on_field = field
                tr.on_value_type = value_type
                tr.on_value = value
                self.default_trans[tr.from_header] = tr
            else:
                # problem, not en enough values
                continue
