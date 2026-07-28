from app.config import settings
from app.graph.state import ResearchState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

MAX_REVISIONS = 3

class ReviewDecision(BaseModel):
    decision: str = Field(description='Either "approve" or "revise"')
    feedback: str = Field(description="Specific, actionable feedback if revising, or a brief note if approving")


def reviewer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    draft_report = state.get("draft_report", "")
    merged_knowledge = state.get("merged_knowledge", "")
    revision_count = state.get("revision_count", 0)

    if revision_count >= MAX_REVISIONS:
        print(f"[reviewer] revision cap ({MAX_REVISIONS}) reached, approving as-is")
        return {
            "review_feedback": f"Approved after reaching the max of {MAX_REVISIONS} revision attempts.",
            "review_decision": "approve",
        }

    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.0)
    structured_llm = llm.with_structured_output(ReviewDecision)

    result: ReviewDecision = structured_llm.invoke(
        [
            SystemMessage(content=""),
            HumanMessage(
                content=(
                    f"Research goal:\n{goal}\n\n"
                    f"Findings available to the writer:\n{merged_knowledge}\n\n"
                    f"Draft report:\n{draft_report}"
                )
            ),
        ]
    )

    print(f"[reviewer] decision: {result.decision}")

    update: ResearchState = {"review_feedback": result.feedback, "review_decision": result.decision}
    if result.decision == "revise":
        update["revision_count"] = revision_count + 1

    return update