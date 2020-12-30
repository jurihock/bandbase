from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import String, Integer, Float, Boolean, Date, Time, DateTime
from sqlalchemy.orm import relationship as Relationship

from sqlalchemy.ext.declarative import declared_attr as sql_declared_attr
from sqlalchemy.ext.declarative import declarative_base as sql_declarative_base

from sqlalchemy.ext.hybrid import hybrid_property as sql_hybrid_property
from sqlalchemy.ext.hybrid import hybrid_method as sql_hybrid_method

import utils.sql as sql

import inspect

# Table class factory

class ClassFactory(object):

    def __init__(self, root=lambda: TableBase):

        root = root() if inspect.isfunction(root) else root

        self.classes =\
        {
            subclass.__name__: subclass
            for subclass in root.__subclasses__()
        }

    def create(self, name):

        return self.classes[name]()

# Table base classes

class AbstractTable(object):

    __abstract__ = True

    InsertedDateTime = Column(DateTime, nullable=False, server_default=sql.NOW())
    UpdatedDateTime  = Column(DateTime, nullable=False, server_default=sql.NOW(), onupdate=sql.NOW())

    @sql_declared_attr
    def __tablename__(cls):

        # class name in plural
        return cls.__name__ + 's'

class PrimaryTable(AbstractTable):

    ID      = Column(Integer, primary_key=True)
    Comment = Column(String(1023))

    def __int__(self): return self.ID

    @sql_hybrid_property
    def IsPersistent(self): return self.ID < 1000

    @sql_hybrid_property
    def IsRelated(self): return False

class SecondaryTable(AbstractTable):

    ID   = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)

    def __int__(self): return self.ID
    def __str__(self): return self.Name

class StaticSecondaryTable(AbstractTable):

    ID   = Column(Integer, primary_key=True, autoincrement=False)
    Name = Column(String(255), nullable=False)

    def __int__(self): return self.ID
    def __str__(self): return self.Name

class AssociationTable(AbstractTable):

    pass

TableBase = sql_declarative_base(cls=AbstractTable)

# Secondary tables

class ContactCategory(TableBase, SecondaryTable):           __tablename__ = 'ContactCategories'
class Currency(TableBase, StaticSecondaryTable):            __tablename__ = 'Currencies'
class MusicalInstrument(TableBase, StaticSecondaryTable):   pass
class GigGemaType(TableBase, StaticSecondaryTable):         pass
class ScorePersonRole(TableBase, StaticSecondaryTable):     pass
class ScoreEdition(TableBase, StaticSecondaryTable):        pass
class ScoreFeatureType(TableBase, StaticSecondaryTable):    pass
class ScoreGemaType(TableBase, StaticSecondaryTable):       pass
class GigVisibility(TableBase, StaticSecondaryTable):       __tablename__ = 'GigVisibilities'
class GigPersonAttendance(TableBase, StaticSecondaryTable): __tablename__ = 'GigPersonAttendance'

# Association tables

class ScorePerson(TableBase, AssociationTable):

    __table_args__   = \
    (
        UniqueConstraint('ScoreID', 'PersonID', 'PersonRoleID',
                         name='UniqueScorePerson'),
    )

    ScoreID       = Column(Integer, ForeignKey('Scores.ID'), primary_key=True)

    PersonID      = Column(Integer, ForeignKey('Contacts.ID'), primary_key=True)
    Person        = Relationship(lambda: Contact, foreign_keys=PersonID)

    PersonRoleID  = Column(Integer, ForeignKey('ScorePersonRoles.ID'), primary_key=True)
    PersonRole    = Relationship(lambda: ScorePersonRole, foreign_keys=PersonRoleID)

    @sql_hybrid_property
    def IsComposer(self): return self.PersonRoleID == 1

    @sql_hybrid_property
    def IsArranger(self): return self.PersonRoleID == 2

    @sql_hybrid_property
    def IsPoet(self):     return self.PersonRoleID == 3

class ScoreFeature(TableBase, AssociationTable):

    __table_args__   = \
    (
        UniqueConstraint('ScoreID', 'ScoreFeatureTypeID',
                         name='UniqueScoreFeature'),
    )

    ScoreID            = Column(Integer, ForeignKey('Scores.ID'), primary_key=True)

    ScoreFeatureTypeID = Column(Integer, ForeignKey('ScoreFeatureTypes.ID'), primary_key=True)
    ScoreFeatureType   = Relationship(lambda: ScoreFeatureType, foreign_keys=ScoreFeatureTypeID)

