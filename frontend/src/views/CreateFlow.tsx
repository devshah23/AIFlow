import workflowService from "@/apis/workflowService";
import SidebarLayout from "@/components/layouts/SidebarLayout";
import CreateFlowSidebar from "@/components/sidebars/CreateFlowSidebar";
import WorkflowCanvas from "@/components/workflows/WorkFlowCanvas";
import {
  INPUTNODE,
  OUTPUTNODE,
  type NODE_TYPES,
} from "@/configs/NodeTypeConfig";
import { NodeCreateOptionsList } from "@/configs/WorkflowNodesConfig";
import { NodeDataChangeContext } from "@/contexts/nodeDataChangeContext";
import { createNode } from "@/factories/NodeStateFactory";
import { setWorkflow } from "@/store/slices/workflowSlice";
import type { RootState } from "@/store/store";
import type { AllNodeType, FileMetaDataType } from "@/types/nodeDataTypes";

import { useEdgesState, useNodesState } from "@xyflow/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { useBlocker } from "react-router-dom";
import isEqual from "lodash.isequal";
import {
  Dialog,
  DialogDescription,
  DialogHeader,
  DialogContent,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const CreateFlow = () => {
  const { id: workflowId } = useParams();
  const [showConfirmModel, setShowConfirmModal] = useState(false);
  const dispatch = useDispatch();
  const blocker = useBlocker(({ currentLocation, nextLocation }) => {
    const areNodesEqual = () => {
      if (nodes.length !== savedNodes.length) {
        return false;
      }
      for (let i = 0; i < nodes.length; i++) {
        if (
          !isEqual(nodes[i].data, savedNodes[i].data) ||
          nodes[i].type !== savedNodes[i].type ||
          nodes[i].position.x !== savedNodes[i].position.x ||
          nodes[i].position.y !== savedNodes[i].position.y
        ) {
          return false;
        }
      }
      return true;
    };

    return (
      !areNodesEqual() ||
      (!isEqual(edges, savedEdges) &&
        currentLocation.pathname !== nextLocation.pathname)
    );
  });

  useEffect(() => {
    if (blocker.state === "blocked") {
      setShowConfirmModal(true);
    }
  }, [blocker.state]);

  const handleCancelNavigation = () => {
    blocker.reset();
    setShowConfirmModal(false);
  };

  useEffect(() => {
    const fetchWorkflowData = async () => {
      if (!workflowId) {
        toast.error("Invalid workflow ID");
        return;
      }

      try {
        const response = await workflowService.getWorkflowById(
          Number(workflowId)
        );

        if (!response?.success || !response.data) {
          throw new Error(response?.message || "Failed to fetch workflow data");
        }

        dispatch(setWorkflow(response.data));
      } catch (error) {
        console.error("Error fetching workflow:", error);
        toast.error("Failed to fetch workflow data. Please try again.");
      }
    };

    fetchWorkflowData();
  }, [workflowId, dispatch]);

  const { nodes: savedNodes, edges: savedEdges } = useSelector(
    (state: RootState) => state.workflow
  );

  const [nodes, setNodesLocal, onNodesChange] =
    useNodesState<AllNodeType>(savedNodes);
  const [edges, setEdgesLocal, onEdgesChange] = useEdgesState(savedEdges);

  // Is nodesLocal required in dependecny
  useEffect(() => {
    setNodesLocal(savedNodes);
    setEdgesLocal(savedEdges);
  }, [savedNodes, savedEdges, setNodesLocal, setEdgesLocal]);
  const addNodesToWF = useCallback(
    (nodeType: NODE_TYPES) => {
      setNodesLocal((prevNodes) => {
        if (
          nodeType === INPUTNODE &&
          prevNodes.some((n) => n.type === INPUTNODE)
        ) {
          toast.error("Only one Input Node is allowed");
          return prevNodes;
        }

        if (
          nodeType === OUTPUTNODE &&
          prevNodes.some((n) => n.type === OUTPUTNODE)
        ) {
          toast.error("Only one Output Node is allowed");
          return prevNodes;
        }
        const newNode = createNode(nodeType, (prevNodes.length + 1).toString());

        return [...prevNodes, newNode];
      });
    },
    [setNodesLocal]
  );

  function updateNodeData<T extends AllNodeType>(
    node: T,
    changedData: { id: string; value: string | number | FileMetaDataType }
  ): T {

    // if changed data is file metadata, we need to handle it differently
    if (
      typeof changedData.value === "object" &&
      "metadataId" in changedData.value
    ) {
      
      return {
        ...node,
        data: {
          ...node.data,
          fileName: (changedData.value as FileMetaDataType).fileName,
          metadataId: (changedData.value as FileMetaDataType).metadataId,
        },
      };
    }

    return {
      ...node,
      data: {
        ...node.data,
        [changedData.id]: changedData.value,
      },
    };
  }
  const handleNodeDataChange = useCallback(
    (
      changedData: { id: string; value: string | number | FileMetaDataType },
      nodeId: string
    ) => {
      setNodesLocal((nds) => {
        return nds.map((n) =>
          n.id === nodeId ? updateNodeData(n, changedData) : n
        );
      });
    },
    [setNodesLocal]
  );
  const nodeDataChangeContextValue = useMemo(
    () => ({ handleNodeDataChange }),
    [handleNodeDataChange]
  );

  return (
    <>
      <SidebarLayout
        navbar={
          <CreateFlowSidebar
            nodeOptionsList={NodeCreateOptionsList}
            addNodesHandler={addNodesToWF}
          />
        }>
        <NodeDataChangeContext.Provider value={nodeDataChangeContextValue}>
          <Dialog
            open={showConfirmModel}
            onOpenChange={(open) => {
              if (!open) {
                blocker.reset();
              }
              setShowConfirmModal(open);
            }}>
            <DialogContent>
              <ConfirmNavigationModal onCancel={handleCancelNavigation} />
            </DialogContent>
          </Dialog>
          <WorkflowCanvas
            nodes={nodes}
            edges={edges}
            setNodes={setNodesLocal}
            setEdges={setEdgesLocal}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            handleNodeDataChange={handleNodeDataChange}
          />
        </NodeDataChangeContext.Provider>
      </SidebarLayout>
    </>
  );
};

const ConfirmNavigationModal = ({ onCancel }: { onCancel: () => void }) => {
  return (
    <>
      <DialogHeader>
        <DialogTitle>Unsaved Changes</DialogTitle>
        <DialogDescription>
          You have unsaved changes in your workflow. Please save them.
        </DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button onClick={onCancel} variant={"destructive"}>
          Close
        </Button>
      </DialogFooter>
    </>
  );
};

export default CreateFlow;
