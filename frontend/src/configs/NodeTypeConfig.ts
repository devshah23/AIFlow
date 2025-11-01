export const INPUTNODE = "input" as const; //defines a const for run time
export type INPUTNODE = typeof INPUTNODE; //defines a type for compile time

export const OUTPUTNODE = "output" as const;
export type OUTPUTNODE = typeof OUTPUTNODE;

export const KNOWLEDGEBASENODE = "knowledgeBase" as const;
export type KNOWLEDGEBASENODE = typeof KNOWLEDGEBASENODE;

export const LLMNODE = "llm" as const;
export type LLMNODE = typeof LLMNODE;

export type NODE_TYPES = INPUTNODE | OUTPUTNODE | KNOWLEDGEBASENODE | LLMNODE;
