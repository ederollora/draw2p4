import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict


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


def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

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

    code_writer = CodeWriter()

    code_writer.write_headers(graph.headers, graph.longest_hname)

    code_writer.write_parser(graph.headers, graph.states, graph.transitions)

    #code_writer.write_defines()

    print(graph)

# Main body
if __name__ == '__main__':
    main()
