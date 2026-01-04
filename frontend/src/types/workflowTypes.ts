import type { Edge } from "@xyflow/react";
import type { AllNodeType } from "./nodeDataTypes";

export type WorkflowType = {
  id: number;
  name: string;
  description?: string;
  nodes: AllNodeType[];
  edges: Edge[];
};
export type WorkflowDescType = {
  id: number;
  name: string;
  description?: string;
};

export type WorkflowResponseType = WorkflowType & {
  id: number;
};
