from pathlib import Path
from datetime import datetime
from app.agent import Agent

TESTS = [
    "List all files in the project.",
    "List all Python functions.",
    "List all classes in the project.",
    "List all imports in the project.",
    "Read hello.py.",
    "Read greet.py.",
    "Read calculator.py.",
    "Explain hello.py.",
    "Explain greet.py.",
    "Review calculator.py.",
    'Search for "Hello".',
    'Search for "Goodbye".',
    "Show me the source code of the greet function.",
    "Run hello.py.",
    "Run greet.py.",
    "Where is Calculator defined?",
    "Where is greet() used?",
    "How do greet.py and hello.py relate?",
    "Describe this project.",
    "Explain how greet.py works internally.",
]



def main():

    agent = Agent()

    total = len(TESTS)

    results_dir = Path("eval_results")
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_file = results_dir / f"{timestamp}.txt"

    with output_file.open("w", encoding="utf-8") as f:

        for index, prompt in enumerate(TESTS, start=1):

            header = (
                "\n"
                + "=" * 80
                + f"\n[{index}/{total}] {prompt}\n"
                + "=" * 80
                + "\n"
            )

            print(header, end="")
            f.write(header)

            try:

                response = agent.chat(prompt)

            except Exception as e:

                response = f"ERROR: {e}"

                print(response)
                f.write(response + "\n")

                break

            print(response)
            f.write(response + "\n")

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
