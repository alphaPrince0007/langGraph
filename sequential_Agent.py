from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    values: List[str]
    final: str

def first_node(state: AgentState) -> AgentState:
    """This is the first node of our sequence"""

    state["final"] = f"Hi {state['name']} "
    return state

def second_node(state: AgentState) -> AgentState:
    """This is the second node of our sequence"""

    state["final"] += f"You are {state['age']} years old "
    return state

def third_node(state: AgentState) -> AgentState:
    """This is the third node of our sequence"""
    values = state.get("values", [])
    skills_str = ", ".join(values)
    state["final"] += f"and your skills are: {skills_str}"
    return state

graph = StateGraph(AgentState)

graph.add_node("first", first_node)
graph.add_node("second", second_node)
graph.add_node("third", third_node)

graph.set_entry_point("first")
graph.add_edge("first", "second")
graph.add_edge("second", "third")
graph.set_finish_point("third")

app = graph.compile()

# graph_png = app.get_graph().draw_mermaid_png()
# with open("graph3.png", "wb") as f:
#     f.write(graph_png)


result = app.invoke({
    'name':'Prince',
    'age': '24',
    'values': ['JavaScript', 'Python', 'Java', 'C++']
})
print(result['final'])