from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
    operation: str

def process_values(state: AgentState) -> AgentState:
    # """This function handles multiple different inputs"""
    # print(state)

    # state["result"] = f"Hi there {state['name']}! Your sum = {sum(state["values"])}"

    # print(state)
    name = state.get("name")
    values = state.get("values", [])
    op = state.get("operation")

    if op == "sum":
        state["result"] = f"Your sum = {sum(values)}"
    elif op == "product":
        product = 1
        for v in values:
            product *= v
            
        state["result"] = f"Your product = {product}"
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

# graph_png = app.get_graph().draw_mermaid_png()
# with open("graph1.png", "wb") as f:
#     f.write(graph_png)

# print("Graph saved successfully as 'graph1.png'")

ans_sum = app.invoke({"name": "Prince", "values": [1,2,3,4,5], "operation": "sum"})
ans_prod = app.invoke({"name": "Prince", "values": [1,2,3,4,5], "operation": "product"})

print(ans_sum['result'])
print(ans_prod['result'])