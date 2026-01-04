import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import workflowService from "@/apis/workflowService";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import React, { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BotIcon, PlusIcon, WorkflowIcon } from "lucide-react";
import type { WorkflowDescType } from "@/types/workflowTypes";
import chatService from "@/apis/chatService";
import { toast } from "react-toastify";
import { Spinner } from "../ui/spinner";
import { Badge } from "../ui/badge";

type ChatListProps = {
  id: number;
  name: string;
  workflowId: number;
}[];

const ChatSidebar = React.memo(() => {
  const navigate = useNavigate();
  const [openNewChatModal, setNewChatModal] = useState(false);
  const [chatList, setChatList] = useState<ChatListProps>([]);
  const fetchChatList = useCallback(async () => {
    try {
      const response = await chatService.getChats();
      if (response.success) {
        setChatList(response.data);
      }
    } catch {
      toast.error("Error fetching chat list");
    }
  }, []);
  useEffect(() => {
    fetchChatList();
  }, [fetchChatList]);

  return (
    <div className="relative ">
      <Sidebar
        collapsible="icon"
        className="group rounded-r-xl overflow-hidden">
        <SidebarContent className="rounded-r-xl overflow-hidden">
          <SidebarGroup>
            <SidebarGroupLabel>
              <h4 className="w-full text-lg font-bold my-2">
                <span>Chats</span>
              </h4>
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                <SidebarMenuItem>
                  <SidebarMenuButton asChild>
                    <Dialog
                      open={openNewChatModal}
                      onOpenChange={setNewChatModal}>
                      <DialogTrigger asChild>
                        <Button
                          onClick={() => setNewChatModal(true)}
                          className="w-full flex items-center justify-start gap-3 px-2 py-1.5 bg-transparent text-foreground rounded-md hover:bg-muted transition-all">
                          <PlusIcon className="w-5 h-5 shrink-0" />
                          <span className="font-semibold truncate transition-all duration-200 group-data-[collapsible=icon]:hidden">
                            {" "}
                            New Chat
                          </span>
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <AddChatModal refetchChats={fetchChatList} />
                      </DialogContent>
                    </Dialog>
                  </SidebarMenuButton>
                </SidebarMenuItem>

                {chatList.map((item) => (
                  <SidebarMenuItem key={item.id}>
                    <SidebarMenuButton asChild>
                      <Button
                        onClick={() => navigate(`/chat/${item.id}`)}
                        className="w-full flex items-center justify-start gap-3 px-2 py-1.5 bg-transparent text-foreground rounded-md hover:bg-muted transition-all">
                        <BotIcon className="w-5 h-5 shrink-0" />
                        <div className="flex-1 flex justify-between">
                          <span className="font-semibold truncate transition-all duration-200 group-data-[collapsible=icon]:hidden">
                            {item.name}
                          </span>
                          <Badge variant="outline">
                            <WorkflowIcon /> {item.workflowId}
                          </Badge>
                        </div>
                      </Button>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
      </Sidebar>
      <SidebarTrigger className="absolute top-4 right-0 -mr-9 p-2 z-50 " />
    </div>
  );
});
export default ChatSidebar;

const AddChatModal = ({ refetchChats }: { refetchChats: () => void }) => {
  const [workflows, setWorkflows] = useState<WorkflowDescType[]>([]);
  const [createChatLoading, setCreateChatLoading] = useState(false);
  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const response = await workflowService.getAllWorkflows();
        setWorkflows(response.data);
      } catch (error) {
        console.error("Error fetching workflows:", error);
      }
    };
    fetchWorkflows();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setCreateChatLoading(true);
    try {
      const formData = new FormData(e.currentTarget);
      const name = formData.get("name") as string;
      const workflowId = formData.get("workflow") as string;
      console.log({ name, workflowId });
      if (!name) {
        toast.error("Please enter name");
        setCreateChatLoading(false);
        return;
      }
      if (!workflowId) {
        toast.error("Please select a workflow");
        setCreateChatLoading(false);
        return;
      }

      const response = await chatService.newChat(Number(workflowId), name);
      if (response.success) {
        toast.success("Chat created successfully");
        refetchChats();
      }
    } catch {
      toast.error("Error creating chat");
    } finally {
      setCreateChatLoading(false);
    }
  };

  return (
    <>
      <DialogHeader>
        <DialogTitle>Add a new chat</DialogTitle>
        <DialogDescription>
          Start a new conversation with a fresh chat.
        </DialogDescription>
      </DialogHeader>
      <form onSubmit={handleSubmit}>
        <div className="grid gap-4">
          <div className="grid gap-3">
            <Label htmlFor="name">Name</Label>
            <Input id="name" name="name" placeholder="Chat of Workflow 1" />
          </div>
          <div className="grid gap-3">
            <Label htmlFor="workflow">Workflow</Label>
            <Select name="workflow">
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select a workflow" />
              </SelectTrigger>
              <SelectContent>
                {workflows.map((workflow) => (
                  <SelectItem
                    value={workflow.id.toString()}
                    key={workflow.id}
                    className="w-full flex justify-between">
                    <span>{workflow.id}</span>
                    <span>{workflow.name}</span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
        <DialogFooter>
          <Button type="submit">
            {createChatLoading && <Spinner />}
            Create Chat
          </Button>
        </DialogFooter>
      </form>
    </>
  );
};
