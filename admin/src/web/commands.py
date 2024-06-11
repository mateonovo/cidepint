from src.core import database, seeds


def register_commands(app):

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()

    @app.cli.command(name="servicesdb")
    def servicesdb():
        seeds.run_services()

    @app.cli.command(name="apidb")
    def apidb():
        seeds.run_api()
