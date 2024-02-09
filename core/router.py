import uuid
from typing import Callable
from core.view import View
from core.context import Context, UpdateType
import logging


class Request:
    def __init__(self, route: str, params: dict[str, str]):
        self.route = route
        self.params = params


class Route:
    def __init__(self, path: str, handler: Callable[[Request], Callable[[Context], View]], type: UpdateType):
        self.path = path
        self.handler = handler
        self.type = type


class Router:
    def __init__(self):
        self.unique_id = uuid.uuid4()
        self.routes: list[Route] = []

    def register_command(self, command):
        def decorator(func):
            route = Route(command, lambda req: func, UpdateType.Command)
            self.routes.append(route)
            return func
        return decorator

    def register_callback(self, callback):
        def decorator(func):
            route = Route(callback, lambda req: func, UpdateType.Callback)
            self.routes.append(route)
            return func
        return decorator

    def get_route(self, context: Context):
        routes = self.get_routes(context.type)
        current_route_path = None
        if context.type is UpdateType.Command:
            current_route_path = context.message.text.split()[0][1:]
        if context.type is UpdateType.Callback:
            current_route_path = context.callback.data

        if not current_route_path:
            return None, None
        for route in routes:
            if self.is_match(route.path, current_route_path):
                return current_route_path, route
        return None, None

    def handle(self, context: Context):
        current_route_path, route = self.get_route(context)
        if not route or not current_route_path:
            logging.info("Route not found for %s. Current route path: %s. Route: %s",
                         context, current_route_path, route)
            return None
        logging.info("For requested route path '%s' found route '%s' for '%s'.",
                     current_route_path, route.path, context)

        request = Request(current_route_path, self.extract_dynamic_params(route.path, current_route_path))

        controller_action = route.handler(request)

        if not controller_action:
            logging.info("Controller action not found for route '%s'.", route.path)
            return None

        logging.info("Controller action '%s' found for route '%s'.", controller_action, route.path)
        view = controller_action(context)

        if not view:
            logging.warning("Controller action resulted with no view. %s", controller_action)
            return None

        if context.type is UpdateType.Command:
            context.bot.respond_to(context.message, view.get_text(), reply_markup=view.get_keyboard(),
                                   parse_mode=view.parse_mode)
        if context.type is UpdateType.Callback:
            context.bot.edit_menu(context.callback, view.get_text(), view.get_keyboard(),
                                  parse_mode=view.parse_mode)

    def get_routes(self, update_type: UpdateType) -> list[Route]:
        return [route for route in self.routes if route.type == update_type]

    def extract_dynamic_params(self, route_path, requested_path):
        route_path_parts = route_path.split('/')
        requested_path_parts = requested_path.split('/')

        dynamic_params = {}

        for route_part, requested_part in zip(route_path_parts, requested_path_parts):
            if '{' in route_part and '}' in route_part:
                param_name = route_part.strip('{}')
                dynamic_params[param_name] = requested_part

        return dynamic_params

    def is_match(self, route_path, requested_path):
        route_path_parts = route_path.split('/')
        requested_path_parts = requested_path.split('/')

        if len(route_path_parts) != len(requested_path_parts):
            return False

        for route_part, requested_part in zip(route_path_parts, requested_path_parts):
            if '{' in route_part and '}' in route_part:
                continue  # Skip dynamic parts
            elif route_part != requested_part:
                return False

        return True


router = Router()
