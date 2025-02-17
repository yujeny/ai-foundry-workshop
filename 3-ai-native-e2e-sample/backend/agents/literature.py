from azure.ai.projects.models import AgentEventHandler, MessageDeltaChunk, ThreadMessage, ThreadRun, RunStep
from typing import Any, Generator, Dict, Union
import logging

logger = logging.getLogger(__name__)

class LiteratureChatHandler(AgentEventHandler):
    """Event handler for streaming literature chat responses."""
    
    def on_message_delta(self, delta: MessageDeltaChunk) -> Generator[Union[str, Dict[str, Any]], None, None]:
        """Handle streaming message chunks."""
        if delta.text:
            logger.debug(f"Received message delta: {delta.text[:100]}...")
            yield delta.text

    def on_thread_message(self, message: ThreadMessage) -> Generator[Dict[str, Any], None, None]:
        """Handle complete thread messages."""
        if message.content:
            logger.info(f"Received thread message: {message.id}")
            yield message.content[0].as_dict()
        else:
            logger.warning(f"Received empty thread message: {message.id}")

    def on_thread_run(self, run: ThreadRun) -> None:
        """Handle thread run status updates."""
        logger.info(f"Thread run status: {run.status}")

    def on_run_step(self, step: RunStep) -> None:
        """Handle individual run steps."""
        logger.info(f"Run step type: {step.type}, Status: {step.status}")

    def on_error(self, data: str) -> Generator[Dict[str, Any], None, None]:
        """Handle error events."""
        error_msg = f"Error in literature chat: {data}"
        logger.error(error_msg)
        yield {"error": error_msg}

    def on_done(self) -> Generator[Dict[str, Any], None, None]:
        """Handle stream completion."""
        logger.info("Literature chat stream completed")
        yield {"done": True}

    def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        """Handle any unrecognized events."""
        logger.warning(f"Unhandled event type: {event_type}, Data: {event_data}")
