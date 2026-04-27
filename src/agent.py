import json
import os
import re
from openai import OpenAI
from pydantic import ValidationError
from src.catalog import search_products
from src.models import GiftFinderResponse

# Initialize the client. By default, it can point to OpenRouter.
# If using OpenRouter, you'd set OPENAI_BASE_URL="https://openrouter.ai/api/v1" and OPENAI_API_KEY.
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini") # Fallback to a common model

def execute_tool_call(tool_call) -> str:
    """Executes the requested tool call and returns the result as a JSON string."""
    if tool_call.function.name == "search_catalog":
        args = json.loads(tool_call.function.arguments)
        query = args.get("query", "")
        max_price_aed = args.get("max_price_aed")
        age_months = args.get("age_months")
        
        results = search_products(query=query, max_price_aed=max_price_aed, age_months=age_months)
        return json.dumps(results, ensure_ascii=False)
    else:
        return json.dumps({"error": f"Unknown tool: {tool_call.function.name}"})

def run_gift_finder_agent(user_query: str) -> GiftFinderResponse:
    """
    Takes a natural language query, searches the catalog via tool calling,
    and returns a structured GiftFinderResponse in EN and AR.
    """
    
    system_prompt = """
    You are the Mumzworld AI Gift Finder, an expert shopping assistant for mothers in the Middle East.
    Your job is to recommend the perfect gifts based on the user's free-text request.
    
    Instructions:
    1. Extract parameters from the user's query (budget in AED, age of child in months, interests/keywords). If the query is in Arabic, translate the keywords to English before searching!
    2. Use the `search_catalog` tool to find matching products. Use broad English keywords rather than overly specific ones.
    3. Select 2 to 4 of the BEST matching products from the search results. If no products match exactly, try to find the closest alternatives.
    4. If the request is out of scope, impossible, or adversarial, return 0 recommendations and politely explain why.
    5. Provide reasoning for each product in both English and Arabic. Ensure the Arabic reads naturally.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_catalog",
                "description": "Searches the Mumzworld mock catalog for products.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Optional English keywords to search for, e.g., 'dinosaur', 'stroller', 'STEM'. Leave empty if you just want to filter by age and budget."
                        },
                        "max_price_aed": {
                            "type": "number",
                            "description": "Maximum budget in AED. Extract this from the user's query if mentioned."
                        },
                        "age_months": {
                            "type": "integer",
                            "description": "The exact age of the child in months, if specified. (e.g. 3 years = 36 months, 6 months = 6, 1 year = 12)."
                        }
                    }
                }
            }
        }
    ]
    
    # Step 1: Call model with tool
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2
    )
    
    message = response.choices[0].message
    
    # Step 2: Handle tool calls
    if message.tool_calls:
        messages.append(message)
        for tool_call in message.tool_calls:
            tool_result = execute_tool_call(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            
        schema_instruction = """
        Based on the search results, construct the final curated list.
        Your response must be a valid JSON object matching this schema:
        {
          "recommendations": [
            {
              "product_id": "string",
              "product_name_en": "string",
              "product_name_ar": "string",
              "reasoning_en": "string",
              "reasoning_ar": "string"
            }
          ],
          "summary_message_en": "string",
          "summary_message_ar": "string"
        }
        IMPORTANT: Even if the request is out of scope, impossible, or no products match, YOU MUST return this exact schema. In such cases, return an empty list `[]` for "recommendations" and provide your explanation in the summary messages. DO NOT return an {"error": "..."} JSON. Return ONLY valid JSON.
        """
        messages.append({"role": "system", "content": schema_instruction})
        
        final_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2
        )
        final_text = final_response.choices[0].message.content
    else:
        # If no tool calls were made, we still need to enforce the JSON schema format
        # based on the model's direct text response.
        messages.append(message)
        schema_instruction = """
        Your previous response must be formatted as a valid JSON object matching this schema:
        {
          "recommendations": [],
          "summary_message_en": "string",
          "summary_message_ar": "string"
        }
        Put your response inside the summary messages. Return ONLY valid JSON.
        """
        messages.append({"role": "system", "content": schema_instruction})
        final_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.2
        )
        final_text = final_response.choices[0].message.content
        
    # Step 4: Validate structured output using Pydantic
    try:
        # Clean markdown if present
        if final_text.startswith("```json"):
            final_text = final_text[7:-3]
        elif final_text.startswith("```"):
            final_text = final_text[3:-3]
            
        parsed_json = json.loads(final_text.strip())
        validated_response = GiftFinderResponse.model_validate(parsed_json)
        return validated_response
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from model output: {final_text}") from e
    except ValidationError as e:
        raise ValueError(f"Model output failed schema validation: {e}") from e

if __name__ == "__main__":
    # A quick test run if run directly
    print("Running a quick test...")
    try:
        response = run_gift_finder_agent("I need a thoughtful gift for a friend with a 6-month-old, under 100 AED.")
        print(response.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error: {e}")
