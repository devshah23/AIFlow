import { DefaultLLMModel } from "@/configs/LLMConfig";
import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeTypeConfig";
import type {
  AllNodeDataType,
  AllNodeType,
  NodeTypeMap,
} from "@/types/nodeDataTypes";
import type { XYPosition } from "@xyflow/react";

export function createNode<T extends keyof NodeTypeMap>(
  nodeType: T,
  id: string,
  position: XYPosition = { x: 25, y: 5 }
): AllNodeType {
  const defaultData = getDefaultNodeData(nodeType);
  const newNode = {
    id,
    position,
    type: nodeType,
    data: defaultData,
  } as AllNodeType;
  return newNode;
}

function getDefaultNodeData<T extends keyof NodeTypeMap>(
  nodeType: T
): NodeTypeMap[T] {
  switch (nodeType) {
    case INPUTNODE:
      return { query: "" } as NodeTypeMap[T];
    case LLMNODE:
      return {
        model: DefaultLLMModel,
        apiKey: "",
        temperature: 0.3,
        prompt: "",
      } as NodeTypeMap[T];
    case KNOWLEDGEBASENODE:
      return { files: [] } as unknown as NodeTypeMap[T];
    case OUTPUTNODE:
      return { result: "" } as NodeTypeMap[T];
    default:
      throw new Error(`Unknown node type: ${nodeType}`);
  }
}

export function getStatesFromNodes(node: {
  id: string;
  type: keyof NodeTypeMap;
  data: any;
}): AllNodeDataType {
  switch (node.type) {
    case INPUTNODE:
      return {
        id: node.id,
        nodeType: INPUTNODE,
        data: node.data as NodeTypeMap[typeof INPUTNODE],
      };
    case LLMNODE:
      return {
        id: node.id,
        nodeType: LLMNODE,
        data: node.data as NodeTypeMap[typeof LLMNODE],
      };
    case KNOWLEDGEBASENODE:
      return {
        id: node.id,
        nodeType: KNOWLEDGEBASENODE,
        data: node.data as NodeTypeMap[typeof KNOWLEDGEBASENODE],
      };
    case OUTPUTNODE:
      return {
        id: node.id,
        nodeType: OUTPUTNODE,
        data: node.data as NodeTypeMap[typeof OUTPUTNODE],
      };
    default:
      throw new Error(`Unknown node type: ${node.type}`);
  }
}
