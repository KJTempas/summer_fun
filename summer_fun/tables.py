import django_tables2 as tables

class StudentTable(tables.Table):
    class Meta:
        model = Student