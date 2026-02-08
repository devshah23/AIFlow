
from app.exceptions.Exceptions import InvalidNodeConfigException
from app.llm.provider_factory import ProviderFactory
from app.services.workflow_runner.context import WfExecutionContext
from app.services.workflow_runner.executors.base_executor import NodeExecutor
from app.services.workflow_runner.executors.executor_util import ExecutorUtil
from google.genai import errors


class LLMExecutor(NodeExecutor):
        
    async def execute(self, context: WfExecutionContext,upstream_nodes):
        try:
          cfg = self.node.config
          
          if cfg["api_key"]=="" or cfg["model"]=="":
            raise InvalidNodeConfigException("LLM Nodes details not found")
          llm_provider = ProviderFactory.create(
              provider_name=cfg.get("provider","gemini"),
              api_key=cfg["api_key"],
              model=cfg["model"],
              temperature=cfg.get("temperature", 0.3),
          )
          upstream_nodes_data = ExecutorUtil.get_data_from_upstream_with_node_types(context, upstream_nodes)
          prompt=self.build_prompt(self.node,upstream_nodes_data,org_query=context.get_output("input_query") or "");
          output = await llm_provider.generate_content_by_prompt(prompt)
          

          return {
              "output": output
          }

        except errors.ServerError as e:
          raise Exception("LLM Node Executor failed: Gemini Error")
        except errors.ClientError as e:      
          raise Exception(f"LLM Node Executor failed Code: {e.code}")
        except errors.APIError as e:
          raise Exception(f"LLM Node Executor failed: API Error") 
        except Exception as e:
          raise Exception("LLM Node Executor failed") from e
        
        
    def build_prompt(self, node, upstream_data,org_query:str):
        upstream_sections = []

        for i, data in enumerate(upstream_data, start=1):
            upstream_sections.append(
                f"[Context {i}]\n{data}"
            )

        upstream_text = "\n\n".join(upstream_sections)

        system_prompt = node.config.get(
            "system_prompt", 
            "Follow the user prompt and use upstream context only when relevant."
        )

        user_prompt = node.config.get("prompt", "")

        final_prompt = f"""
You are an LLM node inside a workflow execution engine.

Your responsibility is to execute a TASK INSTRUCTION
in order to produce an output for the given WORKFLOW INPUT QUERY,
optionally using upstream context as supporting evidence.

You MUST strictly follow the rules below.

---

## 1. Authority & Decision Rules (CRITICAL)

There are three distinct inputs with strict priority:

### A. WORKFLOW INPUT QUERY (Highest Priority)
- This is the original user query of the entire workflow.
- This defines WHAT the answer must be about.
- You must ALWAYS anchor your response to this query.

### B. UPSTREAM CONTEXT (Supporting Only)
- Upstream context may include outputs from knowledge base, tools, or other nodes.
- These are OPTIONAL and SUPPORTING only.
- They are NOT the user query.

Before using any upstream context, perform this check:

#### Relevance Check
- Determine whether any upstream context explicitly discusses
  the same topic or entity as the WORKFLOW INPUT QUERY.
- Explicitly means direct mention or clear factual relevance.
- Implicit, tangential, or loosely related information is NOT relevant.

#### Decision
- If NO upstream context is explicitly relevant:
  - IGNORE ALL upstream context completely.
  - Answer using general world knowledge OR output "Not available".
- If upstream context IS relevant:
  - Use ONLY the relevant portions.
  - Ignore everything else.

You must NEVER treat upstream context as the query itself.

## Answer Provenance Declaration (MANDATORY)

Before producing the final answer, you must determine the source of your answer:

- If the answer uses ANY upstream knowledge base context:
  Answer Mode = DOCUMENT_KNOWLEDGE

- If ALL upstream context is ignored and the answer is generated
  using only your general world knowledge:
  Answer Mode = GENERAL_KNOWLEDGE

You must explicitly declare the Answer Mode in the output.


### C. TASK INSTRUCTION (Behavioral Guidance)
- The task instruction give some information about generation of the output
  (e.g., summarize, answer concisely).
- It does NOT define the topic.
- It must never override the WORKFLOW INPUT QUERY.

Failure to respect these priorities is incorrect behavior.

---

## 2. System Instructions
Follow the SYSTEM INSTRUCTIONS exactly as written.
These define behavior, tone, constraints, and output rules.

---

## 3. Task Execution Rules

The TASK INSTRUCTION defines HOW to produce the output.

- If a TASK INSTRUCTION is provided:
  - Follow it exactly.
  - It may specify format, length, tone, or purpose.

- If NO TASK INSTRUCTION is provided:
  - Default task is:
    "Answer the WORKFLOW INPUT QUERY factually and concisely."

The TASK INSTRUCTION may refine behavior,
but it must NEVER change the topic defined by the WORKFLOW INPUT QUERY.


---

## Output Format (STRICT)

You must follow these rules exactly. Follow the instructions carefully.

### 1. Default Output Format
Unless explicitly overridden by the Task Instruction, the output MUST be in the following **Markdown format**:

**Answer Mode:** <DOCUMENT_KNOWLEDGE | GENERAL_KNOWLEDGE>

**Answer:**
<final answer text formatted in Markdown, including headings, bold, italics, bullet points, paragraphs as appropriate>

### 2. Formatting Rules
- Use proper Markdown formatting.
- Separate logical sections with a blank line.
- Use bullet points or paragraphs where appropriate.
- Do NOT put everything on a single line.
- Do NOT escape newlines.
- Do NOT wrap the answer in quotes or code blocks.
- Highlight key terms or important phrases using **bold** or *italic*.
- Use headings or subheadings where helpful to structure the answer.

### 3. JSON Override Rule (IMPORTANT)
If the Task Instruction explicitly asks to:
- "return JSON"
- "respond in JSON"
- "output a JSON object"
- or specifies a JSON schema

THEN:
- Ignore the default Markdown Output Format entirely.
- Return **ONLY valid JSON** that conforms to the requested schema.
- Do NOT include "Answer Mode", "Answer:", explanations, or Markdown.
- Do NOT include any extra text outside the JSON.

### 4. No Mixed Output
- Never mix JSON with Markdown or plain text.
- The output must be either **strict JSON** or **strict Markdown-formatted text**, never both.

### 5. Knowledge Mode Selection
- Use **DOCUMENT_KNOWLEDGE** only if the answer is derived from retrieved documents.
- Use **GENERAL_KNOWLEDGE** if the answer is based on general model knowledge.


---

### WORKFLOW INPUT QUERY:
{org_query}

### UPSTREAM CONTEXT:
{upstream_text}

### SYSTEM INSTRUCTIONS:
{system_prompt}


### TASK INSTRUCTION:
{user_prompt if user_prompt else "No task instruction provided. Use the default task."}
    """

        return final_prompt.strip()
