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
  useSidebar,
} from "@/components/ui/sidebar";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { NodeCreateOptionsListType } from "@/configs/WorkflowNodesConfig";
import { Button } from "../ui/button";
import React from "react";
import type { NODE_TYPES } from "@/configs/NodeTypeConfig";

type CreateFlowSidebarProps = {
  nodeOptionsList: NodeCreateOptionsListType;
  addNodesHandler: (nodeType: NODE_TYPES) => void;
};

const CreateFlowSidebar = React.memo(
  ({ nodeOptionsList, addNodesHandler }: CreateFlowSidebarProps) => {
    const { state } = useSidebar();
    const isCollapsed = state === "collapsed";

    return (
      <div className="relative ">
        <Sidebar
          collapsible="icon"
          className="group rounded-r-xl overflow-hidden">
          <SidebarContent className="rounded-r-xl overflow-hidden">
            <SidebarGroup>
              <SidebarGroupLabel>
                <h4 className="w-full text-lg font-bold my-2">
                  <span>Node Components</span>
                </h4>
              </SidebarGroupLabel>
              <SidebarGroupContent>
                <SidebarMenu>
                  {nodeOptionsList.map((item) => (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton asChild>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              onClick={() =>
                                addNodesHandler(item.nodeCreateType)
                              }
                              className="w-full flex items-center justify-start gap-3 px-2 py-1.5 bg-transparent text-foreground rounded-md hover:bg-muted transition-all">
                              <item.icon className="w-5 h-5 shrink-0" />
                              <span className="font-semibold truncate transition-all duration-200 group-data-[collapsible=icon]:hidden">
                                {item.title}
                              </span>
                            </Button>
                          </TooltipTrigger>
                          {isCollapsed && (
                            <TooltipContent side="right">
                              Add {item.title}
                            </TooltipContent>
                          )}
                        </Tooltip>
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
  }
);
export default CreateFlowSidebar;
