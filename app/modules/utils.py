import torch
from transformers import pipeline
from transformers.pipelines.base import Pipeline


def load_model(task: str, model: str) -> Pipeline:
    """Loads the given transformers model based on the given task

    Args:
        task (str): NLP task
        model (str): transformers model

    Returns:
        Pipeline: transformers pipeline object
    """
    return pipeline(
        task=task, 
        model=model, 
        device = 0 if torch.cuda.is_available() else -1
    )