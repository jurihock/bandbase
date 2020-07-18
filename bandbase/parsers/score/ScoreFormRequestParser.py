from parsers.common import *
from utils.models import *

class ScoreFormRequestParser(RequestParser):

    def parse(self, score):
        
        score.Name            = self.str('name')
        score.Opus            = self.str('opus')
        score.Piece           = self.str('piece')
        score.CompositionYear = self.int('composition_year')
        score.PublisherID     = self.int('publisher')
        score.Copyright       = self.str('copyright')

        score.StockLetter      = self.str('stock_letter')
        score.StockNumber      = self.int('stock_number')
        score.StockCounter     = self.int('stock_counter')
        score.InStockSinceDate = self.date('in_stock_since_date')
    
        score.EditionID = self.int('edition')
        score.Genre     = self.str('genre')
        score.Style     = self.str('style')
    
        score.MetronomeText = self.str('metronome_text')
        score.MetronomeMark = self.str('metronome_mark')

        if self.bool('feature_vocals'): score.EnableFeature(1)
        else:                           score.DisableFeature(1)

        score.WikidataItemID = self.str('wikidata_item_id')

        score.GemaWorkNumber = self.str('gema_work_number')
        score.GemaTypeID     = self.int('gema_type')
    
        score.Hyperlinks = self.str('hyperlinks')
    
        score.Comment = self.str('comment')
