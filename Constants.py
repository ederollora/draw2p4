
DEFINES_FILENAME = "defines"
HEADERS_FILENAME = "headers"
PARSER_FILENAME = "parser"
MAIN_FILENAME = "switch"
P4_EXTENSION = ".p4"

OUTPUT_DIR = "output"


MAIN_INCLUDE = "#include <core.p4>\n#include <v1model.p4>"
INCLUDE_FILE = "#include %s.p4"

HEADER_INIT = "header {0}_t"
HEADER_LINE = "bit<{0}> {1} {2};"

HEADERS_DEF = "struct headers"

PARSER = "parser"
CONTROL = "control"

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

DEFINE_ENTRY = "#define {0} {1}"
CONSTANT_ENTRY = "const bit<{0}> {1} = {2};"
TYPEDEF_ENTRY = "typedef bit<{0}> {1};"

CORE_FILE = "core"
V1MODEL_FILE = "v1model"
IMPORT_LINE = "#include {0}"

SWITCH_DEF = "{0} ({1}) {2};"
CONTROL_BLOCK_DEF = "{0} {1} ({2})"

MAIN_NAME = "main"

OPENING_PT = "("
CLOSING_PT = ")"
OPENING_BLOCK = "{"
CLOSING_BLOCK = "}"

SLASH = "/"
COMMA = ","
DOT = "."
SPACE = " "
NEWLINE = "\n"
INDENT = (4 * SPACE)

BINARY_VALUES = ["binary", "bin", "b"]
OCTAL_VALUES = ["octal", "oct", "o"]
HEXADECIMAL_VALUES = ["hexadecimal", "hex", "h"]
DECIMAL_VALUES = ["decimal", "dec", "d"]


