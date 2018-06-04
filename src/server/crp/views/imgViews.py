# coding=utf-8

from crp.untils import sp, urlget, unique_imgid_gen, md5, unescape, request_around, inc_imgnum_gen
from crp.services import imgHistoryServices
from crp.exception import CrpException
from flask import request

# 模仿数据隐藏
def data_hide(inpImgPath, outImgPath, imgnum, isdel=True):
    import shutil
    import os

    shutil.copyfile(inpImgPath, outImgPath)
    if isdel:
        os.remove(inpImgPath)
    return True

# 模仿数据提取
def data_extract(inpImgPath, isdel=True):
    import os
    if isdel:
        os.remove(inpImgPath)
    return 0

def data_extract2(inpImgPath, isdel=True):
    import os
    if isdel:
        os.remove(inpImgPath)
    return 1

def bind_routes(app):
    import time

    # 图像绑定视图函数
    @app.route("/img-bind", methods=["POST"])
    @request_around(app, request, hasSessionId=True)
    def img_bind(sessionId):
        # 处理图像
        imgFile = request.files.get('img', None)                    # 图像文件
        if not imgFile:
            raise CrpException("缺少图像文件")
        imgtitle = unescape(request.form.get("imgtitle", None))     # 图像对外标题
        imgtitle = imgtitle if imgtitle else None
        imgnum = next(inc_imgnum_gen)
        imgid = md5(str(imgnum))
        timeStamp = str(int(time.time()*1000000))                   # 转化为微秒级时间戳, 用作文件命名
        inpImgPath = app.config["TMP_DIR"]+timeStamp+".jpeg"        # 原始图片路径
        outImgPath = app.config["IMG_DIR"]+timeStamp+".jpeg"        # 载迷图像输出路径
        imgFile.save(inpImgPath)                                    # 将图像保存
        # 提取图像id，查看id是否已经存在
        # maybeImgId = dataExtract(inpImgPath, isdel=False)

        # 先插入历史记录
        imgHistoryServices.insert_notfinish_img_history(app, sessionId=sessionId, imgid=imgid, path=outImgPath, imgtitle=imgtitle, imgtype=0)

        # 信息隐藏 生成载密图像
        data_hide(inpImgPath, outImgPath, imgnum)         # 调用C++信息隐藏处理

        # 更新数据库finish字段
        imgHistoryServices.update_finish_img_history(app, imgid=imgid)
        return {}

    # 作者溯源视图函数
    @app.route("/query-author", methods=["POST"])
    @request_around(app, request, hasSessionId=True)
    def query_author(sessionId):
        import time
        imgFile = request.files.get('img', None)                    # 图像文件
        if not imgFile:
            raise CrpException("缺少图像文件")
        timeStamp = str(int(time.time()*1000000))                   # 转化为微秒级时间戳, 用作文件命名
        inpImgPath = app.config["TMP_DIR"]+timeStamp+".jpeg"        # 原始图片路径
        imgFile.save(inpImgPath)                                    # 将图像保存

        # 提取图像id
        imgnum = data_extract(inpImgPath)
        imgid = md5(str(imgnum))

        # 查询库
        exists, imgtitle = imgHistoryServices.query_img_author(app, imgid=imgid)
        if exists : 
            return {"exists":exists, "imgtitle":imgtitle, "imgid":imgid}
        else :
            return {"exists":exists}

    @app.route("/ih", methods=["POST"])
    @request_around(app, request, hasSessionId=True)
    def info_hide(sessionId):
        key = unescape(request.form.get("key", None))
        if not key:
            raise CrpException("密钥不能为空")
        secret = unescape(request.form.get("secret", None))
        if not secret:
            raise CrpException("秘密信息不能为空")
        imgFile = request.files.get('img', None)                    # 图像文件
        if not imgFile:
            raise CrpException("缺少图像文件")
        imgtitle = unescape(request.form.get("imgtitle", None))     # 图像对外标题
        imgtitle = imgtitle if imgtitle else None
        # imgid = next(unique_imgid_gen)                              # 获取该次操作的图像ID
        imgnum = next(inc_imgnum_gen)
        imgid = md5(str(imgnum))
        timeStamp = str(int(time.time()*1000000))                   # 转化为微秒级时间戳, 用作文件命名
        inpImgPath = app.config["TMP_DIR"]+timeStamp+".jpeg"        # 原始图片路径
        outImgPath = app.config["IMG_DIR"]+timeStamp+".jpeg"        # 载迷图像输出路径
        imgFile.save(inpImgPath)                                    # 将图像保存
        # 提取图像id，查看id是否已经存在
        # maybeImgId = dataExtract(inpImgPath, isdel=False)
        
         # 先插入历史记录
        imgHistoryServices.insert_notfinish_img_history(app, sessionId=sessionId, path=outImgPath, imgid=imgid, imgtitle=imgtitle, imgtype=1, secret=secret, key=key)

         # 信息隐藏 生成载密图像
        data_hide(inpImgPath, outImgPath, imgid)         # 调用C++信息隐藏处理

        imgHistoryServices.update_finish_img_history(app, imgid)

        return {}

    @app.route("/ix", methods=["post"])
    @request_around(app, request, hasSessionId=True)
    def info_extract(sessionId):
        key = unescape(request.form.get("key", None))
        if not key:
            raise CrpException("密钥不能为空")
        imgFile = request.files.get('img', None)                    # 图像文件
        if not imgFile:
            raise CrpException("缺少图像文件")
        timeStamp = str(int(time.time()*1000000))                   # 转化为微秒级时间戳, 用作文件命名
        inpImgPath = app.config["TMP_DIR"]+timeStamp+".jpeg"        # 原始图片路径
        imgFile.save(inpImgPath)    

        # 提取图像id
        imgnum = data_extract2(inpImgPath)
        imgid = md5(str(imgnum))
        secret = imgHistoryServices.query_img_secret(app, imgid, key)
        return {'secret':secret}