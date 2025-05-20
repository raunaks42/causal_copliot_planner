from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool, FileWriterTool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()

@CrewBase
class CausalCopilotPlanner():
    """CausalCopilotPlanner crew"""

    @agent
    def scientist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scientist_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @agent
    def assistant_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @agent
    def dummy_specialized_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['dummy_specialized_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @task
    def create_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_plan'],
        )
    
    @task
    def start_subgoal(self) -> Task:
        return Task(
            config=self.tasks_config['start_subgoal'],
        )
    
    @task
    def collect_subgoal_results(self) -> Task:
        return Task(
            config=self.tasks_config['collect_subgoal_results'],
        )
    
    @task
    def evaluate_subgoal(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_subgoal'],
        )
    
    @task
    def run_dummy_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['run_dummy_agent_task'],
        )

    @crew
    def crew(self, task_name=None) -> Crew:
        """Creates the CausalCopilotPlanner crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # return Crew(
        #     verbose=True,
        #     agents=[self.scientist_agent(), self.assistant_agent()],
        #     tasks=[self.create_plan(), self.start_subgoal(), self.collect_subgoal_results(), self.evaluate_subgoal()],
        #     process=Process.sequential,
        # )
        if task_name:
            task_obj = next((t for t in self.tasks if t.name == task_name), None)
            if not task_obj:
                raise ValueError(f"Task '{task_name}' not found in tasks.yaml.")
            return SingleTaskCrew(task=task_obj)
        else:
            raise NotImplementedError("Default crew logic not implemented. Use `task_name`.")

class SingleTaskCrew:
    def __init__(self, task: Task):
        self.task = task

    def kickoff(self, inputs=None):
        inputs = inputs or {}
        # self.task.input_variables.update(inputs)
        crew = Crew(agents=[self.task.agent], tasks=[self.task], verbose=True)
        crew.kickoff(inputs=inputs)

@CrewBase
class CausalCopilotSpecializedAgents():
    """CausalCopilotSpecializedAgents crew"""
    
    @agent
    def scientist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scientist_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @agent
    def assistant_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @agent
    def dummy_specialized_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['dummy_specialized_agent'],
            tools=[file_read_tool, file_writer_tool],
        )
    
    @task
    def create_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_plan'],
        )
    
    @task
    def start_subgoal(self) -> Task:
        return Task(
            config=self.tasks_config['start_subgoal'],
        )
    
    @task
    def collect_subgoal_results(self) -> Task:
        return Task(
            config=self.tasks_config['collect_subgoal_results'],
        )
    
    @task
    def evaluate_subgoal(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_subgoal'],
        )
    
    @task
    def run_dummy_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['run_dummy_agent_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CausalCopilotSpecializedAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        assistant_agent = Agent(
            config=self.agents_config['assistant_agent'],
        )

        return Crew(
            verbose=True,
            agents=[self.dummy_specialized_agent()],
            tasks=[self.run_dummy_agent_task()],
            manager_agent=assistant_agent,
            process=Process.hierarchical,
        )
