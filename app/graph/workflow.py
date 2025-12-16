from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import call_model, run_tools

# --- FUNCIÓN DE DECISIÓN PROPIA ---
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tools"
    return "__end__"

def create_graph():
    # 1. Se inicializa el Grafo con el Estado Tipado
    workflow = StateGraph(AgentState)

    # 2. Se añaden los Nodos
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", run_tools)

    # 3. Se definine el Punto de Entrada, se ejecuta primero call_model
    workflow.set_entry_point("agent")

    # 4. Se defininen las Aristas condicionales
    # tools_condition mira el último mensaje del LLM y decide:
    # Pidió una tool?
    # O solo texto?
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": END
        }
    )

    # 5. Después de ejecutar una tool, siempre volvemos al LLM, vuelve a pensar
    workflow.add_edge("tools", "agent")

    # 6. Se valida el grafo, lo optimiza y lo deja listo para ejecutar
    return workflow.compile()

# Se crea un solo grafo, reutilizable, sin estado interno
app_graph = create_graph()