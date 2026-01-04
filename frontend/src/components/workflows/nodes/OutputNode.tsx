import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { CheckCircle2Icon, Maximize2Icon } from "lucide-react";
import React from "react";
import type { NodeProps } from "@xyflow/react";
import type { OutputNodeDataType, OutputNodeType } from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";
import remarkGfm from "remark-gfm";
import ReactMarkdown from "react-markdown";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

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
        <div className="relative border rounded-md p-2 bg-muted text-[10px] max-h-32 overflow-auto">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {nodeStateData.result || "Output will appear here"}
          </ReactMarkdown>

          {/* Expand Button */}
          <Dialog>
            <DialogTrigger asChild>
              <button className="absolute top-1 right-1 p-1 rounded hover:bg-muted-foreground/10">
                <Maximize2Icon className="w-3 h-3" />
              </button>
            </DialogTrigger>

            <DialogContent className="max-w-5xl h-[50vh] overflow-hidden">
              <DialogHeader>
                <DialogTitle>Workflow Output</DialogTitle>
              </DialogHeader>

              <div className="overflow-auto h-full p-4 prose dark:prose-invert max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {nodeStateData.result}
                </ReactMarkdown>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </SimpleNodeLayout>
    );
  },
  (
    prevProps: NodeProps<OutputNodeType>,
    nextProps: NodeProps<OutputNodeType>
  ) => {
    console.log("Comparing OutputNode props:", prevProps.data, nextProps.data);
    return isEqual(prevProps.data, nextProps.data);
  }
);

export default OutputNode;
