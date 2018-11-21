from Constants import *


class CodeWriter:

    def __init__(self):
        self.name = ''
        self.fields = []
        self.typedefs = []
        self.defines = []
        self.consts = []

    def write_headers(self, headers, hname_length):

        header_compilation = "struct headers {" + NEWLINE

        for header_name, header in sorted(headers.items(), key=lambda h: h[1].stage):
            header_compilation += (4 * SPACE) + self.write_a_header(header, hname_length)

        header_compilation += CLOSING_BLOCK + NEWLINE

        with open(HEADERS_FILE, 'a') as header_file:
            header_file.write(header_compilation)

    def write_a_header(self, header, hname_length):

        with open(HEADERS_FILE, 'a') as header_file:
            header_file.write((
                HEADER_INIT +
                (2 * OPENING_BLOCK) +
                NEWLINE).format(header.name))
            for field in header.fields:
                header_file.write(
                    (INDENT + HEADER_LINE + NEWLINE).format(
                        field.bit_width,
                        ((header.longest_bw - len(str(field.bit_width))) * SPACE) + (2 * SPACE),
                        field.name)
                )
            header_file.write(CLOSING_BLOCK + (2 * NEWLINE))

        return ("{0}_t{1}{0};" + NEWLINE) \
            .format(header.name, ((hname_length - len(header.name)) * SPACE) + (2 * SPACE))

    def write_parser(self, headers, states, transitions):

        with open(PARSER_FILE, 'a') as parser_file:
            parser_file.write(
                PARSER + SPACE + PARSER_NAME + OPENING_PT + self.packet_in_arg() + NEWLINE +
                (4 * INDENT) + self.headers_arg() + NEWLINE +
                (4 * INDENT) + self.metadata_arg() + NEWLINE +
                (4 * INDENT) + self.smetadata_arg() + CLOSING_PT + SPACE + OPENING_BLOCK + (3 * NEWLINE))

            for state_id, state in sorted(states.items(), key=lambda s: s[1].stage):
                print(state.name)
                self.write_a_parse_block(state, transitions, states, headers, parser_file)

            parser_file.write(CLOSING_BLOCK + (2 * NEWLINE))

    def write_a_parse_block(self, current_state, transitions, states, headers, file):

        FIRST = 0

        # if an accept block then just return
        if current_state.name == 'accept':
            return

        # if a start block
        if (current_state.name == 'start'):
            file.write(INDENT + STATE_INIT.format(current_state.parse_name) + NEWLINE)
            parse_name = states[transitions[current_state.id][FIRST].to_id].parse_name
            file.write((2 * INDENT) + TRANSITION_DIRECT.format(parse_name) + NEWLINE)
            file.write(INDENT + CLOSING_BLOCK + (2*NEWLINE))
            return

        # if neither of above then regular header parsing

        file.write(INDENT + STATE_INIT.format(current_state.parse_name) + NEWLINE)
        file.write((2 * INDENT) + EXTRACT_LINE.format(HEADER_NAME, current_state.name) + NEWLINE)

        if len(current_state.transition_to) < 2:
            file.write((2 * INDENT) + TRANSITION_DIRECT.format(states[current_state.transition_to[FIRST].to_id].name)\
                           + NEWLINE)
        else:

            nxt_states = [states[nstate.to_id] for nstate in current_state.transition_to]
            on_fields = [x.default_trans[current_state.name].on_field for x in nxt_states if
                         current_state.name in x.default_trans]

            # if not len(on_fields) == len(nxt_states) or all(f == on_fields[ANY] for f in on_fields):
            # we have a problem here
            # pass

            file.write((2 * INDENT) + TRANSITION_INIT.format(HEADER_NAME, current_state.name, on_fields[FIRST]) + NEWLINE)

            trans = 0

            for transition in transitions[current_state.id]:

                print(current_state.name+" -> "+states[transition.to_id].name)

                trans += 1

                if states[transition.to_id].name == 'accept':
                    print()
                    file.write((2 * INDENT) + TRANSITION_ACCEPT + NEWLINE)
                    continue

                dt = None

                if current_state.name in states[transition.to_id].default_trans:
                    dt = states[transition.to_id].default_trans[current_state.name]

                if (dt is None and (transition.value is None)) or \
                        ((dt.has_missing_params()) or transition.value.has_missing_params()):
                    # we have a problem
                    pass

                from_header = dt.from_header if transition.value.has_missing_params() else transition.value.from_header
                on_field = dt.on_field if not transition.value.on_field else transition.value.on_field
                on_value = dt.on_value if not transition.value.on_value else transition.value.on_value
                on_value_type = dt.on_value_type if not transition.value.on_value_type else \
                    transition.value.on_value_type

                if on_value_type in BINARY_VALUES:
                    if not (on_value.startswith('0b') or on_value.startswith('0B')):
                        on_value = '0b' + on_value
                elif on_value_type in OCTAL_VALUES:
                    if not (on_value.startswith('0o') or on_value.startswith('0O')):
                        on_value = '0o' + on_value
                elif on_value_type in HEXADECIMAL_VALUES:
                    if not (on_value.startswith('0x') or on_value.startswith('0X')):
                        on_value = '0x' + on_value

                constant = on_field.upper() + "_" + states[transition.to_id].name.upper()

                if constant not in self.consts:
                    bit_width = headers[from_header].get_field_by_name(on_field).bit_width
                    self.consts.append({constant: (bit_width, on_value)})

                file.write((3 * INDENT) + TRANSITION_LINE.format(constant, states[transition.to_id].parse_name) + NEWLINE)

                if trans == len(transitions[current_state.id]):
                    file.write((3 * INDENT) + TRANS_DEFAULT + NEWLINE)

            file.write((2 * INDENT) + CLOSING_BLOCK + NEWLINE)

        file.write(INDENT + CLOSING_BLOCK + (2*NEWLINE))

    def write_all_defines(self):
        with open(DEFINES_FILE, 'a') as defines_file:
            if not defines_file.tell():
                defines_file.write((2 * NEWLINE))
            for const in self.consts:
                for const_name, (bit_width, value) in const.items():
                    defines_file.write(CONSTANT_ENTRY.format(bit_width, const_name, value) + NEWLINE)

    def write_main_file(self, args):

        with open(MAIN_FILE, 'a') as main_file:
            if not main_file.tell():
                main_file.write((2 * NEWLINE))

            for lib in self.libraries:
                main_file.write()

            main_file.write(NEWLINE)

            for inc in self.includes:
                main_file.write()

            main_file.write(NEWLINE)

            switch, body = self.switch_definition(args)

            #block of switch definition
            main_file(SWITCH_DEF.format(switch, body, MAIN_NAME))




    def packet_in_arg(self):
        return PACKET_IN + SPACE + PACKET_NAME + COMMA

    def headers_arg(self):
        return OUT + SPACE + HEADERS_TYPE + SPACE + HEADER_NAME + COMMA

    def metadata_arg(self):
        return INOUT + SPACE + METADATA_TYPE + SPACE + METADATA_NAME + COMMA

    def smetadata_arg(self):
        return INOUT + SPACE + SMETADATA_TYPE + SPACE + SMETADATA_NAME

    def switch_definition(self, args):
        model = MODELS[args.model]
        switch = model.keys()[0]
        body = ''

        for element in model[switch]:
            body += element + "()," + NEWLINE
        return (switch, body)



