from langgraph.graph import StateGraph, END
from app.graph.state import ResearchState
from app.graph.nodes.supervisor import supervisor_node
from app.graph.nodes.report_writer import report_writer_node
from app.graph.nodes.pdf_agent import pdf_agent_node
from app.graph.nodes.web_agent import web_agent_node

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("pdf_agent", pdf_agent_node)
    graph.add_node("web_agent", web_agent_node)
    graph.add_node("report_writer", report_writer_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "pdf_agent")
    graph.add_edge("supervisor", "web_agent")
    graph.add_edge("pdf_agent", "report_writer")
    graph.add_edge("web_agent", "report_writer")
    graph.add_edge("report_writer", END)

    return graph.compile()

research_graph = build_graph()