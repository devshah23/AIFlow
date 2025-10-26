import { Card, CardContent, CardFooter } from "@/components/ui/card";
import NodeHeader from "../nodes/nodeComponents/NodeHeader";
import { Handle, Position } from "@xyflow/react";

import { memo } from "react";

interface SimpleNodeLayoutProps {
  title: string;
  icon: React.ReactNode;
  description: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

const SimpleNodeLayout = memo(
  ({ children, ...props }: SimpleNodeLayoutProps) => {
    return (
      <>
        <Handle
          type="source"
          position={Position.Right}
          isConnectableStart={true}
          isConnectableEnd={false}
        />
        <Handle
          type="target"
          position={Position.Left}
          isConnectableStart={false}
          isConnectableEnd={true}
        />

        <Card className="h-full w-full max-w-40 bg-card rounded-md border-border shadow-none">
          <NodeHeader
            icon={props.icon}
            title={props.title}
            description={props.description}
          />
          <CardContent className="px-2">{children}</CardContent>
          <CardFooter>{props.footer}</CardFooter>
        </Card>
      </>
    );
  }
);

export default SimpleNodeLayout;
