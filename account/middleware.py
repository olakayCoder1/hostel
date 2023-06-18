from django.template.response import TemplateResponse 

class HostelListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        # Get the response from the next middleware or view
        response = self.get_response(request)
        # Process the response
        if hasattr(response, 'context_data'): 
            print(hasattr(response, 'context'))
            # Add data to the context
            response.context_data['custom_data'] = 'Custom Data'  

        return response
