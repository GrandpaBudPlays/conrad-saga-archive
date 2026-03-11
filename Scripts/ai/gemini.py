import os
import time
from google import genai
from google.genai import types
from google.genai import errors
from google.genai.errors import ClientError

from ai.base import BaseAIModel, ModelResult


class GeminiModel(BaseAIModel):
    DEFAULT_MODEL = 'gemini-3-flash-preview'
    DEFAULT_BACKUP = 'gemini-2.5-flash'
    DEFAULT_TIMEOUT = 480000

    PRICING = {
        'gemini-3-flash-preview': {'input': 0.50, 'output': 3.00},
        'gemini-2.5-flash': {'input': 0.30, 'output': 2.50},
        'gemini-2.5-pro': {'input': 1.25, 'output': 10.00},
    }

    def __init__(self, client: genai.Client | None = None, api_key: str | None = None, model_name: str | None = None, backup_model: str | None = None):
        if client:
            self._client = client
        else:
            api_key = api_key or os.getenv('GEMINIAPIKEY')
            # Use types.HttpOptions to avoid type check errors if possible, 
            # but genai.Client often takes a dict or HttpOptions.
            self._client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=self.DEFAULT_TIMEOUT))
        self._model_name = model_name or self.DEFAULT_MODEL
        self._backup_model = backup_model or self.DEFAULT_BACKUP

    @property
    def name(self) -> str:
        return self._model_name

    def generate(self, prompt: str, system_instruction: str = "", temperature: float = 0.1, response_mime_type: str = "text/plain", response_schema: dict | None = None) -> ModelResult:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            response_mime_type=response_mime_type
        )
        if response_schema:
            config.response_schema = response_schema
            
        config = self._ensure_timeout_config(config)
        return self._generate_with_retry(config, prompt)

    def _ensure_timeout_config(self, config: types.GenerateContentConfig) -> types.GenerateContentConfig:
        current_options = getattr(config, 'http_options', None)
        if current_options and getattr(current_options, 'timeout', None) is not None:
            return config

        config.http_options = types.HttpOptions(timeout=self.DEFAULT_TIMEOUT)
        return config

    def _calculate_cost(self, response, model_name: str) -> tuple:
        if not hasattr(response, 'usage_metadata'):
            return 0, 0, 0.0

        rates = self.PRICING.get(model_name, self.PRICING['gemini-2.5-flash'])
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count

        input_cost = (input_tokens / 1_000_000) * rates['input']
        output_cost = (output_tokens / 1_000_000) * rates['output']
        total_cost = input_cost + output_cost

        print(f"--- Cost Report ({model_name}) ---")
        print(f"Input:  {input_tokens:,} tokens (${input_cost:.4f})")
        print(f"Output: {output_tokens:,} tokens (${output_cost:.4f})")
        print(f"Total:  ${total_cost:.4f}")

        return input_tokens, output_tokens, total_cost

    def _extract_retry_delay(self, error) -> float | None:
        if hasattr(error, 'details') and error.details:
            for detail in error.details:
                if hasattr(detail, 'retry_delay') and detail.retry_delay:
                    return float(detail.retry_delay.rstrip('s'))
        return None

    def _generate_with_retry(self, config: types.GenerateContentConfig, contents: str, retries: int = 6) -> ModelResult:
        model_name = self._model_name
        fallback_used = False

        print(f"Attempting to generate content with model '{model_name}'...")

        for i in range(retries):
            if i == 3:
                print(f"--- Switching to backup model ---")
                model_name = self._backup_model
                fallback_used = True

            try:
                response = self._client.models.generate_content(
                    model=model_name,
                    config=config,
                    contents=contents
                )
                if response is None or not hasattr(response, 'text') or response.text is None:
                    self._handle_retry(i, retries, "Empty/None response", wait_multiplier=5)
                    continue
                input_tokens, output_tokens, cost = self._calculate_cost(response, model_name)
                return ModelResult(
                    model_name=model_name,
                    content=response.text,
                    success=True,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost=cost,
                    fallback_used=fallback_used
                )
            except errors.ServerError as e:
                if e.code == 503:
                    self._handle_retry(i, retries, f"Server busy (503)", wait_multiplier=5)
                elif e.code == 429:
                    retry_delay = self._extract_retry_delay(e)
                    if retry_delay:
                        print(f"--- Quota exceeded (429). Retry after {retry_delay}s ---")
                        time.sleep(retry_delay)
                    print(f"--- Switching to backup model: {self._backup_model} ---")
                    model_name = self._backup_model
                    fallback_used = True
                    continue
                else:
                    print(f"Server Error {e.code}")
                    return ModelResult(model_name=model_name, content="", success=False, error=str(e))

            except (TimeoutError, OSError) as e:
                self._handle_retry(i, retries, "Timeout error", wait_multiplier=10)

            except ClientError as e:
                print(f"--- Rate limit detected ({type(e).__name__}). Switching to backup model ---")
                model_name = self._backup_model
                fallback_used = True
                continue

            except Exception as e:
                self._handle_retry(i, retries, f"Connection issue ({type(e).__name__})", wait_multiplier=5, optional=True)

        return ModelResult(model_name=model_name, content="", success=False, error="Max retries exceeded")

    def _handle_retry(self, attempt: int, total: int, message: str, wait_multiplier: int, optional: bool = False):
        if optional and attempt >= total - 1:
            print(f"{message} (attempt {attempt+1}/{total}). All retries exhausted. Giving up.")
            return
        wait_time = (attempt + 1) * wait_multiplier
        print(f"{message} (attempt {attempt+1}/{total}). Retrying in {wait_time}s...")
        time.sleep(wait_time)
