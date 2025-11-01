import React from "react";
import { SidebarProvider } from "@/components/ui/sidebar";

interface SidebarLayoutProps {
  navbar: React.ReactNode;
  children: React.ReactNode;
}

const SidebarLayout = ({ children, navbar }: SidebarLayoutProps) => {
  return (
    <>
      <SidebarProvider defaultOpen={false}>
        {navbar}
        <div className="flex-1 ml-2 p-2 rounded-2xl border-2">{children}</div>
      </SidebarProvider>
    </>
  );
};

export default SidebarLayout;
