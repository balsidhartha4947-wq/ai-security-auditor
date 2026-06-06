import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(\"OPENAI_API_KEY\")
)


def analyze_security_issue(
    finding,
    related_context
):

    prompt = f\"\"\"
    You are a senior security analyst.

    Analyze this finding:

    {finding}

    Related context:

    {related_context}

    Explain:
    - vulnerability type
    - impact
    - exploitability
    - severity
    - attack scenario
    \"\"\"\n
    response = client.chat.completions.create(
        model=\"gpt-5.5\",
        messages=[
            {
                \"role\": \"user\",
                \"content\": prompt
            }
        ],
        temperature=0.2
    )

    return (
        response
        .choices[0]
        .message
        .content
    )