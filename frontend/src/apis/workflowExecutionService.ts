import fetch, { type ApiResponse } from "./fetchService";

type WorkflowExecutionServiceType = {
  executeWorkflow: (
    workflowId: number,
    inputQuery: string
  ) => Promise<ApiResponse<{ output: string }>>;
};

const workflowExecutionService: WorkflowExecutionServiceType = {
  executeWorkflow: (workflowId: number, inputQuery: string) => {
    return fetch({
      url: `/run/${workflowId}`,
      method: "post",
      data: { query: inputQuery },
    });
  },
};
export default workflowExecutionService;
