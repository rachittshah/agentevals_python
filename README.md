# AgentEval Python Implementation with LiteLLM

This is a Python implementation of the [AgentEval](https://github.com/jamesmurdza/agenteval) framework, which allows for automated testing of AI agents through integration tests and Monte Carlo simulations. This implementation uses LiteLLM for LLM inference.

## Installation

```bash
pip install -e .
```

## Requirements

- Python 3.7+
- LiteLLM
- Selenium
- webdriver-manager

## Usage

### Setting up your environment

First, set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

### Directory Structure

Each evaluation contains:

- `app/`: The codebase before transformation
- `prompt.md`: A description of the transformation to be made
- `solution/`: The canonical solution with the complete codebase transformed

Example:
```
evals/
  eval-001/
    app/
      index.html
    prompt.md
    solution/
      index.html
```

### Running Evaluations

To run evaluations:

```python
import asyncio
from agenteval_python.main import AgentEval

async def run():
    agent_eval = AgentEval()
    results = await agent_eval.run_evals(batch_size=10)
    print(results)

if __name__ == "__main__":
    asyncio.run(run())
```

## Components

### CodegenAgent

The `CodegenAgent` class is responsible for modifying code based on prompts using LiteLLM for inference.

```python
from agenteval_python.agent import CodegenAgent

agent = CodegenAgent(api_key="your-api-key", model="gpt-3.5-turbo")
modified_code = await agent.modify_code(source_code, prompt)
```

### Evaluator

The `Evaluator` class tests agent-modified code using Selenium.

```python
from agenteval_python.evaluator import Evaluator

evaluator = Evaluator(output_dir="./output")
test_result = evaluator.run_test(eval_id, target_dir)
```

### AgentEval

The `AgentEval` class is the main entry point for running evaluations.

```python
from agenteval_python.main import AgentEval

agent_eval = AgentEval(api_key="your-api-key", model="gpt-3.5-turbo")
results = await agent_eval.run_evals(batch_size=10)
```

## Testing

To run tests:

```bash
python test.py
```

## License

This project is licensed under the MIT License.
