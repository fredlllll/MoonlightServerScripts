from Framework.Model import Model


class Number(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'numbers'

    def _get_fields(self):
        return [
            'value'
        ]

    @classmethod
    def modify_number(cls, number_model_id, change):
        cls.modify_numeric_field(number_model_id, 'value', change)
