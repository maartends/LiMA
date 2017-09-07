from __future__ import absolute_import
from datetime import datetime
from sqlalchemy import (
    #~ Column,
    Integer,
    Text,
    String,
    Unicode,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    Boolean,
    Table,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )
# RootFactory security
from lima.models.security import *

from formalchemy import Column, Field
from formalchemy.fields import SelectFieldRenderer, TextAreaFieldRenderer
#~ import fa.jquery as jq

from zope.sqlalchemy import ZopeTransactionExtension
from configobj import ConfigObj

config = ConfigObj('lima/settings.conf')
senders = list()
for item in config['ezine:types'].iteritems():
    senders.append(', '.join((item[1]['sender_name'], item[1]['sender_email'])))
continents = config['ezine:geo']['continents']['name']
countries = config['ezine:geo']['countries']['name']
ezine_types = config['ezine:types']
acctypes = config['ezine:acctypes']['name']
boardbasis = config['ezine:boardbasis']['name']

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Association tables
assoc_table_reltags_auctions = Table('assoc_reltags_auctions', Base.metadata,
    Column('reltag_cid', Integer, ForeignKey('reltags.cid')),
    Column('auction_cid', Integer, ForeignKey('auctions.cid'))
)


# Ezine superclass
class Ezine(Base):
    __label__       = 'Ezine'       # label used in UI
    __plural__      = 'Ezines'      # plural used in UI
    __tablename__   = 'ezines'
    cid             = Column(Integer,       primary_key=True)
    type            = Column(String(50),    unique=False,   nullable=False)
    name            = Column(String,        unique=True,    nullable=False)
    subject         = Column(String(80),    unique=False,   nullable=False)
    send_date       = Column(Date,          unique=False,   nullable=False)
    ezine_items     = relationship("EzineItem",
                                   backref="ezine",
                                   order_by="asc(EzineItem.item_pos)",
                                   cascade='all, delete-orphan')
    __mapper_args__ = {'polymorphic_on': type}

    # Attributes that do not map to columns used for passing around html and
    # txt strings easily, along with the general ezine-data
    html            = None
    html_pre        = None
    txt             = None

    def __unicode__(self):
        return self.name
    """
    def __init__(self, type='', name='', subject='', send_date=None):
        self.type       = type
        self.name       = name
        self.subject    = subject
        self.send_date  = send_date or datetime.now()
    """
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'cid'  : self.cid,
            'type': self.type,
            'name': self.name,
            'subject': self.subject,
            'send_date': self.send_date.strftime("%Y%m%dT%H%M%S"),
            }
    # TODO: implement methods:
    #~ def rendered_html(premailed=False):
        #~ """Returns rendered html for this ezine as unicode string."""
        #~ t = templateFilters()
        #~ renderer = 'lima:' + '/'.join(('templates', 'ezines',
                                       #~ 'biedmee', 'ezine.html.pt'))
        # TODO: Problem: do we need a request object to render the template
        #~ try:
            #~ html = render(renderer, {'Ezine': ezine, 'mailer': 'mailjet',
                                     #~ 'templateFilters': t, 'debug': False,},
                                #~ request=self.request)
    # def rendered_txt():


# Ezine type = biedmee
class BiedmeeEzine(Ezine):
    __label__       = 'Biedmee Ezine'       # label used in UI
    __plural__      = 'Biedmee Ezines'      # plural used in UI
    __tablename__   = 'biedmee_ezines'
    __mapper_args__ = {'polymorphic_identity': 'biedmee'}

    cid = Column(Integer, ForeignKey('ezines.cid'), primary_key=True,)


class CatalogEntry(Base):
    __label__       = 'CatalogEntry'    # label used in UI
    __plural__      = 'CatalogEntries'  # plural used in UI
    __tablename__   = 'catalogentries'
    __mapper_args__ = {'polymorphic_identity': 'catalogentry'}
    cid             = Column(Integer, primary_key=True)
    name            = Column(Unicode)
    price           = Column(Integer, label="Aankoopprijs (garante prijs)")
    cat_desc        = Column(Text, label="Description",)
    stock           = Column(Integer, label="Voorraad")

    def __unicode__(self):
        return ' | '.join( (str(self.id), str(self.name)) )
    """
    def __init__(self, name='', price=0, cat_desc='', stock=0):
        self.name       = name
        self.price      = price
        self.cat_desc   = cat_desc
        self.stock      = stock
    """

