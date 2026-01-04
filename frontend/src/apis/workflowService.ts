import type {
  WorkflowDescType,
  WorkflowResponseType,
  WorkflowType,
} from "@/types/workflowTypes";
import fetch, { type ApiResponse } from "./fetchService";
type WorkflowServiceType = {
  getAllWorkflows: () => Promise<ApiResponse<WorkflowDescType[]>>;
  getWorkflowById: (
    workflowId: number
  ) => Promise<ApiResponse<WorkflowResponseType>>;
  createWorkflow: (data: {
    name: string;
    description: string;
    nodes: WorkflowType["nodes"];
    edges: WorkflowType["edges"];
  }) => Promise<ApiResponse<WorkflowResponseType>>;
  updateWorkflow: (
    workflowId: number,
    data: WorkflowType
  ) => Promise<ApiResponse<WorkflowResponseType>>;
  deleteWorkflow: (workflowId: number) => Promise<ApiResponse<null>>;
};

const workflowService: WorkflowServiceType = {} as WorkflowServiceType;
const baseURL = "/workflow";

workflowService.getAllWorkflows = () => {
  return fetch({
    url: `${baseURL}/all`,
    method: "get",
  });
};
workflowService.getWorkflowById = (workflowId) => {
  return fetch({
    url: `${baseURL}/${workflowId}`,
    method: "get",
  });
};
workflowService.createWorkflow = (data) => {
  return fetch({
    url: `${baseURL}`,
    method: "post",
    data,
  });
};

workflowService.updateWorkflow = (workflowId, data) => {
  return fetch({
    url: `${baseURL}/${workflowId}`,
    method: "put",
    data,
  });
};

workflowService.deleteWorkflow = (workflowId) => {
  return fetch({
    url: `${baseURL}/${workflowId}`,
    method: "delete",
  });
};

export default workflowService;
