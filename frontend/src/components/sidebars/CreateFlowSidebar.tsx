import {
  FileInputIcon,
  CheckCircle2,
  LucideBookText,
  SparklesIcon,
} from "lucide-react";
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
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Link } from "react-router-dom";

const items = [
  {
    title: "Input Component",
    url: "#",
    icon: FileInputIcon,
  },
  {
    title: "Knowledge Base",
    url: "#",
    icon: LucideBookText,
  },
  {
    title: "LLM Component",
    url: "#",
    icon: SparklesIcon,
  },
  {
    title: "Output Component",
    url: "#",
    icon: CheckCircle2,
  },
];

export function CreateFlowSidebar() {
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
                {items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild>
                      <Tooltip>
                        <Link
                          to={item.url}
                          className="flex items-center gap-3 px-2 py-1.5 rounded-md hover:bg-muted transition-all">
                          <TooltipTrigger asChild>
                            <item.icon className="w-5 h-5 shrink-0" />
                          </TooltipTrigger>
                          <span className="font-semibold truncate transition-all duration-200 group-data-[collapsible=icon]:hidden">
                            {item.title}
                          </span>
                        </Link>
                        <TooltipContent side="right">
                          {item.title}
                        </TooltipContent>
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
