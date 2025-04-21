pybabel extract -o trans/messages.pot aio/

pybabel init -i trans/messages.pot -d trans -l ru 
pybabel init -i trans/messages.pot -d trans -l en
pybabel init -i trans/messages.pot -d trans -l uk
pybabel init -i trans/messages.pot -d trans -l es
pybabel init -i trans/messages.pot -d trans -l de




msgfmt trans/en/LC_MESSAGES/messages.po -o trans/en/LC_MESSAGES/messages.mo



pybabel compile -d trans

