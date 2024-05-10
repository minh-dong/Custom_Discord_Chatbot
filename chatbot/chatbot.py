import json
import os.path
from difflib import get_close_matches


# Return the knowledge base filename
def get_knowledge_base_filename() -> str:
    location: str = os.path.dirname(__file__)
    file: str = location + "\\knowledge_base.json"
    return file


# Load knowledge base
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


# Dump the knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Find the best match based on the user question
def find_best_match(user_question: str, questions:list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) # 0.6 = 60% accuate
    return matches[0] if matches else None


# Get the answer for the question
def get_answer_for_questions(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]