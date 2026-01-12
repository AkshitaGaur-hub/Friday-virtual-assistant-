import subprocess

SYSTEM_PROMPT = (
    "You are a virtual assistant named Friday, "
    "skilled in general tasks like Alexa."
)

def ask_ai(user_prompt):
    full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_prompt}\nFriday:"
    
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=full_prompt,
        text=True,
        capture_output=True
    )
    
    return result.stdout.strip()


# Example usage
response = ask_ai("What is coding?")
print(response)
