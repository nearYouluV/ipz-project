# In your converters.py (or you can place this in any module)

class DateConverter:
    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        from datetime import datetime
        return datetime.strptime(value, "%Y-%m-%d").date()  # Convert the string to a date object

    def to_url(self, value):
        return value.strftime("%Y-%m-%d")  # Convert a date object back to the 'YYYY-MM-DD' format
