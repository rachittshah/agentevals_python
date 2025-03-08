"""
Command-line interface for the AgentEval Python package.
"""

import os
import sys
import asyncio
import argparse
import logging
from pathlib import Path

from agenteval_python.main import AgentEval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="AgentEval - A framework for evaluating AI agents")
    parser.add_argument("--api-key", help="OpenAI API key (defaults to OPENAI_API_KEY environment variable)")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use for inference (defaults to gpt-3.5-turbo)")
    parser.add_argument("--output-dir", default="./output", help="Directory to store evaluation results")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of evaluations to run")
    parser.add_argument("--eval-dir", default="./evals/eval-001", help="Directory containing evaluation files")
    
    args = parser.parse_args()
    
    # Check if API key is provided or set in environment
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("API key must be provided or set as OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    # Initialize and run evaluations
    agent_eval = AgentEval(
        api_key=api_key,
        model=args.model,
        output_dir=args.output_dir
    )
    
    results = await agent_eval.run_evals(batch_size=args.batch_size)
    
    # Print summary
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    logger.info(f"Evaluation complete: {success_count}/{total_count} tests passed")
    logger.info(f"Results saved to {os.path.join(args.output_dir, 'results.html')}")

if __name__ == "__main__":
    asyncio.run(main())
