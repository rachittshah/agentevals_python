"""
Main execution script for AgentEval using Python and LiteLLM.
This replaces the original evals.js implementation.
"""

import os
import json
import shutil
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List
from agent import CodegenAgent
from evaluator import Evaluator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentEval:
    """Main class for running agent evaluations."""
    
    def __init__(self, 
                 api_key: str = None, 
                 model: str = "gpt-3.5-turbo",
                 output_dir: str = "./output"):
        """
        Initialize the AgentEval framework.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: Model to use for inference (defaults to gpt-3.5-turbo)
            output_dir: Directory to store evaluation results
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.output_dir = output_dir
        self.agent = CodegenAgent(api_key=self.api_key, model=self.model)
        self.evaluator = Evaluator(output_dir=self.output_dir)
        
    async def run_eval(self, eval_id: str, eval_dir: str) -> Dict[str, bool]:
        """
        Run a single evaluation.
        
        Args:
            eval_id: Identifier for the evaluation
            eval_dir: Directory containing the evaluation files
            
        Returns:
            Dictionary with evaluation results
        """
        prompt_file_path = os.path.join(eval_dir, "prompt.md")
        source_dir = os.path.join(eval_dir, "app")
        target_dir = os.path.join(self.output_dir, f"eval-001/app/{eval_id}")
        
        try:
            # Ensure output directory exists
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy source files to target directory
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
            logger.info(f"[{eval_id}] Directory copied successfully")
            
            # Read prompt
            with open(prompt_file_path, "r", encoding="utf-8") as f:
                prompt = f.read()
            
            # Run agent to modify code
            await self.agent.run(target_dir, prompt)
            
            # Run tests
            test_result = self.evaluator.run_test(eval_id, target_dir)
            
            logger.info(f"[{eval_id}] Passed: {test_result}")
            return {eval_id: test_result}
            
        except Exception as e:
            logger.error(f"[{eval_id}] Error: {str(e)}")
            return {eval_id: False}
    
    async def run_evals(self, batch_size: int = 10) -> Dict[str, bool]:
        """
        Run multiple evaluations in parallel.
        
        Args:
            batch_size: Number of evaluations to run
            
        Returns:
            Dictionary with all evaluation results
        """
        # Clean output directory
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Output directory prepared")
        
        # Run evaluations in parallel
        eval_tasks = []
        for i in range(batch_size):
            eval_id = str(i)
            eval_dir = "./evals/eval-001"
            eval_tasks.append(self.run_eval(eval_id, eval_dir))
        
        results = await asyncio.gather(*eval_tasks)
        
        # Merge results
        merged_results = {}
        for result in results:
            merged_results.update(result)
        
        # Generate HTML results
        html_results = self.evaluator.generate_results_html(merged_results)
        
        # Save results
        results_path = os.path.join(self.output_dir, "results.html")
        with open(results_path, "w", encoding="utf-8") as f:
            f.write(html_results)
        
        logger.info(f"Results saved to {results_path}")
        return merged_results

async def main():
    """Main entry point for the application."""
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        return
    
    # Initialize and run evaluations
    agent_eval = AgentEval(api_key=api_key)
    await agent_eval.run_evals(batch_size=10)

if __name__ == "__main__":
    asyncio.run(main())
