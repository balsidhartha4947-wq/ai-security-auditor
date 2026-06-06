import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(\"OPENAI_API_KEY\")
)


def suggest_remediation(
    finding
):

    prompt = f\"\"\"
    Suggest secure remediation steps
    for this vulnerability:

    {finding}

    Include:
    - code-level fixes
    - best practices
    - safer alternatives
    \"\"\"\n
    response = client.chat.completions.create(
        model=\"gpt-5.5\",
        messages=[
            {
                \"role\": \"user\",
                \"content\": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
    )