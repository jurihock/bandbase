from fastapi import Response


class VcfResponse(Response):
    def __init__(self, content: str, filename: str):
        super().__init__(
            content=content,
            headers={'Content-Disposition': f'attachment;filename="{filename}.vcf"'},
            media_type='text/vcard')
