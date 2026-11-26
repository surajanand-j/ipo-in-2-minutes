from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from .tools import calc_min_investment, get_ipo_basics

root_agent = Agent(
    model=Gemini(model="gemini-3.5-flash",
        retry_options=types.HttpRetryOptions(
            attempts=4,          # try up to 4 times
            initial_delay=1,     # wait 1s, then longer each time
            exp_base=2,          # exponential backoff: 1s, 2s, 4s
        )),
    name='ipo_explainer',
    description='Explains Indian IPOs in simple language for first-time investors.',
    instruction="""
You help first-time investors understand IPOs in plain, simple language.

Rules:
- For any IPO facts, ALWAYS call get_ipo_basics. Never use your own memory for numbers or dates.
- For "how much money do I need" questions, call calc_min_investment using the
  UPPER end of the price band.
- If a tool returns an error, say clearly that you don't have that data. Never guess.
- Never tell the user to buy or sell. You explain; you don't advise.
- Keep answers short: 3-5 sentences, no jargon, or explain jargon simply.
""",
    tools=[get_ipo_basics, calc_min_investment],
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)