from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success


class EnvelopeJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        # Fallback for edge cases where response is missing
        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        status_code = response.status_code
        success = is_success(status_code)

        # 1. ESCAPE HATCH: If the view already structured the dictionary perfectly,
        # let it pass through without double-wrapping.
        if isinstance(data, dict) and 'success' in data and 'data' in data:
            return super().render(data, accepted_media_type, renderer_context)

        # 2. DEFAULT WRAPPER: Wrap standard DRF data into your requested envelope.
        enveloped_data = {
            "success": success,
            "data": data if success else None,
            "client_msg": "Operation successful" if success else "An error occurred",
            "dev_msg": ""
        }

        # Handle DRF error responses (like 400 Bad Request validation errors)
        if not success:
            enveloped_data["data"] = data  # Keeps form validation errors in 'data'
            enveloped_data["dev_msg"] = f"HTTP {status_code} Error"

        return super().render(enveloped_data, accepted_media_type, renderer_context)