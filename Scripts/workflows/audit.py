from ai.gemini import GeminiModel
from file_manager import SessionData
from workflows.base import Workflow
from workflows.feedback import FeedbackWorkflow
from workflows.gold import GoldWorkflow


class AuditWorkflow(Workflow):
    """Generates both the Feedback and Gold reports."""
    
    def execute(self, session: SessionData, model: GeminiModel) -> None:
        # Run Feedback
        FeedbackWorkflow().execute(session, model)
        # Run Gold
        GoldWorkflow().execute(session, model)
        print("Audit workflow completed: Feedback and Gold reports generated.")
