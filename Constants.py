

DEFINES_FILE = "output/defines.p4"
HEADERS_FILE = "output/headers.p4"
PARSER_FILE = "output/parser.p4"
MAIN_FILE = "output/switch.p4"


MAIN_INCLUDE = "#include <core.p4>\n#include <v1model.p4>"
INCLUDE_FILE = "#include %s.p4"

HEADER_INIT = "header {0}_t"
HEADER_LINE = "bit<{0}>{1}{2};"

HEADERS_DEF = "struct headers"

PARSER = "parser"
PARSER_BLOCK_NAME = "MyParser"

PACKET_IN = "packet_in"
PACKET_NAME = "packet"

OUT = "out"
HEADERS_TYPE = "headers"
HEADER_NAME = "hdr"

INOUT = "inout"
METADATA_TYPE = "metadata"
METADATA_NAME = "meta"

SMETADATA_TYPE = "standard_metadata_t"
SMETADATA_NAME = "standard_metadata"

STATE_INIT = "state {0} {{"
EXTRACT_LINE = "packet.extract({0}.{1})"
TRANSITION_INIT = "transition select({0}.{1}.{2}) {{"
TRANSITION_LINE = "{0}: {1};"
TRANSITION_DIRECT = "transition {0};"
TRANSITION_ACCEPT = "transition accept;"
TRANS_DEFAULT = "default: accept;"

OPENING_PT = "("
CLOSING_PT = ")"
OPENING_BLOCK = "{"
CLOSING_BLOCK = "}"

COMMA = ","
DOT = "."
SPACE = " "
NEWLINE = "\n"
INDENT = (4 * SPACE)

BINARY_VALUES = ["binary", "bin", "b"]
OCTAL_VALUES = ["octal", "oct", "o"]
HEXADECIMAL_VALUES = ["hexadecimal", "hex", "h"]
DECIMAL_VALUES = ["decimal", "dec", "d"]