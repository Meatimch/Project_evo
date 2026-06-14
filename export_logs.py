import os
from datetime import datetime


def save_logs(logs: list[str], logs_dir: str | None = None) -> str:
    """Save list of log strings to a timestamped file in logs_dir.

    Returns the path to the created file.
    """
    if logs_dir is None:
        # assume project root is parent of this file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
        logs_dir = os.path.join(project_root, "logs")

    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs_{timestamp}.txt"
    path = os.path.join(logs_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        for line in logs:
            f.write(str(line) + "\n")

    return path
