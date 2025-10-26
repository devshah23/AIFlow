import { SparklesIcon } from "lucide-react";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { LLMModels } from "@/configs/LLMConfig";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const LLMNode = () => {
  return (
    <>
      <SimpleNodeLayout
        title="LLM (Gemini)"
        icon={<SparklesIcon className="w-3 h-3" />}
        description="Run a query with Gemini LLM">
        <div className="flex flex-col gap-2">
          <Select defaultValue={LLMModels[0].value}>
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
            <Label html-for="api-key" className="text-xs font-medium mb-1">
              API Key
            </Label>
            <Input
              id="api-key"
              placeholder="Gemini API Key"
              type="password"
              className=" !text-[12px]"
            />
          </div>
          <div>
            <Label html-for="temperature" className="text-xs font-medium mb-1">
              Temperature
            </Label>
            <Input
              id="temperature"
              type="number"
              max={1}
              min={0}
              step={0.1}
              className="!text-[12px]"
            />
          </div>
          <div>
            <Label htmlFor="user-prompt" className="text-xs font-medium mb-1">
              Prompt
            </Label>
            <Textarea
              placeholder="Write the prompt here."
              id="user-prompt"
              className="!text-[10px] !resize-none !max-h-[40px] scroll-auto"
            />
          </div>
        </div>
      </SimpleNodeLayout>
    </>
  );
};

export default LLMNode;
