from abc import ABC, abstractmethod

from app.services.workflow_runner.context import WfExecutionContext


class NodeExecutor(ABC):

    def __init__(self, node):
        self.node = node
    
    @abstractmethod
    async def execute(self, context:WfExecutionContext,upstream_nodes:list[int]) -> dict:
        pass