import json
import google.generativeai as genai
from app.core.config import settings

# 1. Configure the Gemini library with your API key
genai.configure(api_key=settings.GOOGLE_API_KEY)

# 2. Define generation settings to enforce JSON output
generation_config = {
    "response_mime_type": "application/json",
}

def get_llm_response(query: str, context: list[str]) -> dict:
    """
    Generates a structured JSON response using the Gemini AI model.
    """
    # 3. Instantiate the Gemini model with the specified settings
    model = genai.GenerativeModel(
        settings.LLM_MODEL,
        generation_config=generation_config
    )

    context_str = "\n---\n".join(context)
    
    # The prompt remains the same.
    prompt = f"""
    You are an intelligent assistant for analyzing legal, insurance, and HR documents. 
    Based *only* on the provided context below, answer the user's query.

    Your response MUST be in a valid JSON format with the following keys:
    - "answer": (string) A direct 'yes' or 'no' answer, or a concise summary if the question is not a yes/no type.
    - "conditions": (list of strings) A list of specific conditions, limitations, or requirements mentioned in the context that apply to the answer. If none, provide an empty list.
    - "rationale": (string) A clear explanation of how you arrived at the answer, citing specific parts of the context.
    - "retrieved_clauses": (list of strings) The exact text of the clauses from the context that you used to form your answer.

    **Context from the document:**
    ---
    {context_str}
    ---

    **User Query:**
    "{query}"

    **JSON Response:**
    """

    try:
        # 4. Call the Gemini API
        response = model.generate_content(prompt)
        
        # 5. The response text contains the JSON string
        response_content = response.text
        
        parsed_response = json.loads(response_content)
        
        # Ensure all required keys are present
        required_keys = ["answer", "conditions", "rationale", "retrieved_clauses"]
        for key in required_keys:
            if key not in parsed_response:
                raise KeyError(f"Missing key in LLM response: {key}")

        return parsed_response

    except Exception as e:
        print(f"Error calling LLM or parsing response: {e}")
        return {
            "answer": "Error processing the document.",
            "conditions": [],
            "rationale": f"An error occurred while communicating with the AI model: {str(e)}",
            "retrieved_clauses": context
        }