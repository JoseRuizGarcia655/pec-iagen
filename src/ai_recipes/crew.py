# src/ai_recipes/crew.py
from config.config import PATH, is_verbose
from config.structure_output import IngredientsResponse, BookRecipes
from config.llm import get_llm
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool

llm = get_llm()

@CrewBase
class CookingCrew():

  agents: List[BaseAgent]
  tasks: List[Task]

  def initializer(self, args: dict) -> None:
    self.title = args["title"]
    self.path_book = args["path_book"]
    self.name_article = args["name_article"]
    self.path_article = args["path_article"]

  @agent
  def ingredient_finder(self) -> Agent:
    return Agent(
      config=self.agents_config['ingredient_finder'], # type: ignore[index]
      llm=llm,
      verbose=is_verbose
    )

  @agent
  def ingredient_checker(self) -> Agent:
    return Agent(
      config=self.agents_config['ingredient_checker'], # type: ignore[index]
      llm=llm,
      verbose=is_verbose
    )
  
  @agent
  def chef(self) -> Agent:
    return Agent(
      config=self.agents_config['chef'], # type: ignore[index]
      llm=llm,
      verbose=is_verbose
    )
  
  @agent
  def judge_cooking(self) -> Agent:
    return Agent(
      config=self.agents_config['judge_cooking'], # type: ignore[index]
      llm=llm,
      verbose=is_verbose
    )
  
  @agent
  def writer(self) -> Agent:
    return Agent(
      config=self.agents_config['writer'], # type: ignore[index]
      llm=llm,
      verbose=is_verbose
    )

  @task
  def ingredient_finder_task(self) -> Task:
    return Task(
      config=self.tasks_config['ingredient_finder_task'], # type: ignore[index]
      tools=[FileReadTool(file_path=PATH.BOOKS.value)],
      output_json=IngredientsResponse,
    )

  @task
  def ingredient_checker_task(self) -> Task:
    return Task(
      config=self.tasks_config['ingredient_checker_task'], # type: ignore[index]
      output_json=IngredientsResponse,
    )
  
  @task
  def make_recipes_task(self) -> Task:
    return Task(
      config=self.tasks_config['make_recipes_task'], # type: ignore[index]
      output_json=BookRecipes,
    )

  @task
  def judge_recipes_task(self) -> Task:
    return Task(
      config=self.tasks_config['judge_recipes_task'], # type: ignore[index]
      output_json=BookRecipes,
    )
  
  @task
  def writer_task(self) -> Task:
    return Task(
      config=self.tasks_config['writer_task'], # type: ignore[index]
      output_file=self.path_article,
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=is_verbose,
    )
