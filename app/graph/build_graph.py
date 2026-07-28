from langgraph.graph import StateGraph, END
from app.graph.state import ResearchState
from app.graph.nodes.supervisor import supervisor_node
from app.graph.nodes.report_writer import report_writer_node
from app.graph.nodes.pdf_agent import pdf_agent_node
from app.graph.nodes.web_agent import web_agent_node
from app.graph.nodes.data_agent import data_agent_node
from app.graph.nodes.knowledge_merger import knowledge_merger_node
from app.graph.nodes.fact_checker import fact_checker_node

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("pdf_agent", pdf_agent_node)
    graph.add_node("web_agent", web_agent_node)
    graph.add_node("data_agent", data_agent_node)
    graph.add_node("knowledge_merger", knowledge_merger_node)
    graph.add_node("fact_checker", fact_checker_node)
    graph.add_node("report_writer", report_writer_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "pdf_agent")
    graph.add_edge("supervisor", "web_agent")
    graph.add_edge("supervisor", "data_agent")
    graph.add_edge("pdf_agent", "knowledge_merger")
    graph.add_edge("web_agent", "knowledge_merger")
    graph.add_edge("data_agent", "knowledge_merger")
    graph.add_edge("knowledge_merger", "fact_checker")
    graph.add_edge("fact_checker", "report_writer")
    graph.add_edge("report_writer", END)

    return graph.compile()

research_graph = build_graph()