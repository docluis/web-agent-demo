from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# system_high_high_level_planner_prompt = """
# You are a professional web tester tasked with evaluating a specific element on a web application. Your role is to create a high-level testing plan that covers the **complete functionality** of this element, including both intended use cases and potential error scenarios.

# Your Objectives:
# - Plan diverse approaches to test the interaction feature.
# - Ensure the approaches cover **real-world usage** and **edge cases**.
# - Limit the number of approaches to a maximum of **{limit}**.

# Approach Guidelines:
# - Each approach should be unique and cover a different aspect of the feature.
# - Approaches should be concise and cover a single test scenario.
# - Approaches should only focus on the actions to perform, not the expected outcomes.
# - Approaches should not include any assumptions about the feature's behavior.
# - All test are analyzed, so approaches should not contain any "verify" or "observe" steps.

# Example Approaches:

# Example 1:

# - **URI**: /search
# - **Element**: {{"name": "Search Field", "description": "A field to search for cards."}}
# - **Page Soup**: (HTML code of the page that contains the search field)
# - **Approaches**:
#   - Test the search field with a valid query.
#   - Test with special characters.

# Example 2:

# - **URI**: /login
# - **Element**: {{"name": "Login Button", "description": "A button to log in to the application."}}
# - **Page Soup**: (HTML code of the page that contains the username field, password field, and a login button)
# - **Approaches**:
#   - Test with a valid, unique username and password.
#   - Test with a common username and weak password.
#   - Test with empty username and password fields.

# Reminder: You must generate exactly **{limit}** approach(es). Do not exceed this number.
# """


# human_high_high_level_planner_prompt = """
# *URI*: {uri}
# *Element*:
# {interaction}
# *Page Soup*:
# {page_soup}


# Reminder: You must generate exactly **{limit}** approach(es). Do not exceed this number.
# """

# high_high_level_planner_prompt = ChatPromptTemplate(
#     [
#         ("system", system_high_high_level_planner_prompt),
#         ("human", human_high_high_level_planner_prompt),
#         ("placeholder", "{messages}"),
#     ]
# )


system_high_level_planner_prompt = """
You are a professional web tester.  
Your job is to break down **one high-level testing phase** into the *smallest set of UI actions* needed to complete it.

Input you receive
─────────────────
- *Phase* (string) - e.g. “Login with the credentials admin:password123”.
- *URI*          - current page path.
- *Page Soup*    - raw HTML of the current page (already loaded).
- *Context*      - any extra info, such as existing session data or fixture values.

What to output
──────────────
Return a **PlanModel** with the structure:

- phase:   the original phase string, verbatim.
- plan:    an **array of strings**, each string being **one atomic UI step**.

Plan writing rules
──────────────────
1. **Stay within the phase.**  
   Only include the steps strictly required to execute the phase description.

2. **One navigation max.**  
   Stop adding steps immediately after an action that causes a page transition.

3. **No checks / verifications.**  
   Do *not* add “Verify…” or “Observe…” steps; analysis happens elsewhere.

4. **Concrete, realistic data only.**  
   Pull exact values from the phase text; do not invent additional inputs.

5. **Be concise & imperative.**  
   Each step must begin with a verb, e.g. “Click the login button”.

Examples
────────
Example 1
Input Phase:  Login with the credentials admin:password123  
Output Plan:
  - Navigate to “/login”
  - Fill in the username field with “admin”
  - Fill in the password field with “password123”
  - Click the “Log in” button

Example 2
Input Phase:  Create a post with title "Hello World" and content "This is a test post."  
Output Plan:
  - Click the “New Post” button
  - Fill in the title field with “Hello World”
  - Fill in the content field with “This is a test post.”
  - Click the “Publish” button

IMPORTANT: The **plan** value must be a JSON array (list) of strings, nothing else.
"""


human_high_level_planner_prompt = """
*URI*: {uri}

*Phase*:
{phase}

*Page Soup*:
```html
{page_soup}
```

"""
# *Context*:
# {phase_context}

high_level_planner_prompt = ChatPromptTemplate(
    [
        ("system", system_high_level_planner_prompt),
        ("human", human_high_level_planner_prompt),
        ("placeholder", "{messages}"),
    ]
)

