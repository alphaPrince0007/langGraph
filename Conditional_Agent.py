from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from requests import get

class AgentState(TypedDict):
    number1: int
    number2: int
    operation1: str
    number3: int
    number4: int
    operation2: str
    finalNumber: int
    finalNumber2: int

def adder1(state: AgentState) -> AgentState:
    """This node adds the 2 numbers"""
    
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtractor1(state: AgentState) -> AgentState:
    """This node substracts the 2 numbers"""

    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def adder2(state: AgentState) -> AgentState:
    """This node adds the 2 numbers"""
    
    state["finalNumber2"] = state["finalNumber"] + state["number3"] + state["number4"]
    return state

def subtractor2(state:AgentState) -> AgentState:
    """This node subtracts the 2 numbers"""
    state["finalNumber2"] = state["finalNumber"] - state["number3"] - state["number4"]
    return state

def decide_layer_1(state: AgentState) -> AgentState:
    """This node will select the next node of the graph"""

    if state["operation1"] == "+":
        return "addition_operation"

    elif state["operation1"] == "-":
        return "subtraction_operation"
    else:
        raise ValueError("Invalid operation")
    

def decide_layer_2(state: AgentState) -> AgentState:
    """This node will select the next node of the graph"""

    if state["operation2"] == "+":
        return "addition_operation"

    elif state["operation2"] == "-":
        return "subtraction_operation"
    else:
        raise ValueError("Invalid operation")

    


graph = StateGraph(AgentState)

graph.add_node("add_node1", adder1)
graph.add_node("subtract_node1", subtractor1)
graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtractor2)

graph.add_node("router1", lambda state:state) #passthrough function
graph.add_node("router2", lambda state:state) #passthrough function

graph.add_edge(START, "router1")

graph.add_conditional_edges(
    "router1",
    decide_layer_1,

    {
        #Edge: Node
        "addition_operation": "add_node1",
        "subtraction_operation": "subtract_node1"
    }

)

graph.add_edge("add_node1", "router2")
graph.add_edge("subtract_node1", "router2")

graph.add_conditional_edges(
    "router2",
    decide_layer_2,
    {
        #Edge: Node
        "addition_operation": "add_node2",
        "subtraction_operation": "subtract_node2",
    }
)

graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

app = graph.compile()

graph_png = app.get_graph().draw_mermaid_png()
with open("graph2.png", "wb") as file:
    file.write(graph_png)


initial_state = {
    "number1": 10, "operation1": "-", "number2": 5,
    "number3": 2, "operation2": "+", "number4": 3
}

print(app.invoke(initial_state))

