import { Label } from "@/components/ui/label";
import SimpleNodeLayout from "../nodeLayouts/SimpleNodeLayout";
import { BookTextIcon } from "lucide-react";
import { Input } from "@/components/ui/input";
import React, { useState } from "react";
import { type NodeProps } from "@xyflow/react";
import { useNodeChangeDataContext } from "@/contexts/nodeDataChangeContext";
import type {
  FileMetaDataType,
  KnowledgeBaseNodeType,
} from "@/types/nodeDataTypes";
import isEqual from "lodash.isequal";
import fileUploadService from "@/apis/fileUploadService";
import { toast } from "react-toastify";
import { Spinner } from "@/components/ui/spinner";

const KnowledgeBaseNode = React.memo(
  (nodeProps) => {
    console.log("KnowledgeBaseNode props:", nodeProps);
    const { handleNodeDataChange } = useNodeChangeDataContext();
    const [uploadLoading, setUploadLoading] = useState(false);
    const content = React.useMemo(
      () => (
        <>
          <SimpleNodeLayout
            title="Knowledge Base"
            icon={<BookTextIcon className="w-3 h-3" />}
            description="Let the LLM search info in your file">
            <Label htmlFor="files" className="text-xs font-medium mb-1">
              File for Knowledge Base
              {nodeProps.data && `: ${nodeProps.data.fileName}`}
              {uploadLoading && <Spinner />}
            </Label>
            <Input hidden id="metadata_id" value={nodeProps.data.metadataId} />
            <Input
              id="files"
              type="file"
              disabled={uploadLoading}
              onChange={async (e) => {
                const file = e.target.files?.[0]; // Get the first file
                if (!file) return;

                if (file.size > 5 * 1024 * 1024) {
                  toast.error("File is too large. Max limit is 5MB.");
                  e.target.value = "";
                  return;
                }

                setUploadLoading(true);
                const loadingToast = toast.loading("Uploading file...");

                try {
                  const response = await fileUploadService.uploadFile(file);

                  if (response && response.success) {
                    const { metadata_id, file_name } = response.data;

                    const metaData: FileMetaDataType = {
                      metadataId: metadata_id.toString(),
                      fileName: file_name,
                    };
                    console.log("Uploaded file metadata:", metaData);
                    handleNodeDataChange?.(
                      { id: e.target.id, value: metaData },
                      nodeProps.id
                    );

                    toast.update(loadingToast, {
                      render: "File uploaded successfully!",
                      type: "success",
                      isLoading: false,
                      autoClose: 1000,
                    });
                  } else {
                    throw new Error(
                      response?.message || "Upload failed on server."
                    );
                  }
                } catch (error: Error | any) {
                  console.error("File Upload Error:", error);

                  const errorMessage =
                    error?.response?.data?.message || "Error uploading file.";
                  toast.update(loadingToast, {
                    render: errorMessage,
                    type: "error",
                    isLoading: false,
                    autoClose: 2000,
                  });
                } finally {
                  setUploadLoading(false);
                  e.target.value = "";
                }
              }}
              className=" file:text-[12px] !text-[12px]"
            />
          </SimpleNodeLayout>
        </>
      ),
      [handleNodeDataChange, nodeProps.id, nodeProps.data, uploadLoading]
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
