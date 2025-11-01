import {
  CheckCircle2,
  FileInputIcon,
  LucideBookText,
  SparklesIcon,
} from "lucide-react";
import {
  INPUTNODE,
  KNOWLEDGEBASENODE,
  LLMNODE,
  OUTPUTNODE,
  type NODE_TYPES,
} from "./NodeTypeConfig";

export type NodeCreateOptionsListType = {
  title: string;
  icon: React.FC<React.SVGProps<SVGSVGElement>>;
  nodeCreateType: NODE_TYPES;
}[];

export const NodeCreateOptionsList: NodeCreateOptionsListType = [
  {
    title: "Input Component",
    icon: FileInputIcon,
    nodeCreateType: INPUTNODE,
  },
  {
    title: "Knowledge Base",
    icon: LucideBookText,
    nodeCreateType: KNOWLEDGEBASENODE,
  },
  {
    title: "LLM Component",
    icon: SparklesIcon,
    nodeCreateType: LLMNODE,
  },
  {
    title: "Output Component",
    icon: CheckCircle2,
    nodeCreateType: OUTPUTNODE,
  },
];
