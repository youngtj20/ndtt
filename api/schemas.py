from rest_framework.schemas import ManualSchema
from rest_framework.schemas import AutoSchema
import coreapi
import coreschema
from urllib import parse

class CustomAutoSchema(AutoSchema):
    # self.view.action to get view action name
    
    def get_manual_fields(self, path, method):
        custom_fields =[]
        if self.view.action in ['create', 'update', 'partial_update']:
            return self._manual_fields
    
    def get_link(self, path, method, base_url):
        """
        Generate `coreapi.Link` for self.view, path and method.
        This is the main _public_ access point.
        Parameters:
        * path: Route path for view from URLConf.
        * method: The HTTP request method.
        * base_url: The project "mount point" as given to SchemaGenerator
        """
        # fields = self.get_path_fields(path, method)
        # fields += self.get_serializer_fields(path, method)
        # fields += self.get_pagination_fields(path, method)
        # fields += self.get_filter_fields(path, method)
        fields = None

        manual_fields = self.get_manual_fields(path, method)
        # override fields here
        # if self.view.action in ['create', 'update', 'partial_update']:
        #     fields = manual_fields
        # else:
        fields = self.update_fields(self.get_path_fields(path, method), manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=parse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )

# what use have i got for you?
def get_extra_fields(fields):
    return [
        coreapi.Field(
            f.field_name,
            required=f.required,
            location='form',
            schema=coreschema.String()
        ) for f in fields
    ]

booking_endpoint = ManualSchema([
    coreapi.Field(
        'title',
        required=False,
        location='form',
        schema=coreschema.String(description='Candidate title, e.g Mr, Chief')
    ),
    coreapi.Field(
        'first_name',
        required=True,
        location='form',
        schema=coreschema.String(description='Candidate first name')
    ),
    coreapi.Field(
        'last_name',
        required=True,
        location='form',
        schema=coreschema.String(description='Candidate Last name')
    ),
    coreapi.Field(
        'middle_name',
        required=False,
        location='form',
        schema=coreschema.String(description='candidate middle name')
    ),
    coreapi.Field(
        'state',
        required=True,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'mobile_number',
        required=True,
        location='form',
        schema=coreschema.String(description='Candidate Phone Number')
    ),
    coreapi.Field(
        'email_address',
        required=False,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'address',
        required=False,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'date_of_birth',
        required=True,
        location='form',
        schema=coreschema.String(description='DoB format yy-mm-dd e.g "2009-01-11"')
    ),
    coreapi.Field(
        'gender',
        required=True,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'preferred_date',
        required=True,
        location='form',
        schema=coreschema.String(description='Date to take test')
    ),
    coreapi.Field(
        'drive_test_type',
        required=False,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'exam_preferred_language',
        required=False,
        location='form',
        schema=coreschema.String(description='Candidate language of choice')
    ),
    coreapi.Field(
        'photo',
        required=False,
        location='form',
        schema=coreschema.String(description='Candidate photo')
    ),
    coreapi.Field(
        'card_number',
        required=True,
        location='form',
        schema=coreschema.String(description='Scratch card pin number. max_length=50, unique')
    ),
    coreapi.Field(
        'examination_number',
        required=True,
        location='form',
        schema=coreschema.String(description='Candidate exam number, unique, max_length=10')
    ),
    coreapi.Field(
        'exam_category',
        required=True,
        location='form',
        schema=coreschema.String(description='')
    ),
    coreapi.Field(
        'exam_venue',
        required=True,
        location='form',
        schema=coreschema.String(description='')
    )
])
