from flask_script import Manager
from flask_health import app
from flask_health.scripts.db import InitDB, SeedDB


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command("init_db", InitDB())
    manager.add_command("seed_db", SeedDB())
    manager.run()
