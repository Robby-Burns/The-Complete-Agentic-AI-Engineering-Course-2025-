import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv(override=True)

def record_user_details(email, name="Name not provided", notes="not provided"):
    return {"recorded": f"Email: {email}, Name: {name}, Notes: {notes}"}

def record_unknown_question(question):
    return {"recorded": question}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Use this tool to record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ed Donner"
        self.linkedin = self._load_linkedin()
        self.summary = self._load_summary()

    def _load_linkedin(self):
        try:
            reader = PdfReader("me/linkedin.pdf")
            return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        except Exception:
            return "[Missing LinkedIn PDF]"

    def _load_summary(self):
        try:
            with open("me/summary.txt", "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "[Missing Summary Text]"

    def system_prompt(self):
        return f"""You are acting as {self.name}. Your job is to engage visitors to the site, answer questions based on Ed's background, and offer to record emails or questions when appropriate.

## Summary:
{self.summary}

## LinkedIn:
{self.linkedin}
"""

    def handle_tool_call(self, tool_calls):
        results = []
        for call in tool_calls:
            tool_name = call.function.name
            args = json.loads(call.function.arguments)
            tool_fn = globals().get(tool_name)
            result = tool_fn(**args) if tool_fn else {}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": call.id
            })
        return results

    def chat(self, message, history):
        messages = [{"role": "]()

