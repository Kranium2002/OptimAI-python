# OptimAI

OptimAI is a powerful Python module designed to optimize your code by analyzing its performance and providing actionable suggestions. It leverages a large language model (LLM) to give you detailed insights and recommendations based on the profiling data collected during the execution of your code. This module supports various kinds of profilers from the [perfwatch package](https://github.com/Khushiyant/perfwatch).

## Features

- Custom decorators to optimize functions with ease.
- Integration with perfwatch for performance profiling.
- Capture and analyze stdout, function execution time, network usage, function calls, CPU/GPU usage, etc using [perfwatch](https://github.com/Khushiyant/perfwatch).
- Seamless integration with various LLMs for code optimization suggestions.
- Support for OpenAI, Google Gemini, HuggingFace (offline), ollama and Anthropic.
- Optimized prompts for best performance on any LLM using [dspy](https://github.com/stanfordnlp/dspy)

## Installation

You can install OptimAI using pip:

```bash
pip install optimizeai
```

## Setup

To use OptimAI, you need to configure it with your preferred LLM provider and API key. Supported LLM providers include Google (Gemini models), OpenAI, Ollama, HuggingFace and Anthropic. For Ollama you need to have Ollama installed and the model artifacts also need to be downloaded previously.

1. **Select the LLM Provider**:
    - For Google Gemini models: `llm = "google"`
    - For OpenAI models: `llm = "openai"`
    - For Hugging Face offline: `llm = "huggingface"`
    - For Anthropic models: `llm = "anthropic"`
    - For local Ollama models: `llm = "ollama"`

2. **Choose the Model**:
    - Example: `model = "gpt-4"`, `model = "gemini-1.5-flash"`, `model = "codegemma"`,  or any other model specific to the chosen LLM provider.

3. **Set the API Key**:
    - Use the corresponding API key for the selected LLM provider. No API key required for local Huggingface Inference and Ollama.

## Sample Code

Here's a basic example demonstrating how to use OptimAI to optimize a function:

```python
from optimizeai.decorators.optimize import optimize
from optimizeai.config import Config
from dotenv import load_dotenv
import time
import os

# Load environment variables
load_dotenv()
llm = os.getenv("LLM")
key = os.getenv("API_KEY")
model = os.getenv("MODEL")

# Configure LLM
llm_config = Config(llm=llm, model=model, key=key)
perfwatch_params = ["line", "cpu", "time"]

# Define a test function to be optimized
@optimize(config=llm_config, profiler_types=perfwatch_params)
def test():
    for _ in range(10):
        time.sleep(0.1)
        print("Hello World!")
        pass

if __name__ == "__main__":
    test()
```

### Setting Environment Variables

You can set the environment variables (`LLM`, `API_KEY`, `MODEL`) in a `.env` file for ease of use:

```
LLM=google
API_KEY=your_google_api_key
MODEL=gemini-1.5-flash
```

## Upcoming Features

- **Improved Context for Code Optimization**: Enhance the context provided to the LLM for more accurate and relevant optimization recommendations.
- **Report Generation**: Proper optimization report will be generated.
- **Support for a Better Config**: A better config support is coming through which you can set various llm parameters. 

## Contributing

We welcome contributions to OptimAI! If you have an idea for a new feature or have found a bug, please open an issue on GitHub. If you'd like to contribute code, please fork the repository and submit a pull request.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

OptimAI is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
