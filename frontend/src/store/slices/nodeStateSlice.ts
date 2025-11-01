import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
} from "@/configs/NodeTypeConfig";
import type { AllNodeDataType } from "@/types/nodeDataTypes";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const initialState: AllNodeDataType[] = [
  { id: "1", data: { query: "" }, nodeType: INPUTNODE },
  { id: "2", data: { files: [] }, nodeType: KNOWLEDGEBASENODE },
  {
    id: "3",
    data: { model: "", apiKey: "", temperature: 0, prompt: "" },
    nodeType: LLMNODE,
  },
  { id: "4", data: { result: "" }, nodeType: OUTPUTNODE },
];

export const nodeStatesSlice = createSlice({
  name: "nodeStates",
  initialState,
  reducers: {
    addNodeState: (state, action: PayloadAction<AllNodeDataType>) => {
      state.push(action.payload);
    },
    updateNodeState: (state, action: PayloadAction<AllNodeDataType>) => {
      const index = state.findIndex((node) => node.id === action.payload.id);
      if (index !== -1) {
        state[index] = action.payload;
      }
    },
    removeNodeState: (state, action: PayloadAction<string>) => {
      return state.filter((node) => node.id !== action.payload);
    },
    setNodesState: (_, action: PayloadAction<AllNodeDataType[]>) => {
      console.log("The new node states is", action.payload);
      return action.payload;
    },
  },
});

export const { addNodeState, updateNodeState, removeNodeState, setNodesState } =
  nodeStatesSlice.actions;

export default nodeStatesSlice.reducer;
