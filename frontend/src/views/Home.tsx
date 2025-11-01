// import { Button } from "@/components/ui/button";
// import {
//   Card,
//   CardDescription,
//   CardFooter,
//   CardHeader,
//   CardTitle,
// } from "@/components/ui/card";
// import { Separator } from "@/components/ui/separator";
// import { Eye } from "lucide-react";

// const Home = () => {
//   const workflowList = [
//     {
//       id: "a",
//       name: "ABC",
//       description: "ads lkjfds fjl slk fjslfj",
//     },
//     {
//       id: "c",
//       name: "ABC",
//       description: "ads lkjfds fjl slk fjslfj",
//     },
//     {
//       id: "b",
//       name: "ABC",
//       description: "ads lkjfds fjl slk fjslfj",
//     },
//   ];
//   return (
//     <>
//       <div>
//         <h2 className="text-4xl font-bold">Workflows</h2>
//       </div>
//       <Separator className="my-4" />
//       <div className="flex flex-wrap gap-7">
//         {workflowList.map((wf) => (
//           <WorkflowCard
//             id={wf.id}
//             name={wf.name}
//             description={wf.description}
//           />
//         ))}
//       </div>
//     </>
//   );
// };

// interface WorkflowCardProps {
//   id: string;
//   name: string;
//   description: string;
// }

// const WorkflowCard = (props: WorkflowCardProps) => {
//   return (
//     <>
//       <Card className="min-w-48 p-2.5">
//         <CardHeader>
//           <CardTitle className="text-lg ml-1.5">{props.name}</CardTitle>
//           <Separator className="my-1.5" />
//           <CardDescription className="text-sm ml-1.5">
//             {props.description}
//           </CardDescription>
//         </CardHeader>
//         <CardFooter className="flex justify-end mt-8">
//           <Button
//             variant="outline"
//             className="flex items-center justify-center gap-4 hover:cursor-pointer">
//             View <Eye />
//           </Button>
//         </CardFooter>
//       </Card>
//     </>
//   );
// };

// export default Home;

import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Eye, Workflow, Plus } from "lucide-react";
import { motion } from "framer-motion";

const Home = () => {
  const workflowList = [
    {
      id: "a",
      name: "Customer Onboarding Flow",
      description: "Automates welcome emails and CRM updates.",
    },
    {
      id: "b",
      name: "Payment Processing Flow",
      description: "Handles transactions and sends confirmation alerts.",
    },
    {
      id: "c",
      name: "Feedback Collection Flow",
      description: "Collects user feedback and updates dashboards.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white via-gray-50 to-gray-100 text-gray-900 px-10 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-gray-800 via-gray-600 to-gray-100 text-transparent bg-clip-text">
            Workflows
          </h2>
          <p className="text-gray-500 text-sm mt-1">
            Manage and monitor your workflows effortlessly.
          </p>
        </div>

        <Button
          variant="default"
          className="bg-gradient-to-r from-gray-800 to-gray-400 hover:opacity-90 text-white flex items-center gap-2 px-4 py-2 shadow-md shadow-gray-200 transition-all">
          <Plus size={18} /> New Workflow
        </Button>
      </div>

      <Separator className="my-6" />

      {/* Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
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
}

const WorkflowCard = ({ id, name, description }: WorkflowCardProps) => {
  return (
    <Card className="relative group border border-gray-200 rounded-2xl overflow-hidden bg-white shadow-sm hover:shadow-lg transition-all duration-300 hover:scale-[1.02] hover:border-none hover:bg-gradient-to-br from-gray-800 via-gray-200 to-gray-400">
      {/* Subtle gradient border glow */}
      <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-300 bg-gradient-to-r from-gray-400 via-gray-300 to-gray-200 blur-sm"></div>

      {/* Card Content */}
      <div className="relative z-10 p-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-2 rounded-xl text-gray-700">
            <Workflow size={18} />
          </div>
          <CardTitle className="text-lg font-semibold text-gray-900 group-hover:text-gray-800 transition-colors">
            {name}
          </CardTitle>
        </div>
        <CardDescription className="text-sm text-gray-600 mt-1 mb-4">
          {description}
        </CardDescription>

        <Separator className="my-3" />

        <CardFooter className="flex justify-end">
          <Button
            variant="outline"
            className="flex items-center justify-center gap-2 border-gray-300 text-gray-700 group-hover:bg-gray-100 hover:bg-gradient-to-r hover:from-gray-800 hover:to-gray-600 hover:text-white hover:border-transparent transition-all">
            <Eye size={16} /> View
          </Button>
        </CardFooter>
      </div>
    </Card>
  );
};

export default Home;
