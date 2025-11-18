"""Package initializer for app.models.

Import each model module so that their SQLModel/SQLAlchemy Table objects
are registered on SQLModel.metadata when `import app.models` is executed.
This makes `metadata` populated for Alembic.
"""
from .workflow_nodes import *
from .workflow_edges import *
from .workflows import *
from .chats import *
from .messages import *

__all__ = [
    "WorkflowNodes",
    "WorkflowEdges",
    "Workflows",
    "Chats",
    "Messages",
]
