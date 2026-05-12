from langgraph.graph import StateGraph

def process_node(state):
    query = state["query"]
    context = state["retriever"](query)

    if not context:
        state["escalate"] = True
        return state

    answer = context
    if not answer:
        state["escalate"] = True
        return state

    state["answer"] = answer
    state["escalate"] = False
    return state

def output_node(state):
    if state["escalate"]:
        state["answer"] = state["hitl"](state["query"])
    return state

def build_graph():
    graph = StateGraph(dict)
    graph.add_node("process", process_node)
    graph.add_node("output", output_node)
    graph.set_entry_point("process")
    graph.add_edge("process", "output")
    return graph.compile()
