import os

from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from truckpad_api.app import app

manager = Manager(app)
server = Server(host="0.0.0.0", port=os.getenv('PORT', 8080))
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
