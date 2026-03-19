from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str 
    message: str


def compliment_node(state: AgentState) -> AgentState:
    """Simple node that adds a compliment message to the state"""

    name = state.get("name", "Friend")
    compliment = f"{name}, you are doing an amazing job learning about LangGraph! Keep up the great work!"
    return {"message": compliment, "name": name}

graph = StateGraph(AgentState)

graph.add_node("complimenter", compliment_node)

graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")

app = graph.compile()

# graph_png = app.get_graph().draw_mermaid_png()

# with open("graph.png", "wb") as f:
#     f.write(graph_png)

# print("Graph saved successfully as 'graph.png'")

result = app.invoke({"name": "Prince"})

print(result['message'])