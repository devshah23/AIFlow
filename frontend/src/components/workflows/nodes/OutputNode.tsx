import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { CheckCircle2Icon } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";

const OutputNode = () => {
  return (
    <SimpleNodeLayout
      icon={<CheckCircle2Icon className="w-3 h-3" />}
      title="Output"
      description="Output will appear in this node">
      <Label htmlFor="output" className="text-xs font-medium mb-1">
        Output
      </Label>
      <Textarea
        placeholder="Output will appear here."
        id="output"
        className="!text-[10px] scroll-auto"
      />
    </SimpleNodeLayout>
  );
};

export default OutputNode;
