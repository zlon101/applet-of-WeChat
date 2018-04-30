from crp.services import sp, urlget, returnWrapper
import json

# 给初始app绑定路由，包括蓝图
def bindRoutes(app):
    @app.route("/")
    @app.route("/index")
    @returnWrapper
    def index():
        return {"msg":"服务器运行中..."}

    @app.route("/sessionBuild/<code>", methods=['POST', 'GET'])
    @returnWrapper
    def sessionBuild(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        # 获得wxid
        respstr = urlget(url, {
            "appid":app.config['APPID'],
            "secret":app.config['APPSECRET'],
            "js_code":code,
            "grant_type":"authorization_code"
        })
        respobj = json.loads(respstr)
        print(respobj)
        if(respobj.get("errcode", None)):
            raise Exception("校验code失败，errcode:"+str(respobj.get("errcode", None)))
        
        # 建立sessionId并和wxid绑定
        wxid = respobj["openid"]
        sessionId = sp.newSession(wxid)
        return {"sessionId":sessionId}