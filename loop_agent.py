# Contains the root agent and it's sub-agents

# Importing dependencies
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import google_search

from .util import load_instruction_from_file

# Sub-agent 1: Script Writer
scriptwriter_agent = LlmAgent(
    name="ShortsScriptWriter",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("scriptwriter_instruction.txt"),
    tools=[google_search],
    output_key="generated_script"
)

# Sub-agent 2: Visualizer
visualizer_agent = LlmAgent(
    name="ShortsVisualizer",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("visualizer_instruction.txt"),
    description="Generate visual concepts based on the proivded script.",
    output_key="visual_concept"
)

# Sub-agent 3: Formatter
formatter_agent = LlmAgent(
    name="ConceptFormatter",
    model="gemini-2.0-flash-001",
    instruction="""Combine the script from state['genetaed_script'] and the visual concepts from state['visual_concept'] into a final markdown format requested previously (Hook, Script & Visuals table, Visual Notes, CTA).""",
    description="Formats the final Short Concept.",
    output_key="final_short_concept",
)

# LLM Agent Workflow
youtube_shorts_agent = LoopAgent(
    name="youtube_shorts_agent",
    max_iterations=3,
    sub_agents=[scriptwriter_agent, visualizer_agent, formatter_agent],

)

# The runner will now execute the workflow
root_agent = youtube_shorts_agent