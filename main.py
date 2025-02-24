from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from . import timetable
import re

# 注册插件
@register(name="Timetable", description="自动发送当日课程表的插件", version="0.1", author="ShamiMoon")
class TimetablePlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def message_received(self, ctx: EventContext):
        # msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象

        msg = ctx.event.text_message.strip()
        if re.search(r'调试', msg, re.IGNORECASE):
            ctx.prevent_default()
            msg = msg.split(" ")
            # print(msg)
            if len(msg)==1 or len(msg)>3:
                today_weekday, current_week = 2,11
            else:
                today_weekday, current_week = int(msg[1]),int(msg[2])
                today_weekday-=1
            weekMsg = ""
            week_days = ['一', '二', '三', '四', '五', '六', '日']
            week_day_str = week_days[today_weekday]
            if current_week > 0:
                weekMsg = f"今天是星期{week_day_str}，当前是第{current_week}周："
            # 回复提示消息
            ctx.add_return("reply", ["调试信息:",weekMsg,'\n',timetable.filter_and_display_timetable(week_day_str,current_week)])
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, <发送者id>!"
            ctx.add_return("reply", ["hello, {}!".format(ctx.event.sender_id)])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        if msg == "今日课程" or msg == "今日课程表" or msg == "课程":
            weekMsg = ""
            today_weekday, current_week = timetable.get_today_week_and_day()
            week_days = ['一', '二', '三', '四', '五', '六', '日']
            week_day_str = week_days[today_weekday]
            if current_week > 0:
                weekMsg = f"今天是星期{week_day_str}，当前是第{current_week}周："
            # 回复提示消息
            ctx.add_return("reply", [weekMsg,timetable.display_today_timetable()])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        if msg == "查看课程" or msg == "查看课程表":
            ctx.add_return("reply", [timetable.displayable_all_timetable()])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        if msg == "本周课程" or msg == "本周课程表":
            ctx.add_return("reply", [timetable.display_thisWeek_timeable()])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()



    # 插件卸载时触发
    def __del__(self):
        pass
