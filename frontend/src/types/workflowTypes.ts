import type { Edge } from "@xyflow/react";
import type { AllNodeType } from "./nodeDataTypes";

export type WorkflowType = {
  name: string;
  description?: string;
  nodes: AllNodeType[];
  edges: Edge[];
};
