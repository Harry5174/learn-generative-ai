# assistant.py

import json
import os
from openai import OpenAI, APIError
from openai.types.beta.threads.run import Run
import asyncio


from ..database.database import *

class AssistantManager:
    def __init__(self, api_key, engine):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.assistant_id = self.create_or_load_assistant()
        self.engine = engine 

    def create_or_load_assistant(self):
        assistant_file_path = 'assistant.json'

        if os.path.exists(assistant_file_path):
            with open(assistant_file_path, 'r') as file:
                assistant_data = json.load(file)
                assistant_id = assistant_data['assistant_id']
                print("Loaded existing assistant ID.")
        else:
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "create_person",
                        "description": "Create a new person record with name and location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "The name of the person"},
                                "location": {"type": "string", "description": "The location of the person"},
                            },
                            "required": ["name", "location"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_person_location",
                        "description": "Retrieve the location of a person by their name",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "The name of the person"},
                            },
                            "required": ["name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "read_all_persons",
                        "description": "Get data of all persons in the database",
                        "parameters": {}
                    }
                }
            ]

            try:
                assistant = self.client.beta.assistants.create(
                    instructions="""
                        The assistant will be responsible for communicating with the database to share locations of friends
                    """,
                    model="gpt-3.5-turbo-0125",
                    tools=tools
                )

                with open(assistant_file_path, 'w') as file:
                    json.dump({'assistant_id': assistant.id}, file)
                    print("Created a new assistant and saved the ID.")

                assistant_id = assistant.id
            except APIError as e:
                print(f"Error creating assistant: {e}")
                raise
        
        print({"assistant_id" :assistant_id})
        return assistant_id

    async def start_conversation(self):
        try:
            thread = self.client.beta.threads.create()
            thread_id = thread.id
            print({"thread_id": thread_id})
            return {"thread_id": thread_id}
        except APIError as e:
            print(f"Error during conversation with assistant: {e}")
            raise

    async def chat_with_assistant(self, thread_id: str, user_input: str):
        try:
            message = self.client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
            dict(message)

            run: Run = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=self.assistant_id)
            dict(run)

            while (run_status := self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)).status != 'completed':
                print(f"Run status: {run_status.status}")
                if run_status.status == "requires_action":
                    print(run_status.required_action)
                    tool_outputs = self.handle_required_actions(run_status.required_action)
                    self.client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs)
                elif run_status.status in ["failed", "expired"]:
                    raise Exception("Assistant processing failed or expired")
                else:
                    await asyncio.sleep(1)  # Make the method asynchronous and use await for sleep

            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            if messages.data and (message_content := messages.data[0].content[0]).text:
                response = message_content.text.value
                return {"response": response}
            else:
                raise Exception("The latest message has no content")
        except APIError as e:
            print(f"Error during conversation with assistant: {e}")
            raise

    def handle_required_actions(self, required_action):
        tool_outputs = []
        for tool_call in required_action.submit_tool_outputs.tool_calls:
            action_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            response = self.make_internal_api_call(action_name, arguments)
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(response)
            })
        return tool_outputs

    def make_internal_api_call(self, function_name: str, arguments: dict):
        try:
            if function_name == "get_person_location":
                if arguments and "name" in arguments:
                    location_data = get_location_or_404(arguments['name'], self.engine)
                    return {"location": location_data.location}
                else:
                    return {"error": "Missing required 'name' argument for 'get_person_location'"}

            elif function_name == "read_all_persons":
                persons_data = read_all_persons(self.engine)
                return {"persons": [{"name": person.name, "location": person.location} for person in persons_data]}

            elif function_name == "create_person":
                if arguments and "name" in arguments and "location" in arguments:
                    person_data = create_person(self.engine, Location(name=arguments["name"], location=arguments["location"]))
                    return {"message": f"Person '{person_data.name}' created successfully"}
                else:
                    return {"error": "Missing required arguments for 'create_person'"}

            else:
                return {"error": "Unsupported action"}

        except Exception as e:
            return {"error": f"Internal API call error: {str(e)}"}