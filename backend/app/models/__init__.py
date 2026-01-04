"""Package initializer for app.models.

Import each model module so that their SQLModel/SQLAlchemy Table objects
are registered on SQLModel.metadata when `import app.models` is executed.
This makes `metadata` populated for Alembic.
"""
from .workflow_nodes import WorkflowNodes
from .workflow_edges import WorkflowEdges
from .workflows import Workflows
from .chats import Chats
from .messages import Messages
from .file_metadata import FileMetadata

__all__ = [
    "WorkflowNodes",
    "WorkflowEdges",
    "Workflows",
    "Chats",
    "Messages",
    "FileMetadata",
]
