from parsers.common import *
from utils.models import *

class GigFormRequestParser(RequestParser):

    def parse(self, gig):

        gig.Name                  = self.str('name')

        gig.BeginDate             = self.date('begin_date')
        gig.EndDate               = self.date('end_date')
    
        gig.BeginTime             = self.time('begin_time')
        gig.EndTime               = self.time('end_time')
    
        gig.HostID                = self.int('host')
        gig.LocationID            = self.int('location')
    
        gig.EventRoom             = self.str('event_room')
        gig.EventNature           = self.str('event_nature')
        gig.AudienceSize          = self.int('audience_size')
    
        gig.EntranceFee           = self.float('entrance_fee')
        gig.EntranceFeeCurrencyID = 978 if gig.EntranceFee else None # EUR
    
        gig.LineupKind            = self.str('lineup_kind')
        gig.MusicianCount         = self.int('musician_count')
    
        gig.GemaTypeID            = self.int('gema_type')

        gig.VisibilityID          = self.int('visibility')
    
        gig.Comment               = self.str('comment')
