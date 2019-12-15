class SelectiveIterator:
    def __init__(self, entity, fields):
        self.entity = entity
        self.fields = fields
        self.current_field = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_field < (len(self.fields) - 1):
            self.current_field += 1
            field_name = self.fields[self.current_field]
            return getattr(self.entity, field_name)
        else:
            raise StopIteration()
