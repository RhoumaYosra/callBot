import os
from groq import Groq

client = Groq(
    api_key="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",
)

while True:
    # Pose une question à l'utilisateur
    user_question = input("Posez votre question (ou tapez 'quit' pour sortir) : ")

    # Vérifie si l'utilisateur veut quitter
    if user_question.lower() == "quit":
        break

    # Envoie la question à l'API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_question,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    # Affiche la réponse
    print(chat_completion.choices[0].message.content)
