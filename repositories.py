import logging
import motor

log = logging.getLogger(__name__)


class FormRepository:
    def __init__(self, async_form_collection: motor.motor_asyncio.AsyncIOMotorCollection) -> None:
        """
        Initialize a FormRepository with an async_form_collection.

        :param async_form_collection: An async collection for storing forms.
        :type async_form_collection: motor.motor_asyncio.AsyncIOMotorCollection
        :return: None
        :rtype: None
        """
        self.async_form_collection = async_form_collection

    async def find(self):
        forms = await self.async_form_collection.find().to_list(None)
        log.debug(f'Defining forms: {forms}')
        return forms

    async def find_by_fields(self, request_data):
        forms = await self.find()
        for form in forms:
            form_fields = form.get('fields', {})
            missing_fields = [field for field in form_fields if field not in request_data]
            if missing_fields:
                log.warning(f'Missing fields in request: {missing_fields}')
                continue

            if all(request_data.get(field, '').strip() for field in form_fields):
                log.info(f'Form found: {form.get("name")}')
                return {"form_name": form.get('name')}

        log.info('No matching form found.')
        return None