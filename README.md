# upd8 ninja

Homestuck^2 update checker using a central server to reduce overall load on Homestuck's servers

## website

https://upd8.tjb0607.me/

## API

The upd8ninja.py file generates a json file located at https://upd8.tjb0607.me/latestupd8.json, formatted as such:

    {"parturl": "story/1", "title": "Somewhere, in the distant reaches of space...", "pages": 32}

The parturl is appended to https://homestuck2.com/ by the frontend to create a complete link.
