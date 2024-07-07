import pandas as pd
from graphviz import Digraph
import re

def get_nfa():
    nfa = {}                                 
    s = int(input("how many total states ?: "))            
    p = int(input("How many different path?: "))
    print("for example you have 2 states q0 and q1 ,and 2 paths a and b . We ask you to enter the all conditions you will go to in the states (q0,a) ,(q0,b),(q1,a) and (q1,b). even if it is empty, please enter it as empty.")
    for i in range(s):  
        state = input("Current state is: ")            
        nfa[state] = {}                           
        for j in range(p):
            path = input("path : ") 
            print("Enter end state from state {} travelling through path {} : ".format(state,path))
            reaching_state = [x for x in input().split()] #boşluk ile ayır
            nfa[state][path] = reaching_state     
    nfa1=merge_sublists(nfa)
    print("\n---------NFA transitions---------")
    for state, paths in nfa1.items():
        for path, target_states in paths.items():
            print(f"\u03B4({state}, {path}) -> {target_states}")                        
    print("\n---------NFA table---------")
    nfa_table = pd.DataFrame(nfa)
    print(nfa_table.transpose())

    print("Enter final state of NFA : ")
    nfa_final_state = [x for x in input().split()]                                
    return nfa, nfa_final_state

def nfa_to_dfa(nfa,start_state, nfa_final_states):
    f=nfa_final_states
    dfa = {}
    queue = []
    dfa_final_states = set()
    paths = list(nfa[list(nfa.keys())[0]].keys()) ###

    start_state_dfa = frozenset([start_state])
    queue.append(start_state_dfa)
    dfa[start_state_dfa] = {}

    while queue:
        current = queue.pop(0)
        if current not in dfa:
            dfa[current] = {}

        for path in paths:
            target_state = set()
            for state in current:
                if path in nfa[state]:
                    target_state.update(nfa[state][path])
            
            target_state = frozenset(target_state)
            dfa[current][path] = target_state

            if target_state not in dfa:
                queue.append(target_state)

    # Convert DFA to readable format
    readable_dfa = {}
    for state, transitions in dfa.items():
        state_name = ",".join(state) if state else ''
        readable_dfa[state_name] = {path: list(transitions[path]) for path in transitions}

        if any(nfa_final_state in state for nfa_final_state in f):
            dfa_final_states.add(state_name)

    return readable_dfa, ["".join(state) for state in dfa_final_states]

    
def visualize_automata(automata, final_states, title="Automata"):
    dot = Digraph()
    dot.attr(rankdir='LR')#yatay
    dot.node('start', shape='point')
    
    for state in automata:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    
    dot.edge('start', list(automata.keys())[0])
    
    for state, transitions in automata.items():
        for path, end_states in transitions.items():
            if isinstance(end_states, list):
                for end_state in end_states:
                    dot.edge(state, end_state, label=path)
            else:
                dot.edge(state, end_states, label=path)
    
    dot.render(title, format='png', cleanup=True)
    dot.view()

def merge_sublists(dfa):
    dfa = remove_empty_states(dfa)
    new_dfa = {}
    for state, transitions in dfa.items():
        new_transitions = {}
        for path, target_states in transitions.items():
            if isinstance(target_states, str):
                new_transitions[path] = target_states
            else:
                merged_target_states = []
                for sub_state in target_states:
                    merged_target_states.extend(sub_state.split(","))
                merged_target_states = list(set(merged_target_states))
                merged_target_states = ",".join(merged_target_states)
                new_transitions[path] =merged_target_states
        new_dfa[state] = new_transitions
    return new_dfa

def remove_empty_states(dfa):
    new_dfa = {state: transitions for state, transitions in dfa.items() if state != ''}
    return new_dfa
    
if __name__ == "__main__":
    start_state='q0'
    nfa, nfa_final_state= get_nfa()
    visualize_automata(nfa, nfa_final_state, "NFA")
    dfa, dfa_final_states = nfa_to_dfa(nfa, start_state, nfa_final_state)
    dfa=merge_sublists(dfa)
    print("\n---------DFA transitions---------")
    for state, path in dfa.items():
        for path, merged_target_states in path.items():
            print(f"\u03B4({state}, {path}) -> {merged_target_states}")                   
    dfa_table=pd.DataFrame(dfa)
    print("\n---------DFA table---------")
    print(dfa_table.transpose())
    print("Final states of DFA :")
    print(dfa_final_states)
    visualize_automata(dfa, dfa_final_states, "DFA")

