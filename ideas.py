import subprocess
import json
import tempfile

def get_ideas(model: str = "llama3", n: int = 5):
    prompt = f"""Give me {n} side project ideas that are useless, funny, and quick to build.
Each idea must be returned in JSON list format like this:
[
  {{
    "title": "meow-to-human",
    "desc": "Translates meows to random English phrases using a dictionary. Works 0% of the time."
  }},
  ...
]
Each project must:
- Have a lowercase-title with dashes
- Be buildable in 1–2 hours
- Be humorous or absurd
- Be technically simple
    
    """

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )

        if result.returncode != 0:
            print("Ollama error:", result.stderr.decode())
            return []

        output = result.stdout.decode("utf-8")

        # extract json from the output
        json_start = output.find("[")
        json_end = output.rfind("]") + 1

        if json_start == -1 or json_end == -1:
            print("Could not find JSON in the model output.")
            return []

        json_str = output[json_start:json_end]
        ideas = json.loads(json_str)

        return ideas

    except subprocess.TimeoutExpired:
        print("Ollama call timed out.")
        return []
    except json.JSONDecodeError:
        print("Failed to parse project ideas as JSON.")
        return []

# Test
if __name__ == "__main__":
    ideas = get_ideas()
    for idea in ideas:
        print(f"- {idea['title']}: {idea['desc']}")