import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Eye, Workflow, Plus, Trash2Icon } from "lucide-react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import workflowService from "@/apis/workflowService";
import { useCallback, useEffect, useState } from "react";
import { toast } from "react-toastify";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTrigger,
  DialogFooter,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { DialogClose } from "@radix-ui/react-dialog";
import { Spinner } from "@/components/ui/spinner";

const Home = () => {
  const navigate = useNavigate();
  const [openCreateModal, setOpenCreateModal] = useState(false);
  const [deletingWorkflowId, setDeletingWorkflowId] = useState<string | null>(
    null
  );
  const [workflowList, setWorkflowList] = useState<
    Array<{ id: string; name: string; description: string }>
  >([]);
  const fetchWorkflowList = useCallback(async () => {
    try {
      const response = await workflowService.getAllWorkflows();

      if (!response?.success || !Array.isArray(response.data)) {
        throw new Error(response?.message || "Failed to fetch workflows");
      }

      setWorkflowList(
        response.data.map(
          (wf: { id: number; name: string; description?: string }) => ({
            id: String(wf.id),
            name: wf.name,
            description: wf.description?.trim() || "No description",
          })
        )
      );
    } catch (error) {
      console.error("Error fetching workflows:", error);
      toast.error("Failed to fetch workflows. Please try again.");
    }
  }, []);

  useEffect(() => {
    fetchWorkflowList();
  }, [fetchWorkflowList]);

  const navigateToWorkflow = (id: string) => {
    navigate(`/create/${id}`);
    console.log(`Navigating to workflow with id: ${id}`);
  };

  const deleteWorkflow = async (id: string) => {
    if (!id) {
      toast.error("Invalid workflow ID");
      return;
    }
    setDeletingWorkflowId(id);
    try {
      const response = await workflowService.deleteWorkflow(Number(id));

      if (!response?.success) {
        throw new Error(response?.message || "Failed to delete workflow");
      }

      toast.success("Workflow deleted successfully");
      await fetchWorkflowList();
    } catch (error) {
      console.error("Error deleting workflow:", error);
      toast.error("Failed to delete workflow. Please try again.");
    }
    setDeletingWorkflowId(null);
  };

  const createNewWorkflow = async (name: string, description: string) => {
    if (!name.trim()) {
      toast.error("Workflow name is required");
      return;
    }

    try {
      const response = await workflowService.createWorkflow({
        name: name.trim(),
        description: description?.trim() || "",
        nodes: [],
        edges: [],
      });

      if (!response?.success || !response.data) {
        throw new Error(response?.message || "Failed to create workflow");
      }

      // Avoid stale state by using functional update
      setWorkflowList((prev) => [
        ...prev,
        {
          id: String(response.data.id),
          name: response.data.name,
          description: response.data.description || "No description",
        },
      ]);

      toast.success("Workflow created successfully");
      setOpenCreateModal(false);
    } catch (error) {
      console.error("Error creating workflow:", error);
      toast.error("Failed to create workflow. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white via-gray-50 to-gray-100 text-gray-900 px-10 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 rounded-xl  bg-white px-5 py-2">
        <div>
          <div className="relative inline-flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-violet-500 animate-pulse" />

            <h2 className="text-3xl font-extrabold tracking-tight text-slate-900 relative">
              Workflows
              <span className="absolute -bottom-2 left-0 h-2 w-full rounded-full bg-violet-200/50 blur-md" />
            </h2>
          </div>

          <p className="mt-1 text-sm text-slate-600">
            Create, execute, and observe workflow runs
          </p>
        </div>

        {/* Right: Primary Action */}
        <Dialog open={openCreateModal} onOpenChange={setOpenCreateModal}>
          <DialogTrigger asChild>
            <Button className="flex items-center gap-2 rounded-md bg-violet-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition-all hover:bg-violet-700 focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-2">
              <Plus size={16} />
              New workflow
            </Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-md">
            <CreateWorkflowModal createWorkflowHandler={createNewWorkflow} />
          </DialogContent>
        </Dialog>
      </div>

      <Separator className="my-4" />

      {/* Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {workflowList.map((wf, index) => (
          <motion.div
            key={wf.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}>
            <WorkflowCard
              id={wf.id}
              name={wf.name}
              description={wf.description}
              navigateToWorkflow={navigateToWorkflow}
              deleteWorkflow={deleteWorkflow}
              deleteWorkflowId={deletingWorkflowId}
            />
          </motion.div>
        ))}
      </div>
    </div>
  );
};

interface WorkflowCardProps {
  id: string;
  name: string;
  description: string;
  navigateToWorkflow: (id: string) => void;
  deleteWorkflow: (id: string) => void;
  deleteWorkflowId: string | null;
}

const WorkflowCard = ({
  id,
  name,
  description,
  navigateToWorkflow,
  deleteWorkflow,
  deleteWorkflowId,
}: WorkflowCardProps) => {
  return (
    <Card className="group relative rounded-xl border border-slate-200 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-violet-300 hover:shadow-sm">
      <div className="p-5">
        <div className="flex items-center justify-between mb-3">
          {/* Left group */}
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-100 text-slate-600 ring-1 ring-slate-200">
              <Workflow size={16} />
            </div>

            <CardTitle className="truncate text-sm font-medium text-slate-900">
              {name}
            </CardTitle>
          </div>

          <span className="shrink-0 text-[11px] font-mono text-slate-400">
            #{id}
          </span>
        </div>

        <CardDescription className="text-sm text-slate-600 leading-relaxed mb-4 line-clamp-2">
          {description}
        </CardDescription>

        <Separator className="my-4 bg-slate-100" />

        <CardFooter className="flex justify-end gap-2 p-0">
          <Button
            onClick={() => deleteWorkflow(id)}
            variant="outline"
            className="h-8 w-8 p-0  hover:text-red-600 hover:bg-red-50 border-red-400">
            {deleteWorkflowId === id ? (
              <Spinner className="h-4 w-4 text-red-400" />
            ) : (
              <Trash2Icon size={16} className="text-red-400" />
            )}
          </Button>

          <Button
            onClick={() => navigateToWorkflow(id)}
            variant="outline"
            className="h-8 px-3 py-4 text-sm font-medium text-violet-600 hover:text-violet-700 hover:bg-violet-50 border-violet-300 ">
            <Eye size={16} className="mr-1" />
            Open
          </Button>
        </CardFooter>
      </div>
    </Card>
  );
};

const CreateWorkflowModal = ({
  createWorkflowHandler,
}: {
  createWorkflowHandler: (name: string, description: string) => void;
}) => {
  const [loading, setLoading] = useState(false);
  const createWorkflow = () => {
    let error = false;
    setLoading(true);
    const nameInput = (document.getElementById("name") as HTMLInputElement)
      .value;
    const descriptionInput = (
      document.getElementById("description") as HTMLInputElement
    ).value;
    if (!nameInput) {
      toast.error("Name is required");
      error = true;
    }
    if (!descriptionInput) {
      toast.error("Description is required");
      error = true;
    }

    if (error) {
      setLoading(false);
      return;
    }
    createWorkflowHandler(nameInput, descriptionInput);
    setLoading(false);
  };

  return (
    <>
      <DialogHeader>
        <DialogTitle>Create Workflow</DialogTitle>
        <DialogDescription>
          Automate the tasks you hate doing.
        </DialogDescription>
      </DialogHeader>
      <form
        className="w-full"
        onSubmit={(e) => {
          e.preventDefault();
          createWorkflow();
        }}>
        <div className="flex flex-col justify-center gap-2">
          <div className="block flex-1 gap-2">
            <Label htmlFor="name" className="mb-2">
              Name
            </Label>
            <Input id="name" placeholder="Name" className="w-full" />
          </div>
          <div className="block flex-1 gap-2 ">
            <Label htmlFor="name" className="mb-2">
              Description
            </Label>
            <Textarea
              id="description"
              placeholder="Write a short description about this workflow"
              className="w-full"
            />
          </div>
        </div>
        <DialogFooter className="justify-end mt-8">
          <DialogClose asChild>
            <Button type="button" variant="outline" className="bg-gray-50">
              Cancel
            </Button>
          </DialogClose>
          <Button
            type="submit"
            variant="secondary"
            className="bg-green-600 text-white"
            disabled={loading}>
            {loading && <Spinner />}
            Create
          </Button>
        </DialogFooter>
      </form>
    </>
  );
};

export default Home;
