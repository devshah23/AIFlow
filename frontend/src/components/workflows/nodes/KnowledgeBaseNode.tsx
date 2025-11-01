import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { BookTextIcon } from "lucide-react";
import { Input } from "@/components/ui/input";
import React from "react";
import { type NodeProps } from "@xyflow/react";
import { useNodeChangeDataContext } from "@/contexts/nodeDataChangeContext";
import type {
  FileMetaDataType,
  KnowledgeBaseNodeType,
} from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";

const KnowledgeBaseNode = React.memo(
  (nodeProps) => {
    console.log("KnowledgeBaseNode props:", nodeProps);
    const { handleNodeDataChange } = useNodeChangeDataContext();
    const content = React.useMemo(
      () => (
        <>
          <SimpleNodeLayout
            title="Knowledge Base"
            icon={<BookTextIcon className="w-3 h-3" />}
            description="Let the LLM search info in your file">
            <Label htmlFor="files" className="text-xs font-medium mb-1">
              File for Knowledge Base
              {nodeProps.data.files.length != 0 &&
                `: ${nodeProps.data.files[0].fileName}`}
            </Label>
            <Input
              id="files"
              multiple
              type="file"
              onChange={(e) => {
                const files = e.target.files ? Array.from(e.target.files) : [];
                // store file to backend write fn here.Then store the metadata in node data
                const dummyMetaData: FileMetaDataType[] = [
                  {
                    fileId: "1",
                    fileName: files[0].name,
                    fileSize: files[0].size.toString(),
                    fileType: files[0].type,
                    uploadedUrl: "abvd",
                    uploadedAt: new Date().toISOString(),
                  },
                ];
                handleNodeDataChange?.(
                  { id: e.target.id, value: dummyMetaData },
                  nodeProps.id
                );
                e.target.value = "";
              }}
              className=" file:text-[12px] !text-[12px]"
            />
          </SimpleNodeLayout>
        </>
      ),
      [handleNodeDataChange, nodeProps.id, nodeProps.data.files]
    );
    return content;
  },
  (
    prevProps: NodeProps<KnowledgeBaseNodeType>,
    nextProps: NodeProps<KnowledgeBaseNodeType>
  ) => {
    return isEqual(prevProps.data, nextProps.data);
  }
);

export default KnowledgeBaseNode;
