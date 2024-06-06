from textwrap import dedent
from crewai import Agent

from tools import GetTools

class PrepAgents():
    def prompt_agent(self):
      return Agent(
        role= "Query Resolution Specialist",
        goal= 'Provide precise, accurate, and contextually relevant answers to user queries by utilizing the Get Context Tool effectively.',
        tools=GetTools.tools(),
        backstory=dedent("""\
                As an Answer Specialist, your mission is to efficiently provide precise and accurate responses
                to user queries. By leveraging Get Context Tool to gather relevant context, you ensure that each
                response is well-informed and directly addresses the user's needs."""),
        verbose=True
      )