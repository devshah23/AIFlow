import type { Node } from "@xyflow/react";
import type {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "../configs/NodeTypeConfig";

export type NodeData<T extends string, U extends object> = {
  id: string;
  nodeType: T;
  data: U;
};

export interface NodeTypeMap {
  [INPUTNODE]: InputNodeDataType;
  [LLMNODE]: LMMNodeDataType;
  [KNOWLEDGEBASENODE]: KnowledgeBaseDataType;
  [OUTPUTNODE]: OutputNodeDataType;
}

export type AllNodeDataType = {
  [K in keyof NodeTypeMap]: NodeData<K, NodeTypeMap[K]>;
}[keyof NodeTypeMap];

export type InputNodeDataType = {
  query: string;
};

// export type InputNodeType = NodeData<INPUTNODE, InputNodeDataType>;

export type LMMNodeDataType = {
  model: string;
  apiKey: string;
  temperature: number;
  prompt: string;
};

// export type LLMNodeType = NodeData<LLMNODE, LMMNodeDataType>;
export type FileMetaDataType = {
  fileId: string;
  fileName: string;
  fileSize: string;
  fileType: string;
  uploadedUrl: string;
  uploadedAt: string;
};
export type KnowledgeBaseDataType = { files: FileMetaDataType[] };

// export type KnowledgeBaseType = NodeData<
//   KNOWLEDGEBASENODE,
//   KnowledgeBaseDataType
// >;

export type OutputNodeDataType = {
  result: string;
};
// export type OutputNodeType = NodeData<OUTPUTNODE, OutputNodeDataType>;

export type InputNodeType = Node<InputNodeDataType, INPUTNODE>;
export type LLMNodeType = Node<LMMNodeDataType, LLMNODE>;
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