class Auction(Base):
    __label__       = 'Veiling'     # label used in UI
    __plural__      = 'Veilingen'   # plural used in UI
    __tablename__   = 'auctions'
    __mapper_args__ = {'polymorphic_identity': 'auction'}
    cid             = Column(Integer, primary_key=True)
    catentry_cid    = Column(Integer, ForeignKey('catalogentries.cid'))
    auctiontype_cid = Column(Integer, ForeignKey('auctiontypes.cid'),
                            label='AuctionType (autocomplete: typ de eerste letter)')
    url             = Column(String(2048), label='URL')
    image           = Column(String(2048), label='Foto (absolute url naar de afbeelding)')
    title           = Column(Unicode)
    openprice       = Column(Integer, label="Startbod")
    start_time      = Column(DateTime)
    end_time        = Column(DateTime)
    auct_intro      = Column(Text, label="Veiling intro tekst",)
    auctiontype     = relationship("AuctionType",
                                backref=backref('ezine_auctions',
                                order_by=cid))
    catentry        = relationship("CatalogEntry",
                                   cascade='all, delete-orphan',
                                   backref=backref('auctions', order_by=cid))
    reltags         = relationship("RelTag",
                                secondary=assoc_table_reltags_auctions)

    def __unicode__(self):
        return ' | '.join( (str(self.cid), self.title) )
    """
    def __init__(self, catentry_id=0, auctiontype_id=0, title='', openprice=0,
                 start_time=None, end_time=None, auct_intro=''):
        self.catentry_cid    = catentry_id
        self.auctiontype_cid = auctiontype_id
        self.title          = title
        self.openprice      = openprice
        self.start_time     = start_time or datetime.now()
        self.end_time       = end_time or datetime.now()
        self.auct_intro     = auct_intro
    """

# EzineItems: ezine to auctions association class/table
class EzineItem(Base):
    """ EzineItem superclass """
    __label__       = 'Ezine Item'      # label used in UI
    __plural__      = 'Ezine Items'     # plural used in UI
    __tablename__   = 'ezine_items'
    __table_args__  = (UniqueConstraint('ezine_cid', 'item_pos',
                            name='_ezine_items_positions_sequence'),)
    auct_cid        = Column(Integer, ForeignKey('auctions.cid'),
                                      primary_key=True)
    ezine_cid       = Column(Integer, ForeignKey('ezines.cid'),
                                      primary_key=True)
    item_pos        = Column(Integer)
    image           = Column(String(2048), label='Foto (absolute url naar de afbeelding)')
    title           = Column(Unicode)
    openprice       = Column(Integer, label="Startbod")
    text            = Column(Text, label="Text (HTML, let: url's in deze text worden"
                                   " NIET automatisch voorzien van UTM-codes)")
    auction         = relationship("Auction",
                                backref=backref('ezine_items'))

    def __unicode__(self):
        return ' | '.join( (str(self.auct_cid), self.title) )
    """
    def __init__(self, auct_id=0, ezine_id=0, item_pos=0, image='', title='',
                 openprice=0, text=''):
        self.auct_cid   = auct_id
        self.ezine_cid  = ezine_id
        self.item_pos   = item_pos
        self.image      = image
        self.title      = title
        self.openprice  = openprice
        self.text       = text
    """

""" Commented out: should be linked to CatalogEntry
class Relatie(Base):
    __label__       = 'Relatie'     # label used in UI
    __plural__      = 'Relaties'    # plural used in UI
    __tablename__   = 'customer'

    cid          = Column(Integer, primary_key=True)
    oid         = Column(Integer)
    name        = Column(Unicode, unique=True)
    logo        = Column(Unicode, unique=True)
    url_netloc  = Column(Unicode, unique=True)
    active      = Column(Boolean)

    ezine_items = relationship("EzineItem",
                        backref=backref('customer', order_by=name))

    @property
    def serialize(self):
        # Return object data in easily serializeable format
        return {
           'cid'  : self.cid,
           'oid': self.oid,
           'name': self.name,
           'logo': self.logo,
           'url_netloc': self.url_netloc,

       }
"""

class AuctionType(Base):
    __label__       = 'AuctionType'     # label used in UI
    __plural__      = 'AuctionTypes'    # plural used in UI
    __tablename__   = 'auctiontypes'

    cid             = Column(Integer, primary_key=True)
    name            = Column(Unicode)
    overlay_image   = Column(String(2048))

    def __unicode__(self):
        return self.name

class RelTag(Base):
    __label__       = 'RelTag'     # label used in UI
    __plural__      = 'RelTags'    # plural used in UI
    __tablename__   = 'reltags'

    cid     = Column(Integer, primary_key=True)
    tag     = Column(Unicode, nullable=False)
    desc    = Column(Unicode, label="Description",
                    renderer=TextAreaFieldRenderer)

    def __unicode__(self):
        return self.tag

class ClangMailjetSyncReport(Base):
    __label__       = 'ClangMailjetSyncReport'     # label used in UI
    __plural__      = 'ClangMailjetSyncReports'    # plural used in UI
    __tablename__   = 'clang_mailjet_sync_reports'

    cid             = Column(Integer, primary_key=True)
    start_time      = Column(DateTime)
    end_time        = Column(DateTime)
    filename        = Column(String)
    no_addresses    = Column(Integer)
    status          = Column(Text)

    def __unicode__(self):
        return self.status
