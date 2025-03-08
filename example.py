"""
Example script for running AgentEval.
"""

import os
import asyncio
import logging
from agenteval_python.main import AgentEval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """Run AgentEval with default settings."""
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        return
    
    # Initialize and run evaluations
    agent_eval = AgentEval(api_key=api_key)
    results = await agent_eval.run_evals(batch_size=10)
    
    # Print summary
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    logger.info(f"Evaluation complete: {success_count}/{total_count} tests passed")

if __name__ == "__main__":
    asyncio.run(main())
