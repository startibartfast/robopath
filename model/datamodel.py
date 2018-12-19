'''
Created on Nov 1, 2018

@author: carlo
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Integer, String, Column, DateTime, ForeignKey #, Numeric, SmallInteger

from sqlalchemy import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

Base = declarative_base()

_CONNECTION_STRING = "mysql+pymysql://{0}:{1}@localhost/robopath"

class DatabaseManager():
    def __init__(self):
        self.engine = create_engine(_CONNECTION_STRING.format("root", "admin"))
        # create a configured "Session" class
        s = sessionmaker(bind=self.engine, autoflush=False)
        self.session = s()
        
    def createStructure(self):
        Base.metadata.create_all(self.engine)

    def dropStructure(self):
        Base.metadata.drop_all(self.engine)

class Robot(Base):
    __tablename__ = 'robot'
    id = Column(Integer(), primary_key=True)
    name = Column('name', String(255), nullable=False)
    robot_type = Column('robot_type', String(255), nullable=False)
    passing_points = relationship("PassingPoint", backref='robot', cascade='all,delete-orphan')
    obstacles = relationship("Obstacle", backref='robot', cascade='all,delete-orphan')
    arm_length = Column(Integer, nullable=False)
    unreachable_zone_radius = Column(Integer, nullable=False)
    action_angle = Column(Integer, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    UniqueConstraint('name', 'robot_type', name='robot_ux1')
    
    def __repr__(self):
        return "<Robot(name='%s', type=%s)>" % (self.name, self.robot_type)        

#
# Coordinates x,y,z are related to the graphical library's coordinate systems while x1,y1,z1 are related to robot's system     
class PassingPoint(Base):
    __tablename__ = 'passing_point'
    id = Column(Integer(), primary_key=True)
    robot_id = Column(Integer(), ForeignKey('robot.id'))
    name = Column(String(20), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)
    x1 = Column(Integer, nullable=False)
    y1 = Column(Integer, nullable=False)
    point_id = Column(Integer, nullable=False)
    UniqueConstraint('robot_id', 'name', name='point_ux1')
    
    def __repr__(self):
        return "<PassingPoint(name='%s', x=%d, y=%d)>" % (self.name, self.x, self.y)        

class Obstacle(Base):
    __tablename__ = 'obstacle'
    id = Column(Integer(), primary_key=True)
    robot_id = Column(Integer(), ForeignKey('robot.id'))
    name = Column(String(20), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    x1 = Column(Integer, nullable=False)
    y1 = Column(Integer, nullable=False)
    width1 = Column(Integer, nullable=False)
    height1 = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)
    obstacle_id = Column(Integer, nullable=False)
    UniqueConstraint('robot_id', 'name', name='obstacle_ux1')
    
    def __repr__(self):
        return "<Obstacle(name='%s', x=%d, y=%d)>" % (self.name, self.x, self.y)        

# class Customer(Base):
#     __tablename__ = 'customers'
#     id = Column(Integer(), primary_key=True)
#     first_name = Column(String(100), nullable=False)
#     last_name = Column(String(100), nullable=False)
#     username = Column(String(50), nullable=False)
#     email = Column(String(200), nullable=False)
#     address = Column(String(200), nullable=False)
#     town = Column(String(200), nullable=False)
#     created_on = Column(DateTime(), default=datetime.now)
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#     orders = relationship("Order", backref='customer')
#     def __repr__(self):
#         return "<Customer(id='%d', name='%s %s')>" % (self.id, self.first_name, self.last_name)        
# 
# class Item(Base):
#     __tablename__ = 'items'
#     id = Column(Integer(), primary_key=True)
#     name = Column(String(200), nullable=False)
#     cost_price =  Column(Numeric(10, 2), nullable=False)
#     selling_price = Column(Numeric(10, 2),  nullable=False)
#     quantity =  Column(Integer, nullable=False)
#     orders = relationship("OrderLine", backref='item')
#     def __repr__(self):
#         return "<Item(id='%d', name='%s')>" % (self.id, self.name)        
#     
# class Order(Base):
#     __tablename__ = 'orders'
#     id = Column(Integer(), primary_key=True)
#     customer_id = Column(Integer(), ForeignKey('customers.id'))
#     date_placed = Column(DateTime(), default=datetime.now)
#     order_lines = relationship("OrderLine", backref='order')
#     def __repr__(self):
#         return "<Order(id='%d', customer='%s %s', items='%s')>" % (self.id, self.customer.first_name, self.customer.last_name, self.order_lines)        
# 
# class OrderLine(Base):
#     __tablename__ = 'order_lines'
#     id =  Column(Integer(), primary_key=True)
#     order_id = Column(Integer(), ForeignKey('orders.id'))
#     item_id = Column(Integer(), ForeignKey('items.id'))
#     quantity = Column(SmallInteger())
# #    item = relationship("Item")
#     def __repr__(self):
#         return "<Order Line(id='%d', item='%s')>" % (self.id, self.item.name)        

    