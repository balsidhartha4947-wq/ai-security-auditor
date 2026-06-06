from openai import OpenAI
from openai import APIError, RateLimitError
from fastapi import HTTPException

client = OpenAI()


def analyze_finding(finding: dict):

    try:

        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[
                {
                    "role": "user",
                    "content": str(finding)
                }
            ]
        )

        return response.choices[0].message.content

    except RateLimitError:

        raise HTTPException(
            status_code=429,
            detail="AI rate limit exceeded"
        )

    except APIError:

        raise HTTPException(
            status_code=500,
            detail="AI provider failure"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unexpected AI analysis error"
        )