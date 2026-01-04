import type { Node } from "@xyflow/react";
import type {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "../configs/NodeTypeConfig";

export interface NodeTypeMap {
  [INPUTNODE]: InputNodeDataType;
  [LLMNODE]: LLMNodeDataType;
  [KNOWLEDGEBASENODE]: KnowledgeBaseDataType;
  [OUTPUTNODE]: OutputNodeDataType;
}

export type AllNodeDataType = {
  [K in keyof NodeTypeMap]: NodeTypeMap[K];
}[keyof NodeTypeMap];

export type InputNodeDataType = {
  query: string;
};

export type LLMNodeDataType = {
  model: string;
  apiKey: string;
  temperature: number;
  prompt: string;
};

export type FileMetaDataType = {
  metadataId?: string;
  fileName: string;
};
export type KnowledgeBaseDataType = FileMetaDataType;

export type OutputNodeDataType = {
  result: string;
};

export type InputNodeType = Node<InputNodeDataType, INPUTNODE>;
export type LLMNodeType = Node<LLMNodeDataType, LLMNODE>;
export type KnowledgeBaseNodeType = Node<
  KnowledgeBaseDataType,
  KNOWLEDGEBASENODE
>;
export type OutputNodeType = Node<OutputNodeDataType, OUTPUTNODE>;

export type AllNodeType =
  | InputNodeType
  | LLMNodeType
  | KnowledgeBaseNodeType
  | OutputNodeType;
