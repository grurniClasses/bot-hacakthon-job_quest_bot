import openai


def get_company_info(name):
    openai.api_key = bot_settings.OPENAI_KEY
    location = 'Israel'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'Please tell me about the company named {name} located in {location}',

        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    text = ' ' + response.choices[0]["text"]
    lines = text.split('.')
    pretty_text = '\n'.join(lines).strip()
    print(f'>>> Information about {name}:\n', pretty_text)
    return pretty_text

