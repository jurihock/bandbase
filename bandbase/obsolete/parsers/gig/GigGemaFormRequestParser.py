from parsers.common import *
from utils.models import *

class GigGemaFormRequestParser(RequestParser):

    def parse(self, gig):

        gig.SetlistMeta.BandName = self.str('band_name')
        gig.SetlistMeta.BandLeaderID = self.str('band_leader')
    
        gig.SetlistMeta.GemaMembershipNumber = self.str('gema_membership_number')
        gig.SetlistMeta.GemaCustomerNumber = self.str('gema_customer_number')

        gig.SetlistMeta.EngrosserSignaturePlace = self.str('engrosser_signature_place')
        gig.SetlistMeta.EngrosserSignatureDate = self.date('engrosser_signature_date')
