from langgraph.graph import StateGraph, END
import random
from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """Greeting Node which says hi to the person"""
    state["name"] = f"Hi there, {state["name"]}"
    state["counter"] = 0
    return state


def random_node(state: AgentState) -> AgentState:
    """Generates a random number from 0 to 10"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1
    return state

def should_coutinue(state: AgentState) -> AgentState:
    """Function to decide what to do next"""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"  # Continue looping
    else:
        return "exit" # Exit the loop


# greeting -> random -> random -> random -> random -> random -> END

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",
    should_coutinue,
    {
        "loop": "random",
        "exit": END
    }

)

graph.set_entry_point("greeting")
app = graph.compile()

graph_png = app.get_graph().draw_mermaid_png()
with open("graph4.png", "wb") as f:
    f.write(graph_png)


print(app.invoke({"name":"Prince", "number":[], "counter":-1}))