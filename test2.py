import pyttsx3

def main():
    # Initialiser le moteur TTS
    engine = pyttsx3.init()

    # Définir la voix et les paramètres de la voix
    engine.setProperty('voice', 'French')
    engine.setProperty('rate', 170)  # Vitesse de la voix
    engine.setProperty('volume', 0.8)  # Volume de la voix

    # Texte à convertir en parole
    text = "Comment développer sa culture générale ? Et bien, même avant de répondre à cette question, pourquoi la développer ? " \
           "À quoi sert la culture générale ? Ça sert juste à se la jouer ou à briser la glace, à se rapprocher d'un client, à développer " \
           "une culture commune auprès de ses enfants, à leur laisser un héritage, qui aura d'ailleurs plus de valeur parfois qu'un héritage " \
           "matériel, un héritage purement immatériel, la culture générale. C'est une de mes passions, et dans cette Masterclass, je vous " \
           "apprends à quoi elle sert, donc pourquoi la développer ? Comment la développer avec des exercices pratiques qui sont applicables, " \
           "absolument à n'importe qui, que vous soyez timide, ou que vous manquiez de curiosité, que vous soyez démotivés ? Je vous garantis " \
           "que les exercices qu'on vous donne dans cette Masterclass sont faits pour vous, pourquoi, comment et enfin, quoi mettre dans sa " \
           "culture générale, quelles sources utiliser, comment faire un bon repas de connaissance ? Où trouver une gastronomie des savoirs, " \
           "des histoires, des biographies, des éléments liés au cinéma et à tous les arts ? Comment, pourquoi et quoi, c'est ce que nous " \
           "aborderons dans cette Masterclass sur la culture générale. Je suis Idrisa Bercan, et ceci est ma Masterclass."

    # Générer la parole à partir du texte et enregistrer dans un fichier audio
    engine.save_to_file(text, "output.mp3")
    engine.runAndWait()

if __name__ == "__main__":
    main()
