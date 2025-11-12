from openai import OpenAI

def summarize_task(description: str) -> str:
    """Use the OpenAI Chat Completions API to summarize a paragraph-length task description."""
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes tasks briefly."},
            {"role": "user", "content": f"Summarize this task in a short phrase: {description}"}
        ]
    )

    return response.choices[0].message.content.strip()


def run():
    """Main entry point for uv run tasks4."""
    tasks = [
        "Develop a Python script that reads a JSON file of tasks, allows adding new ones through a command-line interface, and saves them persistently.",
        "Write a reflective summary of the entire CSC-299 project, explaining what was learned from using AI-coding assistants during development."
    ]

    print("\n=== Task Summaries ===")
    for desc in tasks:
        summary = summarize_task(desc)
        print(f"- {summary}")

