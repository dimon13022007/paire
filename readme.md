pybabel extract -o translations/messages.pot aio/

pybabel init -i translations/messages.pot -d translations -l ru
pybabel init -i translations/messages.pot -d translations -l en
pybabel init -i translations/messages.pot -d translations -l uk
pybabel init -i translations/messages.pot -d translations -l es
pybabel init -i translations/messages.pot -d translations -l de
pybabel init -i translations/messages.pot -d translations -l kk
pybabel init -i translations/messages.pot -d translations -l ky
pybabel init -i translations/messages.pot -d translations -l it



msgfmt translations/en/LC_MESSAGES/messages.po -o translations/en/LC_MESSAGES/messages.mo
msgfmt translations/it/LC_MESSAGES/messages.po -o translations/it/LC_MESSAGES/messages.mo
msgfmt translations/ky/LC_MESSAGES/messages.po -o translations/ky/LC_MESSAGES/messages.mo
msgfmt translations/es/LC_MESSAGES/messages.po -o translations/es/LC_MESSAGES/messages.mo
msgfmt translations/de/LC_MESSAGES/messages.po -o translations/de/LC_MESSAGES/messages.mo
msgfmt translations/uk/LC_MESSAGES/messages.po -o translations/uk/LC_MESSAGES/messages.mo
msgfmt translations/kk/LC_MESSAGES/messages.po -o translations/kk/LC_MESSAGES/messages.mo



pybabel extract -o translations/messages.pot aio/handlers/like_handlers.py
pybabel extract -o translations/messages.pot aio/func/func_profile.py

pybabel compile -d translations
