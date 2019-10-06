import re
import random

import nonebot
from nonebot import on_command, CommandSession, Message
from nonebot.permission import *

#, permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)

re_silence = re.compile(r'来.?份(.*)睡眠套餐')

@on_command('silence', aliases=('睡眠套餐', '休眠套餐', '精致睡眠', '来一份精致睡眠套餐', re_silence)) 
async def silence(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']
    await session.bot.set_group_ban(group_id=group_id , user_id=user_id, duration=8*60*60)


bot = nonebot.get_bot()
last_msg = "(仮)"
repeated_flag = False
prob_n = 0.0
PROB_A = 1.5
'''
不复读率 随 复读次数 指数级衰减
从第2条复读，即第3条重复消息开始有几率触发复读

a 设为一个略大于1的小数，最好不要超过2，建议1.5
复读概率计算式：p_n = 1 - 1/a^n
递推式：p_n+1 = 1 - (1 - p_n) / a
'''
@bot.on_message('group')
async def random_repeater(context):
    global last_msg
    global repeated_flag
    global prob_n
    global PROB_A
    msg = context['message'].extract_plain_text()
    if last_msg == msg:
        if not repeated_flag:
            if random.random() < prob_n:    # 概率测试通过，复读并设flag
                repeated_flag = True
                await bot.send(context, msg)
            else:                           # 蓄力
                prob_n = 1 - (1-prob_n)/PROB_A  
    else:   # 不是复读，重置
        last_msg = msg
        repeated_flag = False
        prob_n = 0.0


