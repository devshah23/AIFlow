import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeConfig";
import type { WorkflowType } from "@/types/workflowTypes";
import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

const initialState: WorkflowType = {
  nodes: [
    {
      id: "1",
      type: INPUTNODE,
      data: { label: "Input Node" },
      position: { x: 250, y: 5 },
    },
    {
      id: "2",
      type: KNOWLEDGEBASENODE,
      data: { label: "Knowledge Base Node" },
      position: { x: 500, y: 100 },
    },
    {
      id: "3",
      type: LLMNODE,
      data: { label: "LLM Node" },
      position: { x: 400, y: 300 },
    },
    {
      id: "4",
      type: OUTPUTNODE,
      data: { label: "Output Node" },
      position: { x: 600, y: 300 },
    },
  ],
  edges: [
    // { id: "n1-n2", source: "1", target: "2" },
    // { id: "n1-n3", source: "2", target: "3" },
    // { id: "n1-n4", source: "1", target: "4" },
  ],
};

export const workflow = createSlice({
  name: "workflow",
  initialState,
  reducers: {
    setNodes: (state, action: PayloadAction<WorkflowType["nodes"]>) => {
      state.nodes = action.payload;
    },
    setEdges: (state, action: PayloadAction<WorkflowType["edges"]>) => {
      state.edges = action.payload;
    },
  },
});

export const { setNodes, setEdges } = workflow.actions;
export default workflow.reducer;
