# /your_project_root/app/api/__init__.py
# This file makes the 'api' directory a Python package.

# It can remain empty or be used for defining elements common to the API blueprints,
# such as custom error handlers specific to the API, base classes, or decorators.

# Example (Optional): Define a custom API error exception
# class ApiError(Exception):
#     status_code = 400
#
#     def __init__(self, message, status_code=None, payload=None):
#         super().__init__()
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload
#
#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         rv['error'] = self.__class__.__name__ # Or a more user-friendly error code
#         return rv

# Example (Optional): Register an error handler for the custom exception
# This would typically be done within the app factory or a dedicated error handling module
# from flask import jsonify
# def register_api_error_handler(app_or_bp):
#     @app_or_bp.errorhandler(ApiError)
#     def handle_api_error(error):
#         response = jsonify(error.to_dict())
#         response.status_code = error.status_code
#         return response

# If you define such handlers or exceptions here, you might register them
# in the app factory (__init__.py) after the blueprints are created/imported.
