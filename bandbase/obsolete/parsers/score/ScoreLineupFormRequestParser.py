from parsers.common import *
from utils.models import *

class ScoreLineupFormRequestParser(RequestParser):

    def parse(self, score):

        if score.Lineup is None:

            score.Lineup = ScoreLineup()
        
        score.Lineup.Summary = self.str('summary')
        score.Lineup.Direction = self.str('direction')
    
        score.Lineup.Flute = self.str('flute')
        score.Lineup.Oboe = self.str('oboe')
        score.Lineup.Clarinet = self.str('clarinet')
        score.Lineup.Saxophone = self.str('saxophone')
        score.Lineup.Trumpet = self.str('trumpet')
        score.Lineup.FlugelHorn = self.str('flugel_horn')
        score.Lineup.FrenchHorn = self.str('french_horn')
        score.Lineup.TenorHorn = self.str('tenor_horn')
        score.Lineup.BaritoneHorn = self.str('baritone_horn')
        score.Lineup.Trombone = self.str('trombone')
        score.Lineup.Bass = self.str('bass')
        score.Lineup.Percussion = self.str('percussion')
        score.Lineup.Keyboard = self.str('keyboard')
        score.Lineup.Guitar = self.str('guitar')
        score.Lineup.Strings = self.str('strings')
        score.Lineup.Misc = self.str('misc')
    
        # Finally delete empty lineups
        if score.Lineup.IsEmpty:
    
            # Discard lineup if it isn't in the db
            if score.Lineup.ScoreID is None:

                score.Lineup = None; return
    
            self.db.delete(score.Lineup)
