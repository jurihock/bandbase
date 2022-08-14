from fastapi import Response
from fastapi import status as STATUS


class VcfResponse(Response):
    def __init__(self, content: str, filename: str, status_code: int = STATUS.HTTP_200_OK):
        super().__init__(
            content=content,
            headers={'Content-Disposition': f'attachment;filename="{filename}.vcf"'},
            media_type='text/vcard',
            status_code=status_code)
