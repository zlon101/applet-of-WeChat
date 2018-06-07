# coding=utf-8

from crp.models import Messages, User
from sqlalchemy import desc
from crp.exception import NotExistMessageidException
import datetime
import math

# 添加一条邀请，邀请中需要包含图像相关信息
def add_message(app, imgtitle, imgurl, nick, senderId, authorId, content):
    dbsession = app.sessionMaker()
    oneMessage = Messages(imgurl=imgurl, imgtitle=imgtitle, senderNick=nick, senderId=senderId, authorId=authorId, content=content, datetime=datetime.datetime.today())
    try:
        dbsession.add(oneMessage)        # 邀请入库
    finally:
        dbsession.commit()

# 查询邀请页
def query_messages_page(app, authorId, perpage, page):
    dbsession = app.sessionMaker()
    try:
        allItems = dbsession.query(Messages).filter_by(authorId=authorId).order_by(desc(Messages.unread)).order_by(desc(Messages.datetime)).all()
    finally:
        dbsession.commit()

    # 提取出该页数据
    totalpage = math.ceil(len(allItems)/perpage)
    startIdx = perpage*(page-1)
    endIdx = startIdx+perpage if startIdx+perpage<=len(allItems) else len(allItems)
    items = allItems[startIdx:endIdx]

    # 转化成字典形式
    itemList = []
    for item in items:
        dicitem = {
            "messageId":item.id,
            "unread": item.unread,
            "sender":item.senderNick,
            "img":item.imgurl,
            "imgtitle":item.imgtitle,
            "content":item.content,
            "datetime":str(item.datetime)
        }
        itemList.append(dicitem)
    return totalpage, itemList

def message_unread_number(app, wxid):
    dbsession = app.sessionMaker()
    try:
        count = dbsession.query(Messages).filter_by(authorId=wxid).filter_by(unread=1).count()
    finally:
        dbsession.commit()
    return count

def message_have_read(app, wxid, messageId):
    dbsession = app.sessionMaker()
    try:
        messageItem = dbsession.query(Messages).filter_by(id=messageId).first()
        if not messageItem:
            raise NotExistMessageidException(messageId)
        messageItem.unread=0
    finally:
        dbsession.commit()

def messages_all_read(app, wxid):
    dbsession = app.sessionMaker()
    try:
        messageList = dbsession.query(Messages).filter_by(authorId=wxid).filter_by(unread=1).all()
        for item in messageList:
            item.unread = 0
    finally:
        dbsession.commit()
        
