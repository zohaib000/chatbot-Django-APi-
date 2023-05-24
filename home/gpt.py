import os
import openai
import random

keyss = ["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"]


def find(query):
    try:

        openai.api_key = random.choice(keyss)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except:
        try:
            openai.api_key = random.choice(keyss)
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        except:
            try:
                openai.api_key = random.choice(keyss)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=query,
                    temperature=0.7,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
            except:
                return "I cannot provide you enough information due to restrictions."

    return response['choices'][0]['text']
