import { Textarea } from "@/components/ui/textarea";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { Label } from "@/components/ui/label";
import { FileInputIcon } from "lucide-react";

const InputNode = () => {
  return (
    <SimpleNodeLayout
      title="User Input"
      icon={<FileInputIcon className="w-3 h-3" />}
      description="Enter your query here.">
      <Label htmlFor="user-input" className="text-xs font-medium mb-1">
        Query
      </Label>
      <Textarea
        placeholder="Write the query here."
        id="user-input"
        className="!text-[10px] !resize-none !max-h-[40px] scroll-auto"
      />
    </SimpleNodeLayout>
  );
};

export default InputNode;