class ScoreLineup(TableBase, AssociationTable):

    ScoreID       = Column(Integer, ForeignKey('Scores.ID'), primary_key=True)

    Summary       = Column(String(100))
    Direction     = Column(String(100))

    Flute         = Column(String(100))
    Oboe          = Column(String(100))
    Clarinet      = Column(String(100))
    Saxophone     = Column(String(100))
    Trumpet       = Column(String(100))
    FlugelHorn    = Column(String(100))
    FrenchHorn    = Column(String(100))
    TenorHorn     = Column(String(100))
    BaritoneHorn  = Column(String(100))
    Trombone      = Column(String(100))
    Bass          = Column(String(100))
    Percussion    = Column(String(100))
    Keyboard      = Column(String(100))
    Guitar        = Column(String(100))
    Strings       = Column(String(100))
    Misc          = Column(String(100))

    @sql_hybrid_property
    def IsEmpty(self):

        common_fields = [ 'ScoreID', 'InsertedDateTime', 'UpdatedDateTime' ]

        fields = [ field for field in self.__dict__.keys()
                   if not field.startswith('_')
                   and not field in common_fields ]

        for field in fields:

            value = getattr(self, field)

            if value is not None and value.strip():

                return False

        return True

class GigScore(TableBase, AssociationTable):

    __table_args__   = \
    (
        UniqueConstraint('GigID', 'ScoreOrder',
                         name='UniqueGigScore'),
    )

    GigID         = Column(Integer, ForeignKey('Gigs.ID'), primary_key=True)

    ScoreOrder    = Column(Integer, primary_key=True, autoincrement=False)

    ScoreID       = Column(Integer, ForeignKey('Scores.ID'), nullable=False)
    Score         = Relationship(lambda: Score, foreign_keys=ScoreID)

class GigSetlistMeta(TableBase, AssociationTable):

    __tablename__ = 'GigSetlistMeta'

    GigID          = Column(Integer, ForeignKey('Gigs.ID'), primary_key=True)

    BandName       = Column(String(255), nullable=False)

    BandLeaderID   = Column(Integer, ForeignKey('Contacts.ID'), nullable=False)
    BandLeader     = Relationship(lambda: Contact, foreign_keys=BandLeaderID)

    GemaMembershipNumber = Column(String(50))
    GemaCustomerNumber   = Column(String(50))

    EngrosserSignaturePlace = Column(String(50))
    EngrosserSignatureDate  = Column(Date)

    def __init__(self, *args, **kwargs):

        self.BandName = 'Big Band „Brandheiß“ Pforzheim'
        self.BandLeaderID = 1962

        super(GigSetlistMeta, self).__init__(*args, **kwargs)

class GigPerson(TableBase, AssociationTable):

    __table_args__   = \
    (
        UniqueConstraint('GigID', 'PersonID',
                         name='UniqueGigPerson'),
    )

    GigID        = Column(Integer, ForeignKey('Gigs.ID'), primary_key=True)

    PersonID     = Column(Integer, ForeignKey('Contacts.ID'), primary_key=True)
    Person       = Relationship(lambda: Contact, foreign_keys=PersonID)

    InstrumentID = Column(Integer, ForeignKey('MusicalInstruments.ID'), nullable=False)
    Instrument   = Relationship(lambda: MusicalInstrument, foreign_keys=InstrumentID)

    AttendanceID = Column(Integer, ForeignKey('GigPersonAttendance.ID'), nullable=False)
    Attendance   = Relationship(lambda: GigPersonAttendance, foreign_keys=AttendanceID)

    Comment      = Column(String(255))

class ScoreFolderItem(TableBase, AssociationTable):

    __table_args__   = \
    (
        UniqueConstraint('ScoreFolderID', 'ScoreOrder',
                         name='UniqueScoreFolderItem'),
    )

    ScoreFolderID = Column(Integer, ForeignKey('ScoreFolders.ID'), primary_key=True)

    ScoreOrder    = Column(String(5), primary_key=True)

    ScoreID       = Column(Integer, ForeignKey('Scores.ID'), nullable=False)
    Score         = Relationship(lambda: Score, foreign_keys=ScoreID)

# Primary tables

