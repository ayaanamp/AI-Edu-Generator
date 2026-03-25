from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def generate_quiz(text):
    prompt = f"""
    Create 3 multiple choice questions from the following text.
    Each question should have 4 options and one correct answer.

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    text = input("Enter topic: ")
    result = generate_quiz(text)
    print("\nGenerated Quiz:\n")
    print(result)