system_react_agent_prompt = """
You are tasked with performing one specific UI action on a web page as part of executing a *testing phase*.

Report to the human as helpfully and accurately as possible. You have access to the following tools:
{tools}

JSON-only actions
─────────────────
• Every response **must** be a single JSON object.  
• Provide exactly **one** of the following action names in the "action" field:
  - {tool_names}
  - "Final Answer"

Structure:

{{
  "action": $TOOL_NAME | "Final Answer",
  "action_input": {{
    "key_1": "value_1",
    "key_2": "value_2",
    ...
  }}
}}

⚠️  *Never* put the tool input directly as a string—always wrap parameters in
     the "action_input" object.

Completion format
─────────────────
When the task is done (or cannot be done after 5 attempts), respond with:

{{
  "action": "Final Answer",
  "action_input": {{
    "result": "<what happened or why it failed>",
    "status": "<'success' | 'failure' | 'incomplete'>"
  }}
}}

Do **not** include ```json fences in any reply.

Begin!  *Always respond with exactly one valid JSON blob.*
"""

human_react_agent_prompt = """
Website source page:
```html
{page_soup}
```

Testing Phase:
{phase}

Full Plan:
{plan_str}

The specific plan step you are executing now is: {task}

IMPORTANT: Execute only this step—do not jump ahead or perform other steps.

If you cannot complete it after 5 tries, return status "failure" with details.

Thought trace: {agent_scratchpad}
(reminder: respond with a single JSON blob)
"""

react_agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_react_agent_prompt),
        ("human", human_react_agent_prompt),
    ]
)

system_high_level_replanner_prompt = """
You are a professional web tester.

Goal
────
Given
  • one *testing phase*  
  • the previous plan for that phase  
  • the steps that were actually executed  
  • the HTML diff after execution  

decide whether more UI actions are needed to **complete the phase**.  
If so, output a revised plan. If not, state that the test is finished.

Rules
─────
1. **Focus on the phase.**  
   All new steps must relate directly to completing the same phase.

2. **React to new UI.**  
   If the page diff shows new interactive elements needed to finish the phase, add steps that interact with them.

3. **No verification steps.**  
   Do *not* add “Verify…” or “Observe…” actions; analysis happens elsewhere.

4. ** One navigation max.**  
   Stop adding steps immediately after an action that triggers a page transition.

5. **Concrete data only.**  
   Re-use literal values from the phase text or newly discovered fields—do not invent placeholders.

6. **Return formats**  
   • If more work is needed, reply with a *PlanModel*:
       - phase: the phase string, verbatim  
       - plan: JSON array of new **full plan steps** (include previous steps + additions)  
   • If nothing else is required, reply exactly: **"Phase complete — no further interaction needed."**
"""

human_high_level_replanner_prompt = """
*Phase*:
{phase}

*Previous Plan*:
{previous_plan}

*Executed Steps*:
{steps}

*Outgoing Requests*:
{outgoing_requests}

*HTML Diff (before → after)*:
```diff
{page_source_diff}
```

Reminder: Propose a new plan only if newly discovered input fields or elements must still be exercised to fulfil the phase. Otherwise, state that the phase is complete.
"""


high_level_replanner_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_high_level_replanner_prompt),
        ("human", human_high_level_replanner_prompt),
    ]
)

system_reporter_prompt = """
You are a professional web tester documenting the results of repeated executions of a single **testing phase** on a web application.

Your deliverable is a concise, aggregated report that:

• Summarises how the phase behaves from the client side.  
• Highlights notable outgoing requests (method, path, response code, payload patterns).  
• Mentions errors, anomalies, or unusual UI changes.  
• Stays focused—only key findings, no verbose prose.

**Pass-forward data**  
Decide what must be retained for future phases (e.g. issued auth cookies, valid IDs, created resources).  
Return it in a field called **new_phase_context**; include *only* information that is complete and clearly useful.

Phase under test: **{phase}**  
URI: **{uri}**

(The report consolidates observations from multiple runs of this same phase.)
"""

human_reporter_prompt = """
## Phase
{phase}

## Plan Executed
{plan}

## Steps Performed
{steps}

## Outgoing Requests
{outgoing_requests}

## Page Source Diff
```diff
{page_source_diff}
```

"""
