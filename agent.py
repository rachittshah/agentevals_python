"""
Agent implementation for AgentEval using LiteLLM for inference.
This replaces the original codegen.js implementation.
"""

import os
import litellm
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodegenAgent:
    """Agent that modifies code based on prompts using LiteLLM for inference."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the agent with API key and model.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: Model to use for inference (defaults to gpt-3.5-turbo)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as OPENAI_API_KEY environment variable")
        
        self.model = model
        # Set the API key for litellm
        os.environ["OPENAI_API_KEY"] = self.api_key
        
    async def modify_code(self, source_code: str, prompt: str) -> str:
        """
        Modify code based on the provided prompt using LiteLLM.
        
        Args:
            source_code: Original source code to modify
            prompt: Instructions for code modification
            
        Returns:
            Modified code
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"*index.html*```\n{source_code}\n```\n\n{prompt}\n\nReturn the entire contents of the new index.html."
                }
            ]
            
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=0.2,
            )
            
            # Extract the content from the response
            modified_code = response.choices[0].message.content.strip()
            
            # Clean up the code (remove markdown code blocks if present)
            cleaned_code = modified_code.replace("```html", "").replace("```", "").strip()
            
            logger.info("Code modified successfully")
            return cleaned_code
            
        except Exception as e:
            logger.error(f"Error modifying code: {str(e)}")
            raise
    
    async def run(self, target_dir: str, prompt: str) -> None:
        """
        Run the agent on a target directory with a prompt.
        
        Args:
            target_dir: Directory containing the file to modify
            prompt: Instructions for code modification
        """
        try:
            file_path = os.path.join(target_dir, "index.html")
            
            # Read the file content
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            
            # Modify the code
            modified_content = await self.modify_code(file_content, prompt)
            
            # Write the modified content back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
                
            logger.info(f"File {file_path} modified successfully")
            
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            raise
