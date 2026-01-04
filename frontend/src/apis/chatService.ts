import fetch, { type ApiResponse } from "./fetchService";

export type Message = {
  id: number;
  chatId: number;
  fromEntity: "user" | "assistant";
  content: string;
};

type ChatServiceType = {
  newChat: (workflowId: number, name: string) => Promise<ApiResponse<null>>;
  getChats: () => Promise<
    ApiResponse<
      {
        id: number;
        name: string;
        workflowId: number;
      }[]
    >
  >;
  getChat: (chatId: number) => Promise<
    ApiResponse<{
      chat: {
        id: number;
        name: string;
        workflowId: number;
        description: string;
      };
      messageDetails: {
        messages: Message[];
        nextCursor: number | null;
        totalMessages: number;
        hasMore: boolean;
      };
    }>
  >;
  getMessages: (
    chatId: number,
    cursor?: number,
    limit?: number
  ) => Promise<
    ApiResponse<{
      messages: Message[];
      nextCursor: number | null;
      totalMessages: number;
      hasMore: boolean;
    }>
  >;
  runWorkflow: (
    chatId: number,
    data: { message: string }
  ) => Promise<ApiResponse<{ userMessage: Message; workflowMessage: Message }>>;
};

const chatService: ChatServiceType = {
  newChat: (workflowId: number, name: string) => {
    return fetch({
      url: `/chat/create`,
      method: "post",
      data: { name, workflowId },
    });
  },
  getChats: async () => {
    return fetch({
      url: `/chat/all`,
      method: "get",
    });
  },
  getChat: (chatId: number) => {
    return fetch({
      url: `/chat/${chatId}`,
      method: "get",
    });
  },
  getMessages: (chatId: number, cursor?: number, limit: number = 20) => {
    return fetch({
      url: `/chat/messages/${chatId}`,
      method: "get",
      params: { cursor, limit },
    });
  },
  runWorkflow: (chatId: number, data: { message: string }) => {
    return fetch({
      url: `/chat/run/${chatId}`,
      method: "post",
      data: data,
    });
  },
};
export default chatService;
