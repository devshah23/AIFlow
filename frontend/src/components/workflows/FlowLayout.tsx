import React from "react";
import { Background, Controls, MiniMap, ReactFlow } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const FlowLayout = () => {
  return (
    <div className="h-full w-full">
      <ReactFlow fitView>
        <Controls />
        <MiniMap />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default FlowLayout;
