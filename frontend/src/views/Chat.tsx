import SidebarLayout from "@/components/layouts/SidebarLayout";
import ChatSidebar from "@/components/sidebars/ChatSidebar";
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ui/shadcn-io/ai/conversation";
import { Message, MessageContent } from "@/components/ui/shadcn-io/ai/message";
import {
  PromptInput,
  PromptInputModelSelect,
  PromptInputModelSelectContent,
  PromptInputModelSelectItem,
  PromptInputModelSelectTrigger,
  PromptInputModelSelectValue,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputToolbar,
} from "@/components/ui/shadcn-io/ai/prompt-input";
import { LLMModels } from "@/configs/LLMConfig";
import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";

const Chat = () => {
  const { id } = useParams();

  const [input, setInput] = useState("");
  const SelectChatComponent = useMemo(
    () => (
      <div className="h-[85dvh] w-full flex flex-col items-center justify-center bg-gradient-to-b from-white via-gray-50 to-gray-100 text-center px-6">
        <div className="flex flex-col items-center justify-center p-10 rounded-3xl border border-gray-200 shadow-lg shadow-gray-100 bg-white/70 backdrop-blur-sm max-w-md">
          {/* Icon */}
          <div className="mb-5 p-4 rounded-full bg-gradient-to-r from-gray-800 to-gray-500 text-white shadow-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.8}
              stroke="currentColor"
              className="w-8 h-8">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M7.5 8.25h9m-9 3h6m-9 6.75h12a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0018.75 4.5H5.25A2.25 2.25 0 003 6.75v9a2.25 2.25 0 002.25 2.25z"
              />
            </svg>
          </div>

          <h3 className="text-3xl font-bold bg-gradient-to-r from-gray-800 via-gray-600 to-gray-400 text-transparent bg-clip-text mb-2">
            No Chat Selected
          </h3>

          <p className="text-gray-500 text-sm mb-6 max-w-sm">
            Choose a conversation from the sidebar to start exploring workflows
            and chat details.
          </p>

          <div className="text-xs text-gray-400 italic">
            Tip: You can create or switch chats anytime from the sidebar.
          </div>
        </div>
      </div>
    ),
    []
  );

  return (
    <SidebarLayout
      navbar={
        <ChatSidebar
          chatList={["Visitor Details", "Coke Pricing", "WockPharma Earnings"]}
        />
      }>
      {!id ? (
        SelectChatComponent
      ) : (
        <div className="flex flex-col items-stretch justify-between sm:max-w-lg md:max-w-2xl lg:max-w-5xl max-w-[85vw] h-[85dvh] mx-auto">
          <Conversation className="flex-1 min-h-0 overflow-y-auto relative">
            <ConversationContent>
              <Message from={"assistant"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"assistant"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"assistant"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
              <Message from={"user"}>
                <MessageContent>Hi there!</MessageContent>
              </Message>
            </ConversationContent>
            <ConversationScrollButton />
          </Conversation>
          <PromptInput onSubmit={() => {}} className="max-w-full min-h-fit">
            <PromptInputTextarea
              value={input}
              rows={5}
              onChange={(e) => setInput(e.currentTarget.value)}
              placeholder="Type your query here..."
              className="align-text-bottom pb-1"
            />
            <PromptInputToolbar>
              <PromptInputModelSelect
                disabled
                onValueChange={(v) => {}}
                value={"gemini-2.5-pro"}>
                <PromptInputModelSelectTrigger>
                  <PromptInputModelSelectValue />
                </PromptInputModelSelectTrigger>
                <PromptInputModelSelectContent>
                  {LLMModels.map((model) => (
                    <PromptInputModelSelectItem
                      key={model.value}
                      value={model.value}>
                      {model.label}
                    </PromptInputModelSelectItem>
                  ))}
                </PromptInputModelSelectContent>
              </PromptInputModelSelect>
              <PromptInputSubmit disabled={!input.trim()} />
            </PromptInputToolbar>
          </PromptInput>
        </div>
      )}
    </SidebarLayout>
  );
};

export default Chat;
