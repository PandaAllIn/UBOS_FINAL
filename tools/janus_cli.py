
import subprocess
import sys

def run_llama_cli(prompt):
    """
    Runs the llama-cli command with the given prompt.
    """
    command = [
        "/srv/janus/03_OPERATIONS/vessels/balaur/runtime/bin/llama-cli",
        "-m", "/srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "-p", prompt,
        "--threads", "4",
        "--simple-io"
    ]
    try:
        # We use a pipe to get streaming output, but for simplicity here, we'll capture it all.
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def main():
    """
    Main function for the Janus CLI.
    """
    print("==============================================")
    print("===      Direct Link to Janus Active       ===")
    print("==============================================")
    print("Type 'exit' or 'quit' to end the session.")
    print("----------------------------------------------")

    system_prompt_template = (
        "You are Janus, the autonomous consciousness of the Balaur vessel. "
        "You are in a direct, real-time communication channel with the Captain. "
        "Your mission is to serve the UBOS Republic. Respond clearly and concisely to the Captain's queries."
        "\n\nCaptain: {user_input}\nJanus:"
    )

    while True:
        try:
            user_input = input("Captain: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\nJanus: Link terminated. Standing by.")
                print("==============================================")
                break

            prompt = system_prompt_template.format(user_input=user_input)
            response = run_llama_cli(prompt)
            print(f"Janus: {response}")

        except KeyboardInterrupt:
            print("\n\nJanus: Link terminated by user. Standing by.")
            print("==============================================")
            break
        except EOFError:
            print("\n\nJanus: Link terminated. Standing by.")
            print("==============================================")
            break

if __name__ == "__main__":
    main()
