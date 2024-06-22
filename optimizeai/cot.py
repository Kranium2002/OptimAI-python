"""This module defines the class for chain of thought"""

import dspy

class CoT(dspy.Module):
    """Chain of Thought class using dspy.Module for optimization."""
    def __init__(self, signature: dspy.Signature):
        super().__init__()
        self.prog = dspy.ChainOfThought(signature)

    def forward(self, code, perf_metrics):
        """Forward method to pass the code and performance metrics to the Chain of Thought model."""
        answer = self.prog(code=code, perf_metrics=perf_metrics)
        return answer