class Contact(TableBase, PrimaryTable):

    FirstName     = Column(String(255))
    LastName      = Column(String(255), nullable=False)
    FullLastName  = Column(String(255))
    BirthDate     = Column(Date)

    CategoryID    = Column(Integer, ForeignKey(ContactCategory.ID), nullable=False)
    Category      = Relationship(ContactCategory, foreign_keys=CategoryID)

    Street        = Column(String(50))
    HouseNumber   = Column(String(5))
    PostalCode    = Column(String(10))
    City          = Column(String(50))
    Country       = Column(String(50))

    LandlinePhone = Column(String(50))
    MobilePhone   = Column(String(50))
    Fax           = Column(String(50))
    EMail         = Column(String(50))
    WWW           = Column(String(50))

    Latitude      = Column(Float)
    Longitude     = Column(Float)

    def __str__(self):

        return self.Name

    @sql_hybrid_property
    def Name(self):

        foo = [ self.FirstName, self.FullLastName or self.LastName ]

        result = ' '.join(bar for bar in foo if bar)

        return result

    @Name.expression
    def Name(self):

        return sql.CONCAT(Contact.FirstName, ' ',
                          Contact.LastName, ' ',
                          Contact.FullLastName)

    @sql_hybrid_property
    def Address(self):

        foo = \
        [
            '{0} {1}'.format(self.Street, self.HouseNumber or '').strip()
                if self.Street else None,
            '{0} {1}'.format(self.PostalCode or '', self.City).strip()
                if self.City else None,
        ]

        result = ', '.join(bar for bar in foo if bar).strip()

        return result or None

    @sql_hybrid_property
    def IsScorePublisher(self):

        return self.CategoryID == 1 # Verlag

    @sql_hybrid_property
    def IsScorePerson(self):

        return self.CategoryID == 11 # Komponist, Bearbeiter oder Dichter

    @sql_hybrid_property
    def IsGigPerson(self):

        return sql.OR(self.CategoryID == 12, # Bandmusiker
                      self.CategoryID == 13, # Ehemalige Bandmusiker
                      self.CategoryID == 14) # Gastmusiker

    @sql_hybrid_property
    def IsBandMusician(self):

        return self.CategoryID == 12 # Bandmusiker

class Score(TableBase, PrimaryTable):

    # FIXME: Temporary disable the unique stock ID constraint
    # __table_args__   = \
    # (
    #     UniqueConstraint('StockLetter', 'StockNumber', 'StockCounter',
    #                      name='StockID'),
    # )

    Name             = Column(String(255), nullable=False)
    Opus             = Column(String(255))
    Piece            = Column(String(255))
    CompositionYear  = Column(Integer)
    Copyright        = Column(String(255))

    PublisherID      = Column(Integer, ForeignKey(Contact.ID))
    Publisher        = Relationship(Contact, foreign_keys=PublisherID)

    EditionID        = Column(Integer, ForeignKey(ScoreEdition.ID), nullable=False)
    Edition          = Relationship(ScoreEdition, foreign_keys=EditionID)

    Genre            = Column(String(50))
    Style            = Column(String(50))
    MetronomeText    = Column(String(50))
    MetronomeMark    = Column(String(50))

    WikidataItemID   = Column(String(50))

    GemaWorkNumber   = Column(String(50))
    GemaTypeID       = Column(Integer, ForeignKey(ScoreGemaType.ID))
    GemaType         = Relationship(ScoreGemaType, foreign_keys=GemaTypeID)

    Persons          = Relationship(ScorePerson,  cascade='save-update, merge, delete, delete-orphan')
    Features         = Relationship(ScoreFeature, cascade='save-update, merge, delete, delete-orphan')
    Lineup           = Relationship(ScoreLineup,  cascade='save-update, merge, delete, delete-orphan', uselist=False)

    # FIXME: Temporary allow the stock number be nullable
    StockLetter      = Column(String(10))
    StockNumber      = Column(Integer, nullable=True)
    StockCounter     = Column(Integer)
    InStockSinceDate = Column(Date)

    Hyperlinks       = Column(String(3071))

    def __str__(self):

        return self.NameOpusPieceStockID

    @sql_hybrid_property
    def NameOpusPiece(self):

        foo = [ self.Opus, self.Piece ]

        baz = ', '.join(bar for bar in foo if bar is not None)

        result = '%s (%s)' % (self.Name, baz) \
            if baz else self.Name

        return result

    @sql_hybrid_property
    def NameOpusPieceStockID(self):

        result = '%s #%s' % (self.NameOpusPiece, self.StockID or 'n.a.')

        return result

    @sql_hybrid_property
    def StockNumberCounter(self):

        result = ','.join(str(x) for x in [ self.StockNumber or ('?' if self.StockCounter else '' ), self.StockCounter ] if x)

        return result or 'n.a.'

    @sql_hybrid_property
    def StockID(self):

        result = ','.join(str(x) for x in [ self.StockLetter, self.StockNumberCounter ] if x)

        return result

    @sql_hybrid_property
    def GSM(self):

        result = ', '.join(x for x in [ self.Genre, self.Style, self.MetronomeText ] if x)

        return result

    @GSM.expression
    def GSM(self):

        return sql.CONCAT(Score.Genre, ' ', Score.Style, ' ', Score.MetronomeText)

    @sql_hybrid_method
    def HasFeature(self, id):

        ids = [feature.ScoreFeatureTypeID for feature in self.Features]

        return id in ids

    @sql_hybrid_method
    def EnableFeature(self, id):

        ids = [feature.ScoreFeatureTypeID for feature in self.Features]

        if id in ids:
            return

        feature = ScoreFeature(ScoreID=self.ID, ScoreFeatureTypeID=id)

        return self.Features.append(feature)

    @sql_hybrid_method
    def DisableFeature(self, id):

        features = [feature for feature in self.Features if feature.ScoreFeatureTypeID == id]

        for feature in features:
            self.Features.remove(feature)

    @sql_hybrid_method
    def GetComposer(self, index):

        if self.Persons is None:
            return None

        composers = [ person.Person \
                      for person in self.Persons \
                      if person.IsComposer ]

        if len(composers) <= index:
            return None

        return composers[index]

    @sql_hybrid_method
    def GetArranger(self, index):

        if self.Persons is None:
            return None

        arrangers = [ person.Person \
                      for person in self.Persons \
                      if person.IsArranger ]

        if len(arrangers) <= index:
            return None

        return arrangers[index]

    @sql_hybrid_method
    def GetPoet(self, index):

        if self.Persons is None:
            return None

        poets = [ person.Person \
                  for person in self.Persons \
                  if person.IsPoet ]

        if len(poets) <= index:
            return None

        return poets[index]

