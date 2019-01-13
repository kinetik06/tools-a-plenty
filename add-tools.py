# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Tool, Base, Brand, User

engine = create_engine('sqlite:///toolcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

brand1 = Brand(name='Craftman', description="Craftman, an authentic American icon. For nearly a century, we've been the brand mechanics trust.")

tool1 = Tool(name='25 Piece Screwdriver Set', description="""Includes 17 drivers: (4) 1-1/2-in (3/32-in, 1/4-in, PH#0, PH#2), (2) 2-1/2-in (1/8-in, PH#0), (4) 3-in (PH#1, T10, T15, T20), (5) 4-in (3/16-in, 1/4-in, PH#2, T25, SQ#2), (2) 6-in (1/4-in and PH#2), 4 pc hook and pick set, 3-offsets screwdriver, keychain""",
             price='29.98', type='Hand Tools', brand=brand1)
tool2 = Tool(name='81 pc. Gunmetal Tool Set', description="""The New CRAFTSMAN Gunmetal Chrome 81-Piece mechanics tool set is made for the auto-enthusiast, semi-pro, or do-it-yourselfer. This set comes with the new industry-leading, CRAFTSMAN 120-tooth ratchet that provides maximum accessibility in tight spots. With its slim head and 3-degree arc swing, you can get into narrow spaces with ease and quickly tighten or loosen a fastener.""",
             price='119.00', type='Hand Tools', brand=brand1)
tool3 = Tool(name='V20 20-volt Max 1/2-in Drive Cordless Impact Wrench', description="""The CRAFTSMAN V20 20V MAX 1/2-in impact wrench has a MAX torque rating of 350 ft-lbs for speed and ease of removing large fasteners. The hog ring anvil makes changes quick and easy.""",
             price='149.00', type='Power Tools', brand=brand1)
tool4 = Tool(name='V20* CORDLESS BRUSHLESS DRILL/DRIVER KIT', description="""The CRAFTSMAN V20 20V MAX* Brushless Drill/Driver has a 1/2-in. chuck to fit a variety of drill bits for different applications. The 400 UWO provides the power needed to complete your heavy duty tasks. The metal ratcheting chuck provides secure bit retention and durability.""",
             price='159.00', type='Power Tools', brand=brand1)
tool5 = Tool(name='Mini Diagonal Pliers - 4.5"', description="""Multi-Zone Bi-Material Grips for Comfort and Control""",
             price='5.98', type='Hand Tools', brand=brand1)
tool6 = Tool(name='20 oz. Smooth Face Steel Rip Claw Hammer', description="""Vibration reduction ergonomic grip for end user comfort and added performance""",
             price='19.98', type='Hand Tools', brand=brand1)
tool7 = Tool(name='165-Piece Standard (SAE) and Metric Polished Chrome Mechanic\'s Tool Set', description="""A combination of ratchets, wrenches, sockets, and accessories make the CRAFTSMAN 165-piece mechanics tool set the perfect collection for the professional, semi-pro, or serious do-it-yourselfer.""",
             price='99.00', type='Hand Tools', brand=brand1)
tool8 = Tool(name='Nail Punch Set', description="""The CRAFTSMAN 3 pc nail set has a comfortable bi-material grip with a color coded handle to make it easier to identify the size of each tip without removing it from your tool belt.""",
             price='8.98', type='Hand Tools', brand=brand1)
session.add_all([brand1, tool1, tool2, tool3, tool4, tool5, tool6, tool7, tool8])
session.commit()

# deleted = session.query(Brand).first()
# session.delete(deleted)
# session.commit()
