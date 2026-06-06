from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv(\"OPENAI_API_KEY\")
)


def create_investigation_plan(
    findings
):

    prompt = f\"\"\"
    You are a security planning agent.

    Analyze findings and prioritize:
    - critical vulnerabilities
    - risky attack surfaces
    - likely exploit chains

    Findings:
    {findings}
    \"\"\"

    response = client.chat.completions.create(
        model=\"gpt-5.5\",
        messages=[
            {
                \"role\": \"user\",
                \"content\": prompt
            }
        ]
    )

    return response.choices[0].message.content