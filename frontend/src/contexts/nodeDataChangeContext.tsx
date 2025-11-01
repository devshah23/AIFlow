import type { FileMetaDataType } from "@/types/nodeDataTypes";
import { createContext, useContext } from "react";

export const NodeDataChangeContext = createContext<{
  handleNodeDataChange?: (
    changedData: { id: string; value: string | number | FileMetaDataType[] },
    nodeId: string
  ) => void;
}>({});

export const useNodeChangeDataContext = () => useContext(NodeDataChangeContext);
