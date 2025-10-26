import SidebarLayout from "@/components/layouts/SidebarLayout";
import { CreateFlowSidebar } from "@/components/sidebars/CreateFlowSidebar";
import FlowLayout from "@/components/workflows/WorkFlowCanvas";

const CreateFlow = () => {
  return (
    <>
      <SidebarLayout navbar={<CreateFlowSidebar />}>
        <FlowLayout />
      </SidebarLayout>
    </>
  );
};

export default CreateFlow;
