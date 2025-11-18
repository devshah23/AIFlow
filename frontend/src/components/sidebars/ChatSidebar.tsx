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
import { Button } from "../ui/button";
import React from "react";
import { useNavigate } from "react-router-dom";
import { BotIcon } from "lucide-react";

type ChatSidebarProps = {
  chatList: string[];
};

const ChatSidebar = React.memo(({ chatList }: ChatSidebarProps) => {
  const navigate = useNavigate();

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
                {chatList.map((item, index) => (
                  <SidebarMenuItem key={index}>
                    <SidebarMenuButton asChild>
                      <Button
                        onClick={() => navigate("/chat")}
                        className="w-full flex items-center justify-start gap-3 px-2 py-1.5 bg-transparent text-foreground rounded-md hover:bg-muted transition-all">
                        <BotIcon className="w-5 h-5 shrink-0" />
                        <span className="font-semibold truncate transition-all duration-200 group-data-[collapsible=icon]:hidden">
                          {item}
                        </span>
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
