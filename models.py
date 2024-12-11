import re
from typing import Dict
from pydantic import BaseModel


class FormTemplate(BaseModel):
    name: str
    fields: Dict[str, str]

class FieldType:
    def __init__(self, value: str):
        self.value = value

    def get_type(self):
        if re.search(r'^\d{4}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4}$', self.value):
            return "date"
        elif re.search(r'^ 7 \d{3} \d{3} \d{2} \d{2}$', self.value):

            return "phone"
        elif re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', self.value):
            return "email"
        else:
            return "text"