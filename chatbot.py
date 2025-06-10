from openai import OpenAI

client = OpenAI(
    api_key="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",
)
response = client.responses.create(
    model="gpt-4.1-mini",
    input="One random character",
    text={
        "format": {
            "type": "text"
        }
    },
    reasoning={},
    tools=[],
    temperature=1,
    max_output_tokens=20,
    top_p=1,
    store=True
)

print(response.output_text)
