import gettext



LANGUAGES = ["uk","ru", "en", "es", "de", "kk"]


translations = {
    lang: gettext.translation(
        domain="messages", localedir="translations", languages=[lang], fallback=True
    )
    for lang in LANGUAGES
}

async def get_translator(lang: str):
    return translations.get(lang, translations["ru"])

# _ = get_translator()



# pybabel extract -o translations/messages.pot .
#
# pybabel init -i translations/messages.pot -d translations -l ru
#
# pybabel compile -d translations