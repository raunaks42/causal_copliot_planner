#!/usr/bin/env python
import json
import sys
import warnings

from causal_copilot_planner.crew import CausalCopilotPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    
    inputs = {
        "threshold": 0.75,
        "summary_style": "structured",  # or 'narrative'
        "causal_query": "What is the effect of remote work on software engineering productivity?",
        "dataset_name": "software_engineering_productivity.csv",
    }
    
    try:
        causal_copilot_crew = CausalCopilotPlanner().crew()

        print("🔁 Executing: create_plan")
        causal_copilot_crew.task(name="create_plan").execute(inputs=inputs)

        while True:
            print("🔁 Executing: start_subgoal")
            causal_copilot_crew.task(name="start_subgoal").execute(inputs=inputs)

            print("🔁 Executing: collect_subgoal_results")
            causal_copilot_crew.task(name="collect_subgoal_results").execute(inputs=inputs)

            print("🔁 Executing: evaluate_subgoal")
            causal_copilot_crew.task(name="evaluate_subgoal").execute(inputs=inputs)

            with open("SubGoals.json", "r") as f:
                subgoals = json.load(f)
            if all(sg["status"] == "completed" for sg in subgoals):
                print("✅ All subgoals completed.")
                break
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         CausalCopilotPlanner().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         CausalCopilotPlanner().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         CausalCopilotPlanner().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
