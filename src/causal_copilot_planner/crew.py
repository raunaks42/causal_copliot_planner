from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

scientist_agent = Agent.load("scientist_agent")
assistant_agent = Agent.load("assistant_agent")
dummy_specialized_agent = Agent.load("dummy_specialized_agent")

create_plan = Task.load("create_plan")
start_subgoal = Task.load("start_subgoal")
collect_subgoal_results = Task.load("collect_subgoal_results")
evaluate_subgoal = Task.load("evaluate_subgoal")
run_dummy_agent_task = Task.load("run_dummy_agent_task")

@CrewBase
class CausalCopilotPlanner():
    """CausalCopilotPlanner crew"""

    @crew
    def crew(self) -> Crew:
        """Creates the CausalCopilotPlanner crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            verbose=True,
            agents=[scientist_agent, assistant_agent],
            tasks=[create_plan, start_subgoal, collect_subgoal_results, evaluate_subgoal],
            process=Process.sequential,
        )
    
@CrewBase
class CausalCopilotSpecializedAgents():
    """CausalCopilotSpecializedAgents crew"""

    @crew
    def crew(self) -> Crew:
        """Creates the CausalCopilotSpecializedAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            verbose=True,
            agents=[dummy_specialized_agent],
            tasks=[run_dummy_agent_task],
            manager_agent=assistant_agent,
            process=Process.hierarchical,
        )
