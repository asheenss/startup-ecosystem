import json
from typing import Dict, Any, Type, TypeVar, Optional
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from app.core.config import settings
from .protocol import ProtocolMessage

T = TypeVar("T", bound=BaseModel)

class LLMInterface:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = "gpt-4o-mini"

    def process_task(self, msg: ProtocolMessage, response_model: Optional[Type[T]] = None) -> Dict[str, Any]:
        """
        Processes a structured task via the LLM.
        Enforces protocol-compliant JSON output.
        """
        if not self.client:
            return {"error": "LLM client not configured"}

        system_prompt = f"""
        You are an AI Agent operating within a structured multi-agent system.
        You must adhere to the following protocol:
        - Input is a ProtocolMessage (JSON).
        - Output must be a JSON object matching the 'expected_output' schema.
        - Your name: {msg.agent}
        """

        user_content = json.dumps(msg.model_dump(), indent=2)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content or "{}"
            payload = json.loads(raw_content)

            # Optional: Validate against a Pydantic model if provided
            if response_model:
                try:
                    validated = response_model.model_validate(payload)
                    return validated.model_dump()
                except ValidationError as e:
                    return {"error": "Validation failed", "details": str(e), "raw": payload}

            return payload

        except Exception as e:
            return {"error": str(e)}
