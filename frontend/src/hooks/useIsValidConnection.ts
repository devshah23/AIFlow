import { useCallback, useRef } from "react";
import type { Connection, Edge } from "@xyflow/react";
import { toast } from "react-toastify";
import { OUTPUTNODE } from "@/configs/NodeTypeConfig";
import type { AllNodeType } from "@/types/nodeDataTypes";

const useIsValidConnection = (nodes: AllNodeType[], edges: Edge[]) => {
  const lastInvalidRef = useRef<string | null>(null);
  const toastTimeoutRef = useRef<null | number>(null);

  const nodeCycleAbsent = useCallback(function checkCycle(
    source: string,
    target: string,
    edges: Edge[]
  ) {
    const visited = new Set();
    visited.add(source);
    visited.add(target);

    function dfs(node: string) {
      const nextNodes = edges
        .filter((e) => e.source === node)
        .map((e) => e.target);
      for (const n of nextNodes) {
        if (!visited.has(n)) {
          visited.add(n);
          return dfs(n);
        } else {
          return false;
        }
      }
      return true;
    }

    return dfs(target);
  },
  []);
  const showNewMessage = (message: string, key: string) => {
    if (lastInvalidRef.current !== key) {
      lastInvalidRef.current = key;
      if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current);
      toastTimeoutRef.current = setTimeout(() => {
        toast.error(message, {
          autoClose: 600,
        });
      }, 10);
    }
  };

  const isValidConnection = useCallback(
    (connection: Connection | Edge) => {
      const { source, target } = connection;
      const key = `${source}->${target}`;
      if (source === target) {
        showNewMessage("Node cannot connect to itself", key);
        return false;
      }

      const sourceNode = nodes.find((n) => n.id === source);
      const targetNode = nodes.find((n) => n.id === target);
      if (!sourceNode || !targetNode) return false;

      if (sourceNode.type === OUTPUTNODE) {
        showNewMessage("OutputNode cannot be source", key);
        return false;
      }

      const valid = nodeCycleAbsent(source, target, edges);
      if (!valid) {
        showNewMessage("Cycle is not allowed", key);
        return false;
      }

      lastInvalidRef.current = null;
      return true;
    },
    [nodes, edges, nodeCycleAbsent]
  );

  return isValidConnection;
};

export default useIsValidConnection;
