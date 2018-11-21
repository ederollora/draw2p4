import sys
import xml.etree.ElementTree as ET
import argparse



from CodeWriter import CodeWriter
from Graph import Graph
from State import State
from Header import Header
from Transition import Transition

TYPE_STATE = "state"
TYPE_TRANSITION = "transition"

INNER = "inner_"
OUTER = "outer_"

CHILD_CELL = 0

SOURCE = 0
TARGET = 1

__author__ = 'Jason Vasquez Orona'


def get_args():

    parser = argparse.ArgumentParser()
    parser.parse_args()

    parser = argparse.ArgumentParser(
        description='Application that converts a graph into P4 headers, parser and the rest of the template')
    # Add arguments

    parser.add_argument(
        '-m', '--model', type=str, help='Model', required=True, )

    parser.add_argument(
        '-p', '--path', type=str, help='Port number', required=False, default=None, nargs='+')

    parser.add_argument(
        '-i', '--includes_folder', type=str, help='Separate folder for includes', required=False, default=False, action="store_true")

    return parser.parse_args()


def model_config(args):




    pass


def main(args):

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    code_writer = CodeWriter()

    model_config(args)

    stage_num = 0
    stages = 0

    start_id = 0
    end_id = 0

    transitions = {}
    states = {}

    graph = Graph()

    for obj in root.iter('object'):

        #if(obj.child().attrib["style"].split(";") == "ellipse")
        #    then this is a state

        type = (obj.get("type") or "no_type").lower().strip()

        if type == "transition":
            if "endArrow" in obj[CHILD_CELL].attrib['style']:
                # At this point we confirm this is a transition

                if "source" not in obj[CHILD_CELL].attrib:
                    raise Exception('Transition arrow with id:'+obj.get('id')+' is missing source connection. Check it is correctly attached to a source state')
                if "target" not in obj[CHILD_CELL].attrib:
                    raise Exception('Transition arrow with id:'+obj.get('id')+' is missing target connection. Check it is correctly attached to a target state')

                new_transition = Transition()
                new_transition.extract(obj)

                if obj[CHILD_CELL].get('source') not in transitions:
                    transitions[obj[CHILD_CELL].get('source')] = []
                transitions[obj[CHILD_CELL].get('source')].append(new_transition)
            else:
                # Not sure what to do if we reach here
                continue
        elif type == "state":
            #print obj.findall("mxCell")[0]
            if "ellipse" in obj[CHILD_CELL].attrib['style']:
                # At this point we confirm this is a state
                if obj.get('name').lower() == "start":
                    start_id = obj.get('id')

                if obj.get('name').lower() == "accept":
                    end_id = obj.get('id')

                new_state = State()
                new_state.extract(obj)


                if not graph.headers:
                    graph.headers = {}

                all_fields = {k: obj.get(k) for k in obj.attrib.keys() if k.startswith("h_")}

                if new_state.name not in graph.headers and \
                        len(all_fields) > 0:
                    new_header = Header()
                    new_header.extract(obj, all_fields)

                    new_header.fields.sort(key=lambda x: x.position, reverse=False)

                    new_state.parse_headers.append(new_header)
                    graph.headers[new_header.name] = new_header


                graph.states[new_state.id] = new_state

                if len(new_state.name) > graph.longest_hname:
                    graph.longest_hname = len(new_state.name)

                if obj.get('id') not in states:
                    states[obj.get('id')] = new_state
                else:
                    # problem
                    continue

    #next stage state ids
    stage_ids = []
    next_stage_ids = []
    stage_ids.append(start_id)
    stage = 0

    while len(stage_ids) > 0:
        id = stage_ids[0]
        stage_ids.remove(id)
        state = states[id]
        state.stage = stage

        for header in state.parse_headers:
            header.stage = state.stage

        if id in transitions:
            for transition in transitions[id]:
                if not state.transition_to:
                    state.transition_to = []
                if state.id not in  graph.transitions:
                    graph.transitions[state.id] = []

                state.transition_to.append(transition)
                graph.transitions[state.id].append(transition)

                if transition.to_id not in next_stage_ids:
                    next_stage_ids.append(transition.to_id)

        if not stage_ids:
            stage+=1
            stage_ids.extend(next_stage_ids)
            next_stage_ids = []


    code_writer.write_headers(graph.headers, graph.longest_hname)
    code_writer.write_parser(graph.headers, graph.states, graph.transitions)
    code_writer.write_all_defines()
    code_writer.write_main_file()

    print(graph)

# Main body
if __name__ == '__main__':

    args = get_args()
    main(args)
