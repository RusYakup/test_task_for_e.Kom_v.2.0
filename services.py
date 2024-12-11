import logging
import traceback

from models import FieldType

log = logging.getLogger(__name__)


class FormService:
    def __init__(self, form_repository):
        self.form_repository = form_repository
        print(self.form_repository)

    async def process_request(self, request):
        try:
            data = dict(request.query_params)
            if not data or len(data) == 0:
                log.error("No data in request")
                return {"error": "No data in request"}

            forms = await self.form_repository.find_by_fields(data)

            if forms:
                log.info(f"Form found: {forms.get('form_name')}")
                return forms

            log.info('No matching form found.')

            typed_fields = {}
            for field, value in data.items():
                typed_fields[field] = FieldType(value).get_type()

            log.info(f"Typed fields: {typed_fields}")
            return typed_fields

        except Exception as e:
            log.error(f"Error: {str(e)}")
            log.error(traceback.format_exc())
            return {"error": "Error processing request"}
