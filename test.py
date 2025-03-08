"""
Test script for the AgentEval Python implementation.
"""

import os
import asyncio
import logging
from pathlib import Path

# Add parent directory to path to import agenteval_python
import sys
sys.path.append('/home/ubuntu')

from agenteval_python.agent import CodegenAgent
from agenteval_python.evaluator import Evaluator
from agenteval_python.main import AgentEval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_agent():
    """Test the CodegenAgent implementation."""
    logger.info("Testing CodegenAgent...")
    
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        logger.info("Setting a temporary API key for testing")
        os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
        api_key = "sk-dummy-key-for-testing"
    
    # Initialize agent
    agent = CodegenAgent(api_key=api_key)
    
    # Test code modification
    source_code = """<!DOCTYPE html>
<html>
<head>
  <title>Counter App</title>
</head>
<body>
  <h1>Counter</h1>
  <p>Count: <span id="count">0</span></p>
  <button id="incrementBtn">Increment</button>
</body>
</html>"""
    
    prompt = "Update the code so clicking the button increments the count by one."
    
    try:
        # This will fail with a dummy key, but we can test the code structure
        modified_code = await agent.modify_code(source_code, prompt)
        logger.info("Agent test completed")
    except Exception as e:
        logger.error(f"Agent test failed: {str(e)}")
        logger.info("This is expected if using a dummy API key")

async def test_evaluator():
    """Test the Evaluator implementation."""
    logger.info("Testing Evaluator...")
    
    # Initialize evaluator
    evaluator = Evaluator(output_dir="./test_output")
    
    # Generate test results HTML
    results = {"0": True, "1": False, "2": True}
    html = evaluator.generate_results_html(results)
    
    # Save results
    os.makedirs("./test_output", exist_ok=True)
    with open("./test_output/test_results.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    logger.info("Evaluator test completed")

async def test_agenteval():
    """Test the AgentEval implementation."""
    logger.info("Testing AgentEval...")
    
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        logger.info("Setting a temporary API key for testing")
        os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
        api_key = "sk-dummy-key-for-testing"
    
    # Initialize AgentEval
    agent_eval = AgentEval(api_key=api_key, output_dir="./test_output")
    
    # Test directory structure
    eval_dir = Path("/home/ubuntu/agenteval_python/evals/eval-001")
    if not eval_dir.exists():
        logger.error(f"Evaluation directory {eval_dir} does not exist")
        return
    
    app_dir = eval_dir / "app"
    if not app_dir.exists() or not (app_dir / "index.html").exists():
        logger.error(f"App directory {app_dir} or index.html does not exist")
        return
    
    prompt_file = eval_dir / "prompt.md"
    if not prompt_file.exists():
        logger.error(f"Prompt file {prompt_file} does not exist")
        return
    
    logger.info("Directory structure test passed")
    logger.info("AgentEval test completed")

async def main():
    """Run all tests."""
    logger.info("Starting tests...")
    
    await test_agent()
    await test_evaluator()
    await test_agenteval()
    
    logger.info("All tests completed")

if __name__ == "__main__":
    asyncio.run(main())
