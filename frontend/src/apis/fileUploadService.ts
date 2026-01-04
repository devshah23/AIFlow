import fetch, { type ApiResponse } from "./fetchService";

type fileUploadServiceType = {
  uploadFile: (file: File) => Promise<ApiResponse<UploadKBFileResponse>>;
};

const fileUploadService: fileUploadServiceType = {
  uploadFile: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch({
      url: "/upload_kb_file",
      method: "post",
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export type UploadKBFileResponse = {
  metadata_id: number;
  file_name: string;
};
export default fileUploadService;
