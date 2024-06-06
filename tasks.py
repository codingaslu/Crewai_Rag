from textwrap import dedent
from crewai import Task
from tools import GetTools


class PrepTasks():

  def prompt_task(self, agent, query, chat_history):
    return Task(
			description=dedent(f"""\
                Go step by step.
                Step 1: Take the this user query {query}.
                Step 2: Use the Get Context Tool to retrieve relevent context.
                Step 3: Answer the query using retrieved context and chat history(if available)

				Chat History: {chat_history}
				Query : {query}"""),
			expected_output=dedent("""\
				A well-structured output"""),
			agent=agent,
            tools=[GetTools().context]
		)
    

