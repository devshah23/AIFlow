import { SparklesIcon } from "lucide-react";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DefaultLLMModel, LLMModels } from "@/configs/LLMConfig";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import React from "react";
import type { NodeProps } from "@xyflow/react";
import { useNodeChangeDataContext } from "@/contexts/nodeDataChangeContext";
import type { LLMNodeType } from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";

const LLMNode = React.memo(
  (nodeProps) => {
    const nodeStateData = nodeProps.data;
    console.log("Rendering LLMNode with data:", nodeStateData);

    const { handleNodeDataChange } = useNodeChangeDataContext();
    const content = React.useMemo(
      () => (
        <>
          <SimpleNodeLayout
            title="LLM (Gemini)"
            icon={<SparklesIcon className="w-3 h-3" />}
            description="Run a query with Gemini LLM">
            <div className="flex flex-col gap-2">
              <Select
                defaultValue={DefaultLLMModel}
                value={nodeStateData.model}
                onValueChange={(value) => {
                  handleNodeDataChange?.({ id: "model", value }, nodeProps.id);
                }}>
                <SelectTrigger className="w-full text-[10px]/6 py-1 font-semibold">
                  <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent>
                  {LLMModels.map((data) => (
                    <SelectItem
                      key={data.value}
                      value={data.value}
                      className="text-[10px] font-semibold">
                      {data.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <div>
                <Label html-for="apiKey" className="text-xs font-medium mb-1">
                  API Key
                </Label>
                <Input
                  id="apiKey"
                  value={nodeStateData.apiKey}
                  placeholder="Gemini API Key"
                  type="password"
                  className="nodrag !text-[12px]"
                  onChange={(e) => {
                    handleNodeDataChange?.(
                      { id: e.target.id, value: e.target.value },
                      nodeProps.id
                    );
                  }}
                />
              </div>
              <div>
                <Label
                  html-for="temperature"
                  className="text-xs font-medium mb-1">
                  Temperature
                </Label>
                <Input
                  id="temperature"
                  type="number"
                  value={nodeStateData.temperature}
                  max={1}
                  min={0}
                  step={0.05}
                  className="!text-[12px] appearance-none [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  onChange={(e) => {
                    const value = parseFloat(e.target.value);
                    console.log("Temperature value:", value);

                    if (isNaN(value) || (value <= 1 && value >= 0)) {
                      handleNodeDataChange?.(
                        { id: e.target.id, value: value },
                        nodeProps.id
                      );
                    }
                  }}
                />
              </div>
              <div>
                <Label htmlFor="prompt" className="text-xs font-medium mb-1">
                  Task Instruction
                </Label>
                <Textarea
                  placeholder="Write the task instruction here."
                  id="prompt"
                  value={nodeStateData.prompt}
                  className="!text-[10px] !resize-none !max-h-[40px] scroll-auto"
                  onChange={(e) => {
                    handleNodeDataChange?.(
                      { id: e.target.id, value: e.target.value },
                      nodeProps.id
                    );
                  }}
                />
              </div>
            </div>
          </SimpleNodeLayout>
        </>
      ),
      [nodeProps.id, handleNodeDataChange, nodeStateData]
    );
    return content;
  },
  (prevProps: NodeProps<LLMNodeType>, nextProps: NodeProps<LLMNodeType>) => {
    return isEqual(prevProps.data, nextProps.data);
  }
);

export default LLMNode;
