from wxauto import WeChat

def send_msg(target, msg):
    wx = WeChat()
    wx.GetSessionList()
    wx.ChatWith(target)
    wx.SendMsg(msg)

# send_msg('宝', 'test')