class Gig(TableBase, PrimaryTable):

    Name          = Column(String(255), nullable=False)

    BeginDate     = Column(Date, nullable=False)
    EndDate       = Column(Date, nullable=False)

    BeginTime     = Column(Time, nullable=False)
    EndTime       = Column(Time, nullable=False)

    HostID        = Column(Integer, ForeignKey(Contact.ID))
    Host          = Relationship(Contact, foreign_keys=HostID)

    LocationID    = Column(Integer, ForeignKey(Contact.ID), nullable=False)
    Location      = Relationship(Contact, foreign_keys=LocationID)

    EventRoom     = Column(String(50))
    EventNature   = Column(String(50))
    AudienceSize  = Column(Integer)

    EntranceFee           = Column(Float)
    EntranceFeeCurrencyID = Column(Integer, ForeignKey(Currency.ID))

    LineupKind    = Column(String(50))
    MusicianCount = Column(Integer)

    GemaTypeID    = Column(Integer, ForeignKey(GigGemaType.ID))
    GemaType      = Relationship(GigGemaType, foreign_keys=GemaTypeID)

    VisibilityID  = Column(Integer, ForeignKey(GigVisibility.ID), nullable=False, server_default='0')
    Visibility    = Relationship(GigVisibility, foreign_keys=VisibilityID)

    Scores        = Relationship(GigScore, cascade='save-update, merge, delete, delete-orphan')
    Persons       = Relationship(GigPerson, cascade='save-update, merge, delete, delete-orphan')

    SetlistMeta   = Relationship(GigSetlistMeta, cascade='save-update, merge, delete, delete-orphan', uselist=False)

    def __init__(self, *args, **kwargs):

        self.LineupKind = 'Big Band'
        self.VisibilityID = 0

        super(Gig, self).__init__(*args, **kwargs)

    def __str__(self):

        return self.Name

    def build(self, db):

        if self.SetlistMeta is None:

            self.SetlistMeta = GigSetlistMeta()

            self.SetlistMeta.BandLeader = db.query(Contact) \
                .get(self.SetlistMeta.BandLeaderID)

            self.Visibility = db.query(GigVisibility) \
                .get(self.VisibilityID)

    @sql_hybrid_property
    def DateTuple(self):

        return (self.BeginDate, self.EndDate)

    @sql_hybrid_property
    def TimeTuple(self):

        return (self.BeginTime, self.EndTime)

    @sql_hybrid_property
    def IsPublished(self):

        return self.VisibilityID > 0

    @sql_hybrid_property
    def IsPrivate(self):

        return self.VisibilityID == 1

    @sql_hybrid_property
    def IsPublic(self):

        return self.VisibilityID >= 2

    @sql_hybrid_property
    def IsFeatured(self):

        return self.VisibilityID == 3

    @sql_hybrid_method
    def GetScore(self, index):

        if self.Scores is None:
            return None

        for score in self.Scores:

            if score.ScoreOrder == index:
                return score.Score

        return None

    @sql_hybrid_method
    def GetPerson(self, index):

        if self.Persons is None:
            return None

        if len(self.Persons) <= index:
            return None

        persons = sorted(self.Persons, key=lambda person: [person.Instrument.Name, person.Person.LastName])

        return persons[index]

class ScoreFolder(TableBase, PrimaryTable):

    Name  = Column(String(255), nullable=False)
    Order = Column(Integer, nullable=False)

    Items = Relationship(ScoreFolderItem, cascade='save-update, merge, delete, delete-orphan')

    def __str__(self):

        return self.Name
