from src.modules.hive_db.routes import routes as hive_db_routes

api_routes = [
    hive_db_routes,
]

def register_routes(routes, app, prefix=None):
    for module in routes:
        for route in module:
            if prefix:
                app.add_route(f'/{prefix}/{route[0]}', route[1])
            else:
                app.add_route(f'/{route[0]}', route[1])
