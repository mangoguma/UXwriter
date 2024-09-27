from openai import OpenAI


import json


data_schema = {
    "type": "object",
    "properties": {
        "Core_Values": {
            "type": "object",
            "properties": {
                "Clear": {"type": "boolean"},
                "Concise": {"type": "boolean"},
                "Casual": {"type": "boolean"},
                "Respect": {"type": "boolean"},
                "Emotional": {"type": "boolean"},
                "Remove_empty_sentences": {"type": "boolean"},
                "Focus_on_key_message": {"type": "boolean"},
                "Easy_to_speak": {"type": "boolean"},
                "Suggest_than_force": {"type": "boolean"},
                "Universal_words": {"type": "boolean"},
                "Find_hidden_emotion": {"type": "boolean"},
            },
        }
    },
    "required": ["Core_Values", "Principles"],
}


class UXwriter:
    client = None

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)


    def get_score(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in evaluating content based on predefined values and principles. 
                    For each of the core values and Principles provided, you will return a True or False assessment.""",
                },
                {"role": "user", "content": prompt},
            ],
            functions=[
                {
                    "name": "evaluate_content",
                    "description": "Evaluate the content based on Core Vlues and Principles",
                    "parameters": data_schema,
                }
            ],
            function_call={"name": "evaluate_content"},
        )
        result = response.choices[0].message.function_call.arguments
        return result


    def edit(self, prompt, score):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI content assistant. First, think step-by-step. Carefully identify the content's weak points.
                        Then, suggest sentences that fully meet the Core Values and Principles.
                        Minimize additional explanations.
                        Do not use Markdown format in your response.
                        no talk; just do.
                        Core Values:
                            - Clear // Clear
                            - Concise // Concise
                            - Casual // Friendly
                            - Respect // Respectful
                            - Emotional // Empathetic

                        Principles:
                            - Predictable hint // Does it provide a hint about what’s next?
                            - Weed cutting // Have all unnecessary words been removed?
                            - Remove empty sentences // Have all meaningless sentences been removed?
                            - Focus on key message // Does it only convey the key message?
                            - Easy to speak // Are complex terms or expressions avoided?
                            - Suggest than force // Does it avoid forcing actions or instilling fear?
                            - Universal words // Is it universally understandable and harmless?
                            - Find hidden emotion // Does it go beyond delivering information and connect with the user's emotions?
                        """,
                },
                {
                    "role": "user",
                    "content": f"""Content: 
                        {prompt}

                        Content Evaluation Criteria:
                        {json.dumps(score)}

                        no talk; just do. only sentence
                    """,
                },
            ],
        )
        return response.choices[0].message.content

