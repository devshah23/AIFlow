import { CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import React from "react";

interface NodeHeaderProps {
  title: string;
  icon: React.ReactNode;
  description: string;
}

const NodeHeader = (props: NodeHeaderProps) => {
  return (
    <>
      <CardHeader className="gap-0">
        <CardTitle className="flex gap-2 items-center text-xs font-bold border-b-2 px-2 py-1">
          {props.icon}
          {props.title}
        </CardTitle>
        <CardDescription className="bg-blue-300 text-left text-accent-foreground font-medium text-[10px] border-blue-300 px-2 py-1">
          {props.description}
        </CardDescription>
      </CardHeader>
    </>
  );
};

export default NodeHeader;
