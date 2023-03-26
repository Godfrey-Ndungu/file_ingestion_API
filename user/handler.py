from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call the default exception handler first to get the response object
    response = exception_handler(exc, context)

    # Check if a response was generated
    if response is not None:
        # Check for 404 error
        if response.status_code == status.HTTP_404_NOT_FOUND:
            message = "The requested resource could not be found."
        # Check for 500 error
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            message = (
                "An internal server error occurred. Please try again later."  # noqa
            )
        # For all other errors
        else:
            message = "An error occurred while processing your request. Please try again later."  # noqa

        # Create the response data with custom error message
        response.data = {
            "error": True,
            "status_code": response.status_code,
            "message": message,
        }

    return response
