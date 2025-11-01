import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { CheckCircle2Icon } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import React from "react";
import type { NodeProps } from "@xyflow/react";
import type { OutputNodeDataType, OutputNodeType } from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";

const OutputNode = React.memo(
  (nodeProps) => {
    const nodeStateData = nodeProps.data as OutputNodeDataType;
    return (
      <SimpleNodeLayout
        icon={<CheckCircle2Icon className="w-3 h-3" />}
        title="Output"
        description="Output will appear in this node">
        <Label htmlFor="result" className="text-xs font-medium mb-1">
          Output
        </Label>
        <Textarea
          value={nodeStateData.result || ""}
          placeholder="Output will appear here."
          id="result"
          className="!text-[10px] scroll-auto"
        />
      </SimpleNodeLayout>
    );
  },
  (
    prevProps: NodeProps<OutputNodeType>,
    nextProps: NodeProps<OutputNodeType>
  ) => {
    return isEqual(prevProps.data, nextProps.data);
  }
);

export default OutputNode;
