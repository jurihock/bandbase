from parsers.common import *
from utils.models import *

class ScoreFolderItemFormRequestParser(RequestParser):

    def __init__(self, folder, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.folder = folder

    def parse(self):

        item = ScoreFolderItem()

        prefix = 'score_folder_{0}_'.format(int(self.folder))

        item.ScoreOrder = self.str(prefix + 'order')
        item.ScoreID    = self.int(prefix + 'score')

        self.folder.Items.append(item)

        return item
