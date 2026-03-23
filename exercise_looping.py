from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict):
    name: str
    secret_number: int
    guess: int
    attempts: int
    lower_bound: int
    upper_bound: int
    status: str

def guess_node(state: AgentState) -> AgentState:
    """Node where the agent makes a guess"""
    state["guess"] = (state["lower_bound"] + state["upper_bound"]) // 2
    state["attempts"] += 1
    return state

def hint_node(state: AgentState) -> AgentState:
    """Node where the agent receives a hint"""
    if state["guess"] > state["secret_number"]:
        state["upper_bound"] = state["guess"] - 1
    elif state["guess"] < state["secret_number"]:
        state["lower_bound"] = state["guess"] + 1
    else:
        state["status"] = "found"

def setup_node(state: AgentState) -> AgentState:
    """This is the setup node where"""
    state["secret_number"] = random.randint(1, 20)
    state["lower_bound"] = 1
    state["upper_bound"] = 20
    state["attempts"] = 0
    state["status"] = "searching"
    return state

def should_continue(state: AgentState) -> AgentState:
    # logic to break the loop
    if state["status"] == "found":
        return "exit"
    if state["attempts"] >= 7:
        return "exit"
    return "loop" 

graph = StateGraph(AgentState)

graph.add_node("setup", setup_node)
graph.add_node("guess", guess_node)
graph.add_node("hint", hint_node)

graph.add_edge(START, "setup")
graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint")

graph.add_conditional_edges(
    "hint",
    should_continue,
    {
        "loop": "guess", # This creates the back-edge for binary search
        "exit": END
    }
)

app = graph.compile()

# graph_png = app.get_graph().draw_mermaid_png()
# with open("graph5.png", "wb") as f:
#     f.write(graph_png)

print(app.invoke({"name": "Prince"}))
