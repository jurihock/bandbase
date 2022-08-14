from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi import status as STATUS

import bandbase.core.common
import bandbase.core.database
import bandbase.core.security
import bandbase.utils.sql as SQL

from bandbase.schemas.database import *
from bandbase.schemas.files import *


router = APIRouter(prefix='/contact', tags=['files', 'contacts'])


@router.get('/{id}.vcf', dependencies=[Depends(bandbase.core.security.ssl), Depends(bandbase.core.security.auth)],
                         response_class=VcfResponse)
def vcf(id: int, logger: bandbase.core.common.Logger = Depends(bandbase.core.common.logger)):

    try:

        with bandbase.core.database.session() as db:

            contact = db.query(Contact).get(id)

            if not contact:

                raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND)

            contactAddress = '{0} {1}'.format(contact.Street, contact.HouseNumber or '').strip() \
                                       if contact.Street else None

            vcf = \
            [
                'BEGIN:VCARD',

                'VERSION:3',

                'FN:{0}'.format(contact.Name),
                'N:{0};{1};;;'.format(contact.LastName, contact.FirstName or ''),

                'BDAY:{0:04}-{1:02}-{2:02}'.format(contact.BirthDate.year, contact.BirthDate.month, contact.BirthDate.day) \
                                            if contact.BirthDate else None,

                'ADR:;;{0};{1};;{2};{3}'.format(contactAddress or '', contact.City or '', contact.PostalCode or '', contact.Country or '') \
                                         if contactAddress or contact.City or contact.PostalCode or contact.Country else None,

                'TEL;TYPE=VOICE:{0}'.format(contact.LandlinePhone) if contact.LandlinePhone else None,
                'TEL;TYPE=CELL:{0}'.format(contact.MobilePhone) if contact.MobilePhone else None,
                'TEL;TYPE=FAX:{0}'.format(contact.Fax) if contact.Fax else None,
                'EMAIL:{0}'.format(contact.EMail) if contact.EMail else None,
                'URL:{0}'.format(contact.WWW) if contact.WWW else None,

                'GEO:{0};{1}'.format(contact.Latitude, contact.Longitude) \
                              if contact.Latitude and contact.Longitude else None,

                'ORG:{0}'.format('Big Band „Brandheiß“ Pforzheim'),
                'ROLE:{0}'.format(contact.Category.Name),

                'NOTE:{0}'.format(contact.Comment) if contact.Comment else None,

                'END:VCARD'
            ]

            content = '\n'.join([entry for entry in vcf if entry])
            filename = contact.Name

            return VcfResponse(content=content, filename=filename)

    except HTTPException as e:
        raise e

    except Exception as e:

        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to create the VCF file: {e}')
