from sqlalchemy import Column, String, create_engine, Date, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class User(Base):
    # 表名
    __tablename__='users'
    __table_args__ = {"mysql_charset" : "utf8"}

    # 字段
    id = Column(Integer, primary_key=True)
    wxid = Column(String(32), unique=True, index=True)
    unreadNum = Column(Integer, default=0)
    datetime = Column(DateTime)


class ImgHistory(Base):
    # 表名
    __tablename__='img_history'
    __table_args__ = {"mysql_charset" : "utf8"}

    # 字段
    id = Column(Integer, primary_key=True)                  # 自增主键
    imgid = Column(String(64), unique=True, index=True)     # 图像ID, 隐藏在图像中的数据
    wxid = Column(String(32), index=True)                   # 微信ID
    path = Column(String(128))                              # 图像相对于工作目录的路径
    title = Column(String(64))                              # 图像名称
    content = Column(String(300))                           # 图像内容, 用于信息隐藏
    finish = Column(Integer, default=0)                     # 是否完成的标记, 0-未完成, 1-完成, 2-处理错误
    datetime  = Column(DateTime)                            # 创建日期

class Invites(Base):
    __tablename__='invites'     # 表名
    __table_args__ = {"mysql_charset" : "utf8"}

    # 字段
    id = Column(Integer, primary_key=True)                  # 自增主键
    unread = Column(Integer, default=0)                     # 是否未读(0:已读，1:未读)
    imgurl = Column(String(128))                            # 图片url
    imgtitle = Column(String(64))                           # 图片名称
    inviterNick = Column(String(128))                       # 用户昵称
    inviterId = Column(String(32))
    authorId = Column(String(32))
    content = Column(String(300))
    datetime = Column(DateTime)                             # 邀请时间
