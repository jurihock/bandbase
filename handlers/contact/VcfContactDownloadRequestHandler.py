from app import app

from handlers.common import *
from parsers.contact import *
from utils.models import *

import utils.logger as logger
import utils.flash as flash
import utils.filters as filters
import utils.request as request
import utils.response as response
import utils.database as database

class VcfContactDownloadRequestHandler(RequestHandler):

    def handle_get(self):

        with database.session() as db:

            contact = db.query(Contact).get(self.id)

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

            vcf = '\n'.join([entry for entry in vcf if entry])

            return response.vcf(vcf, contact.Name + '.vcf')
