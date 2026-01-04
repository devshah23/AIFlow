import chatService, {
  type Message as MessageResponse,
} from "@/apis/chatService";
import SidebarLayout from "@/components/layouts/SidebarLayout";
import ChatSidebar from "@/components/sidebars/ChatSidebar";
import ReactMarkdown from "react-markdown";
import {
  Conversation,
  ConversationContent,
} from "@/components/ui/shadcn-io/ai/conversation";
import { Message, MessageContent } from "@/components/ui/shadcn-io/ai/message";
import {
  PromptInput,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputToolbar,
} from "@/components/ui/shadcn-io/ai/prompt-input";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import remarkGfm from "remark-gfm";
import { Spinner } from "@/components/ui/spinner";

const Chat = () => {
  const { id } = useParams();
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [input, setInput] = useState("");
  const [hasMoreMessages, setHasMoreMessages] = useState(false);
  const [processing, setProcessing] = useState<"ready" | "submitted">("ready");
  const lastMessageRefId = useRef<number>(0);
  const [messagesLoading, setMessagesLoading] = useState(false);

  const [cursor, setCursor] = useState<number | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const fetchChatData = useCallback(async () => {
    try {
      if (id) {
        setMessagesLoading(true);
        const response = await chatService.getChat(Number(id));
        if (response.success) {
          const messageList = response.data.messageDetails.messages || [];
          setMessages(messageList);
          setHasMoreMessages(response.data.messageDetails.hasMore || false);
          setCursor(response.data.messageDetails.nextCursor || null);
        } else {
          throw Error("Not able to fetch messages");
        }
      }
    } catch {
      toast.error("Can't fetch messages for the chat");
    }
    setMessagesLoading(false);
  }, [id]);

  const fetchMoreMessages = useCallback(async () => {
    try {
      setMessagesLoading(true);
      if (id) {
        const response = await chatService.getMessages(
          Number(id),
          Number(cursor)
        );
        if (response.success) {
          setMessages((prevMessages) => [
            ...(response.data.messages || []),
            ...prevMessages,
          ]);
          setHasMoreMessages(response.data.hasMore || false);
          setCursor(response.data.nextCursor || null);
        } else {
          throw Error("Not able to fetch more messages");
        }
      }
    } catch {
      toast.error("Can't fetch more messages for the chat");
    }
    setMessagesLoading(false);
  }, [id, cursor]);
  const runWorkflow = useCallback(async () => {
    try {
      setProcessing("submitted");
      const response = await chatService.runWorkflow(Number(id), {
        message: input,
      });

      if (response.success) {
        const newMessages = response.data;
        setMessages((prevMessages) => {
          const filteredMessages = prevMessages.filter((msg) => msg.id !== -1);
          return [
            ...filteredMessages,
            newMessages.userMessage,
            newMessages.workflowMessage,
          ];
        });
      } else {
        toast.error("Failed to execute workflow.");
      }
    } catch {
      toast.error("An error occurred while running the workflow.");
    }
    setProcessing("ready");
  }, [id, input]);

  const handleSend = () => {
    if (!input.trim()) {
      toast.warning("Please enter a query.");
      return;
    }

    const userMessage: {
      id: number;
      fromEntity: "user" | "assistant";
      content: string;
      chatId: number;
    } = {
      id: -1,
      fromEntity: "user",
      content: input,
      chatId: Number(id),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setInput("");

    runWorkflow();
  };

  useEffect(() => {
    fetchChatData();
    // const el = scrollRef.current;
    // if (!el) return;
    // requestAnimationFrame(() => {
    //   el.scrollTop = el.scrollHeight;
    // });
  }, [id, fetchChatData]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el || !hasMoreMessages) return;

    let debounceTimer: number | null = null;

    const onScroll = () => {
      if (el.scrollTop < 25 && hasMoreMessages) {
        if (debounceTimer) return;

        debounceTimer = setTimeout(async () => {
          const prevHeight = el.scrollHeight;

          await fetchMoreMessages();

          requestAnimationFrame(() => {
            el.scrollTop = el.scrollHeight - prevHeight;
          });

          debounceTimer = null;
        }, 200);
      }
    };

    el.addEventListener("scroll", onScroll);
    return () => {
      el.removeEventListener("scroll", onScroll);
      if (debounceTimer) clearTimeout(debounceTimer);
    };
  }, [fetchMoreMessages, hasMoreMessages]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    console.log("Messages Length:", messages.length);
    const lastMsgId = lastMessageRefId.current;
    if (messages.length === 0 || messages[messages.length - 1].id === lastMsgId)
      return;
    // Scroll for first time instant bottom.
    if (lastMessageRefId.current === 0) {
      requestAnimationFrame(() => {
        el.scrollTop = el.scrollHeight;
      });
    }

    lastMessageRefId.current = messages[messages.length - 1].id;
    // Scroll for new and other message modification smooth behavior
    el.scrollTo({
      top: el.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

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
            Choose a conversation from the sidebar to start exploring workflows.
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
    <>
      <SidebarLayout navbar={<ChatSidebar />}>
        {!id ? (
          SelectChatComponent
        ) : (
          <div className="flex flex-col items-stretch justify-between sm:max-w-lg md:max-w-2xl lg:max-w-5xl max-w-[85vw] h-[85dvh] mx-auto">
            <div
              ref={scrollRef}
              className="flex-1 min-h-0 overflow-y-auto relative">
              {messagesLoading && (
                <div className="absolute top-2 left-1/2 -translate-x-1/2 z-10">
                  <Spinner className="w-6 h-6 text-primary" />
                </div>
              )}
              <Conversation>
                <ConversationContent>
                  {messages.map((msg) => (
                    <Message key={msg.id} from={msg.fromEntity}>
                      <MessageContent>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      </MessageContent>
                    </Message>
                  ))}
                </ConversationContent>
              </Conversation>
            </div>
            <PromptInput
              className="max-w-full min-h-fit flex mt-3"
              onSubmit={(e) => {
                e.preventDefault();
                if (!input.trim()) return;
                handleSend();
              }}>
              <PromptInputTextarea
                value={input}
                rows={5}
                placeholder="Type your query here..."
                className="align-text-bottom pb-1 flex-1"
                onChange={(e) => setInput(e.currentTarget.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    (e.currentTarget.form as HTMLFormElement)?.requestSubmit();
                  }
                }}
              />

              <PromptInputToolbar>
                <PromptInputSubmit
                  status={processing}
                  type="submit"
                  disabled={!input.trim() || processing === "submitted"}
                />
              </PromptInputToolbar>
            </PromptInput>
          </div>
        )}
      </SidebarLayout>
    </>
  );
};
export default Chat;
