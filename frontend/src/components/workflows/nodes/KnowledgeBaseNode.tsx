import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { BookTextIcon } from "lucide-react";
import { Input } from "@/components/ui/input";

const KnowledgeBaseNode = () => {
  return (
    <>
      <SimpleNodeLayout
        title="Knowledge Base"
        icon={<BookTextIcon className="w-3 h-3" />}
        description="Let the LLM search info in your file">
        <Label htmlFor="user-file" className="text-xs font-medium mb-1">
          File for Knowledge Base
        </Label>
        <Input
          id="user-file"
          type="file"
          className=" file:text-[12px] !text-[12px]"
        />
      </SimpleNodeLayout>
    </>
  );
};

export default KnowledgeBaseNode;
