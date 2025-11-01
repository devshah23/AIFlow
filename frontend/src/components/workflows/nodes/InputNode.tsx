import { Textarea } from "@/components/ui/textarea";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { Label } from "@/components/ui/label";
import { FileInputIcon } from "lucide-react";
import React from "react";
import type { NodeProps } from "@xyflow/react";
import { useNodeChangeDataContext } from "@/contexts/nodeDataChangeContext";
import type { InputNodeDataType, InputNodeType } from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";

const InputNode = React.memo(
  (nodeProps) => {
    const nodeData = nodeProps.data as InputNodeDataType;
    console.log("InputNode", nodeProps.data);

    const { handleNodeDataChange } = useNodeChangeDataContext();
    return (
      <SimpleNodeLayout
        title="User Input"
        icon={<FileInputIcon className="w-3 h-3" />}
        description="Enter your query here.">
        <Label htmlFor="user-input" className="text-xs font-medium mb-1">
          Query
        </Label>
        <Textarea
          value={nodeData.query}
          placeholder="Write the query here."
          id="query"
          className="!text-[10px] !resize-none !max-h-[40px] scroll-auto"
          onChange={(e) => {
            handleNodeDataChange?.(
              { id: e.target.id, value: e.target.value },
              nodeProps.id
            );
          }}
        />
      </SimpleNodeLayout>
    );
  },
  (
    prevProps: NodeProps<InputNodeType>,
    nextProps: NodeProps<InputNodeType>
  ) => {
    return isEqual(prevProps.data, nextProps.data);
  }
);

export default InputNode;
