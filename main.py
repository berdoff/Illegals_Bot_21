import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import tok,str_token,main_str_token,ip_token,mongo,berdoff_token,seraph_token
from random import randint
import json
import datetime
from pymongo import MongoClient
import time
import os
import sys
import requests
import certifi



session1=vk_api.VkApi(token=main_str_token)
vk1=session1.get_api()

session=vk_api.VkApi(token=str_token)
vk=session.get_api()

vk_session = vk_api.VkApi(token = tok)
longpoll = VkBotLongPoll(vk_session,212957523)

cluster=MongoClient(mongo,tlsCAFile=certifi.where())
db=cluster["UsersData"]
collection=db["ILLEGALS"]
archive=db["ILLEGALS_HISTORY"]
gos=db["GOS_21"]
archive_gos=db["GOS_ARCHIVE_21"]
db_forms=db["forms"]
rakbots_dostup=db["RAKBOT_DOSTUP"]

sled_kf=[12,6,1]
obzvon_kf=[13,14]
go_adm_kf=[15]
price={"1":-1_000_000,
"2":-1_500_000,
"3":-3_000_000,
"4":-5_000_000,
"5":-10_000_000}
usluga={"1":"выпуск 9-ки из тср",
"2":"выпуск 10-ки из тср",
"3":"снять устный выговор",
"4":"снять строгий выговор",
"5":"получить -3 дня к сроку"}

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}



def norm_money(money):
    money=list(str(money))
    for i in range(len(money),0,-3):
        money.insert(i,".")
    money=money[:-1]
    return "".join(money)







def go_adm(id,nick):
        user=collection.find_one({"nick" : nick, "rank" : "Лидер"})
        nick=user["nick"]
        add_data=user["add_data"]
        srok=user["srok_data"]
        rank=user["rank"]+" "+user["frac"]
        id_vk=str(user["id_vk"])
        vk_user="https://vk.com/id"+id_vk
        int_id_vk=user["id_vk"]
        msg_to_user=f"Привет, тебе было выдано право на заполнение формы на пост хелпера\nЗаполни в течение 24 часов\nhttp://admin-tools.ru/a/setadm.php"
        forma=f"Ник: {nick} \nДата назначения:{add_data} \nДата окончания срока:{srok} \nЛидерка:{rank} \n ВК:{vk_user}"
        command=f"!padm @id{id_vk}"
        str_send(339,forma)
        str_send(339,command)
        chat_sender(id,f"✅Лидеру {nick} было выдано право на заполнение формы")
        str_send_to_user(int_id_vk,msg_to_user)
        chat_sender(id,f"✅Лидеру {nick} было отправлено сообщение о форме")

def str_send_to_user(id,text):
        session1.method('messages.send', {'user_id' : id, 'message' : text,'random_id' : 0})
def chet_online(hours,minutes,seconds):
        minutes+=seconds//60
        seconds=seconds%60
        hours+=minutes//60
        minutes=minutes%60
        online=f'{hours}:{minutes}:{seconds}'
        return online

def get_online(nick,type,author_nick):
        last_use=collection.find_one({"type":"kd"})["online"]
        last_use=datetime.datetime.strptime(last_use, '%Y-%m-%d %H:%M:%S.%f')
        print(last_use)
        now=datetime.datetime.now()
        print(now)
        kd=last_use-now
        print(kd)
        print(kd.days)
        print(kd.seconds)
        if kd.days<=-1 or type==0:
            header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
            a = requests.get("http://berdoff.ru/getonline",data={"token": berdoff_token, "nick": nick,"server":"21"}).text
            print(a)
            online=json.loads(a)
            text_online='⏳ '+nick+' ⏳'+'\n'+'\n'
            today = datetime.date.today()
            monday = today - datetime.timedelta(days=today.weekday())
            monday_online=''
            hours=0
            minutes=0
            seconds=0
            for i in range(7):
                if i>0:
                    day=monday+datetime.timedelta(days=i)
                else:
                    day=monday
                try:
                    day_online=online["online"][f'{day}']
                    text_online+=str(day)+' '+day_online+'\n'
                    day_hours=day_online.split(':')[0]
                    day_minutes=day_online.split(':')[1]
                    day_seconds=day_online.split(':')[2]
                    hours+=int(day_hours)
                    minutes+=int(day_minutes)
                    seconds+=int(day_seconds)
                except:
                    text_online+=str(day)+' 00:00:00'+'\n'
            full_online=chet_online(hours,minutes,seconds)
            text_online+='\n'+'Онлайн за последнюю неделю: '+full_online
            if type==1:
                kd_time=now+datetime.timedelta(minutes=0.5)
                kd_time=str(kd_time)
                collection.update_one({"type":"kd"},{"$set":{"online":kd_time}})
            return text_online
        else:
            a=f'❗ КД! Осталось подождать {kd.seconds} сек.'
            return a


def get_online_lw(nick, type, author_nick):
    last_use = collection.find_one({"type": "kd"})["online"]
    last_use = datetime.datetime.strptime(last_use, '%Y-%m-%d %H:%M:%S.%f')
    print(last_use)
    now = datetime.datetime.now()
    print(now)
    kd = last_use - now
    print(kd)
    print(kd.days)
    print(kd.seconds)
    if kd.days <= -1 or type == 0:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
        a= requests.get("http://berdoff.ru/getonline",data={"token":berdoff_token,"nick":nick}).text
        print(a)
        online = json.loads(a)
        text_online = '⏳ ' + nick + ' ⏳' + '\n' + '\n'
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())-datetime.timedelta(days=7)
        monday_online = ''
        hours = 0
        minutes = 0
        seconds = 0
        for i in range(7):
            if i > 0:
                day = monday + datetime.timedelta(days=i)
            else:
                day = monday
            try:
                day_online = online["online"][f'{day}']
                text_online += str(day) + ' ' + day_online + '\n'
                day_hours = day_online.split(':')[0]
                day_minutes = day_online.split(':')[1]
                day_seconds = day_online.split(':')[2]
                hours += int(day_hours)
                minutes += int(day_minutes)
                seconds += int(day_seconds)
            except:
                text_online += str(day) + ' 00:00:00' + '\n'
        full_online = chet_online(hours, minutes, seconds)
        text_online += '\n' + 'Онлайн за последнюю неделю: ' + full_online
        if type == 1:
            kd_time = now + datetime.timedelta(minutes=0.5)
            kd_time = str(kd_time)
            collection.update_one({"type": "kd"}, {"$set": {"online": kd_time}})
        return text_online
    else:
        a = f'❗ КД! Осталось подождать {kd.seconds} сек.'
        return a

def proverka(leader,p):
        nick=leader["nick"]
        org=leader["frac"]
        id_vk=leader["id_vk"]
        p=int(p)
        a=requests.post("https://seraphtech.site/api/v2/leader.add", data={"token":seraph_token,"nick":nick, "fraction":org, "vkid":f"{id_vk}","removal":p})
        return a


def str_send(id,text):
    session1.method('messages.send', {'chat_id' : id, 'message' : text,'random_id' : 0})

def chat_sender(id, text):
        a=text.split("\n")
        b=""
        if len(text)>1200:
            for i in a:
                b+=i+"\n"
                if len(b)>1200:
                    print(b)
                    vk_session.method('messages.send', {'chat_id' : id, 'message' : b, 'disable_mentions': 1 ,'random_id' : 0})
                    time.sleep(1)
                    b=""
            vk_session.method('messages.send', {'chat_id' : id, 'message' : b, 'disable_mentions': 1 ,'random_id' : 0})
        else:      
            vk_session.method('messages.send', {'chat_id' : id, 'message' : text, 'disable_mentions': 1 ,'random_id' : 0})

def Alert(id,text):
    vk_session.method('messages.send', {'chat_id' : id, 'message' : text,'random_id' : 0})

def get_id_by_tag(msg):
    return str(msg).split("id")[1].split("|")[0]

def add_ghetto_zam_konf(user_id,nick_zama):
        try:
            session.method('messages.addChatUser',{'chat_id':74,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_zama+'] был успешно добавлен в беседу Забивы каптов')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_zama+'] не удалось добавить в беседу Забивы каптов')
        try:
            session.method('messages.addChatUser',{'chat_id':73,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_zama+'] был успешно добавлен в беседу Курилка гетто')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_zama+'] не удалось добавить в беседу Курилка гетто')

def add_mafii_zam_konf(user_id,nick_zama):
    try:
        session.method('messages.addChatUser',{'chat_id':76,'user_id':user_id})
        chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_zama+'] был успешно добавлен в беседу Забивы стрел')
    except:
        chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_zama+'] не удалось добавить в беседу Забивы стрел')
    try:
        session.method('messages.addChatUser',{'chat_id':75,'user_id':user_id})
        chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_zama+'] был успешно добавлен в беседу Курилка мафий')
    except:
        chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_zama+'] не удалось добавить в беседу Курилка мафий')

def add_ghetto_leader_konf(user_id,nick_user):
        try:
            session.method('messages.addChatUser',{'chat_id':74,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Забивы каптов')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Забивы каптов')
        try:
            session.method('messages.addChatUser',{'chat_id':73,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Курилка гетто')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Курилка гетто')
        try:
            session.method('messages.addChatUser',{'chat_id':190,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Лидеры гетто')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Лидеры гетто')

def add_mafii_leader_konf(user_id,nick_user):
        try:
            session.method('messages.addChatUser',{'chat_id':76,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Забивы стрел')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Забивы стрел')
        try:
            session.method('messages.addChatUser',{'chat_id':75,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Курилка мафий')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Курилка мафий')
        try:
            session.method('messages.addChatUser',{'chat_id':71,'user_id':user_id})
            chat_sender(id,'Пользователь '+'[id'+str(user_id)+'|'+nick_user+'] был успешно добавлен в беседу Лидеры мафий')
        except:
            chat_sender(id,'Пользователя '+'[id'+str(user_id)+'|'+nick_user+'] не удалось добавить в беседу Лидеры мафий')

def add_kf(vk,frac_id,role,frac,nick):
    frac_id=int(frac_id)
    if role=="Лидер" and frac_id in ghetto_frac:
        add_ghetto_leader_konf(vk,nick)
    if role=="Лидер" and frac_id in mafia_frac:
        add_mafii_leader_konf(vk,nick)
    if role=="Заместитель" and frac_id in ghetto_frac:
        add_ghetto_zam_konf(vk,nick)
    if role=="Заместитель" and frac_id in mafia_frac:
        add_mafii_zam_konf(vk,nick)

def del_ghetto_zam_konf(user_id):
        try:
            session.method('messages.removeChatUser',{'chat_id':74,'user_id':user_id})
        except:
            b=''
        try:
            session.method('messages.removeChatUser',{'chat_id':73,'user_id':user_id})
        except:
            pass
def del_mafii_zam_konf(user_id):
    try:
        session.method('messages.removeChatUser',{'chat_id':76,'user_id':user_id})
    except:
        b=''
    try:
        session.method('messages.removeChatUser',{'chat_id':75,'user_id':user_id})
    except:
        pass
def del_ghetto_leader_konf(user_id):
    try:
        session.method('messages.removeChatUser',{'chat_id':74,'user_id':user_id})
    except:
        b=''
    try:
        session.method('messages.removeChatUser',{'chat_id':73,'user_id':user_id})
    except:
        pass
    try:
        session.method('messages.removeChatUser',{'chat_id':72,'user_id':user_id})
    except:
        pass
def del_leader_mafii_konf(user_id):
    try:
        session.method('messages.removeChatUser',{'chat_id':71,'user_id':user_id})
    except:
        b=''
    try:
        session.method('messages.removeChatUser',{'chat_id':75,'user_id':user_id})
    except:
        pass
    try:
        session.method('messages.removeChatUser',{'chat_id':76,'user_id':user_id})
    except:
        pass

def add_friend(user_id):
        session.method('friends.add',{'user_id':user_id})

def remove_kf(nick,id):
    id_vk=collection.find_one({"nick":nick})["id_vk"]
    role=collection.find_one({"nick":nick})["rank"]
    del_ghetto_leader_konf(id_vk)
    del_leader_mafii_konf(id_vk)
    chat_sender(id,f"{role} {nick} был успешно кикнут с кф")
    
def set_warn(nick,edit,prichina,id_authora,admin):
    user=collection.find_one({"nick":nick})
    user["preds"]=user["vigs"]*3+user["preds"]+int(edit)
    user["vigs"]=user["preds"]//3
    user["preds"]=user["preds"]%3
    collection.update_one({"nick":nick},{"$set":{"vigs":user["vigs"],"preds":user["preds"]}})
    if admin==1:
        collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены предупреждения @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
        chat_sender(id,f"✅Лидеру {nick} изменены предупреждения @id{id_authora}(администратором) на {edit} по причине: {prichina}")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены предупреждения @id{id_authora}(администратором) на {edit} по причине: {prichina}")
    elif admin==0:
        collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены предупреждения системой на {edit} по причине: {prichina}"}})
        chat_sender(id,f"✅Лидеру {nick} изменены предупреждения системой на {edit} по причине: {prichina}")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены предупреждения системой на {edit} по причине: {prichina}")
                      
def set_vig(nick,edit,prichina,id_authora,admin):
    user=collection.find_one({"nick":nick})
    user["vigs"]=eval(str(user["vigs"])+edit)
    if admin==1:
        chat_sender(id,f"✅Лидеру {nick} изменены выговоры @id{id_authora}(администратором) на {edit} по причине: {prichina} ")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены выговоры @id{id_authora}(администратором) на {edit} по причине: {prichina} ")
        collection.update_one({"nick":nick},{"$set":{"vigs":user["vigs"]}})
        collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены выговоры @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
    elif admin==0:
        chat_sender(id,f"✅Лидеру {nick} изменены выговоры системой на {edit} по причине: {prichina} ")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены выговоры системой на {edit} по причине: {prichina} ")
        collection.update_one({"nick":nick},{"$set":{"vigs":user["vigs"]}})
        collection.update_one({"nick":nick},{"$set":{"warn_history":user["warn_history"]+f"\nИзменены выговоры системой на {edit} по причине: {prichina}"}})


def set_day(nick,edit,prichina,id_authora,admin):
    user=collection.find_one({"nick":nick})
    srok_data=user["srok_data"]
    srok_data=datetime.datetime.strptime(srok_data,"%d.%m.%Y")
    srok_data=srok_data+datetime.timedelta(days=int(edit))
    srok_data=str(srok_data.day)+'.'+str(srok_data.month)+'.'+str(srok_data.year)
    if admin==1:
        chat_sender(id,f"✅Лидеру {nick} изменены дни @id{id_authora}(администратором) на {edit} по причине: {prichina} ")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены дни @id{id_authora}(администратором) на {edit} по причине: {prichina} ")
        collection.update_one({"nick":nick},{"$set":{"srok_data":srok_data}})
        collection.update_one({"nick":nick},{"$set":{"days_history":user["days_history"]+f"\nИзменены дни @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
    if admin==0:
        chat_sender(id,f"✅Лидеру {nick} изменены дни системой на {edit} по причине: {prichina} ")
        chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены дни системой на {edit} по причине: {prichina} ")
        collection.update_one({"nick":nick},{"$set":{"srok_data":srok_data}})
        collection.update_one({"nick":nick},{"$set":{"days_history":user["days_history"]+f"\nИзменены дни системой на {edit} по причине: {prichina}"}})

def AddVoprNRP(vopros):
    voprosi=collection.find_one({"type":'voprosi'})['nrpvopr']
    voprosi+='\n'+vopros
    collection.update_one({"type":'voprosi'},{"$set":{"nrpvopr" : voprosi}})
    chat_sender(id,'Вопрос: '+vopros+' успешно добавлен в БД вопросов нрп банд.')

def AddVoprMaf(vopros):
    voprosi=collection.find_one({"type":'voprosi'})['mafiivopr']
    voprosi+='\n'+vopros
    collection.update_one({"type":'voprosi'},{"$set":{"mafiivopr" : voprosi}})
    chat_sender(id,'Вопрос: '+vopros+' успешно добавлен в БД вопросов мафий.')

def AddVoprRP(vopros):
    voprosi = collection.find_one({"type": 'voprosi'})['rpvopr']
    voprosi += '\n' + vopros
    collection.update_one({"type": 'voprosi'}, {"$set": {"rpvopr": voprosi}})
    chat_sender(id, 'Вопрос: ' + vopros + ' успешно добавлен в БД вопросов рп банд.')


def AddVoprOpen(vopros):
    voprosi = collection.find_one({"type": 'voprosi'})['openvopr']
    voprosi += '\n' + vopros
    collection.update_one({"type": 'voprosi'}, {"$set": {"openvopr": voprosi}})
    chat_sender(id, 'Вопрос: ' + vopros + ' успешно добавлен в БД вопросов рп банд.')

print("Bot started")



ghetto_frac=[11,12,13,14,15,25]
mafia_frac=[16,17,18,19]

name_fracs1={
    "11":"Grove Street",
    "12":"Los Santos Vagos",
    "13":"East Side Ballas",
    "14":"Varrios Los Aztecas",
    "15":"The Rifa",
    "16":"Russian Mafia",
    "17":"Yakuza",
    "18":"La Cosa Nostra",
    "19":"Warlock MC",
    "25":"Night Wolfs"
    
}


vigs_frac={
    
}

vigs_cf={
    11:19,
    12:19,
    13:19,
    14:19,
    15:19,
    16:5,
    17:5,
    18:5,
    19:5,
    25:19
}



try:
    for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                try:
                    id_authora=str(event.object.message['from_id'])
                    msg = event.object.message['text'].lower()
                    norm_msg=event.object.message['text']
                    print(event.object.message['text'])
                    if event.from_chat:         
                        id = event.chat_id
                        if str(msg).split()[0]=='/id_be':
                            chat_sender(id,"ID беседы: "+str(id))
                        if str(msg).split()[0]=='/lids':
                            a=collection.find({"rank":"Лидер"}).sort("frac_id")
                            b=""
                            for i in a:
                                b+="📝 "+i["rank"]+" "+i["frac"]+" @id"+i["id_vk"]+"("+i["nick"]+")"+"\n"
                            chat_sender(id,b)

                        if str(msg).split()[0] == '/lhistory' and id==16:
                            data_start=norm_msg.split()[1]
                            data_end = norm_msg.split()[2]
                            chat_sender(id,"⚙ Загрузка информации о поставленных/снятых лидерах ⚙")
                            data_start = datetime.datetime.strptime(data_start, '%d.%m.%Y')
                            data_start = str(data_start.day) + '.' + str(data_start.month) + '.' + str(data_start.year)
                            data_end = datetime.datetime.strptime(data_end, '%d.%m.%Y')
                            data_end = str(data_end.day) + '.' + str(data_end.month) + '.' + str(data_end.year)
                            leaders_add=[]
                            leaders_del=[]
                            while data_start!=data_end:
                                leaders_add.append(collection.find({"add_data":str(data_start),"dostup":"1"}))
                                leaders_add.append(gos.find({"add_data": str(data_start),"dostup":"1"}))
                                leaders_add.append(archive_gos.find({"add_data": str(data_start), "dostup": "1"}))
                                leaders_add.append(archive.find({"add_data": str(data_start), "dostup": "1"}))
                                for i in archive.find():
                                    if data_start in i["snyatie"]:
                                        leaders_del.append(i)
                                for i in archive_gos.find():
                                    if data_start in i["snyatie"]:
                                        leaders_del.append(i)
                                data_start=datetime.datetime.strptime(data_start, '%d.%m.%Y')
                                data_start=(data_start+datetime.timedelta(days=1))
                                data_start=str(data_start.day)+'.'+str(data_start.month)+'.'+str(data_start.year)
                            spisok=""

                            for i1 in leaders_add:
                                for i in i1:
                                    try:
                                        spisok+=i["add_data"]+" поставлен "+i["role"]+" "+i["frac"]+" "+i["nick"]+" "+i["type_add"]+"\n"
                                    except:
                                        spisok+=i["add_data"]+" поставлен "+i["rank"]+" "+i["frac"]+" "+i["nick"]+" "+i["type_add"]+"\n"
                            spisok+="------------------------------------------------------------------------\n"
                            print(spisok)
                            for i in leaders_del:
                                try:
                                    spisok+=i["snyatie"].split()[0]+" снят "+i["role"]+" "+i["frac"]+" "+i["nick"]+" Причина: "+" ".join(i["snyatie"].split()[1:])+"\n"
                                except:
                                    spisok+=i["snyatie"].split()[-1]+" снят "+i["rank"]+" "+i["frac"]+" "+i["nick"]+" Причина: "+" ".join(i["snyatie"].split()[:-1])+"\n"
                            print(spisok)
                            if spisok!="":
                                chat_sender(16,spisok)
                            else:
                                chat_sender(16, "❗Используйте /lhistory [дата начала] [дата конца(не включительно)]")

                        if str(msg).split()[0] == '/check' and id == 17:
                            if str(msg)=="/check":
                                chat_sender(id,"❗ Используйте /check [nick/id] [server]")
                            else:
                                chat_sender(id,"⚙Ожидайте загрузки...")
                                nick=norm_msg.split()[1]
                                server=norm_msg.split()[2]
                                chat_sender(id,check_chs(nick,server))

                        if str(msg).split()[0] == '/gstore':
                            if db_forms.find_one({"user":id_authora})["dostup"]=="1":
                                if len(str(msg).split())>1:
                                    id_store=norm_msg.split()[1].strip()
                                    if id_store in ["11","12","13","14","15","25"] :
                                        forms_bd=db["forms"]
                                        forms_bd.insert_one({"forma":f"/addorgmats {id_store}","author":id_authora,"status":0})
                                        chat_sender(id,"Форма записана, ожидайте пополнения в течение 30 секунд")
                                    else:
                                        chat_sender(id,"Ошибка. ID Фракций:\n\nGrove: 11\nVagos: 12\nBallas: 13\nAztec: 14\nRifa: 15\nNight Wolfs: 25")
                                else:
                                    chat_sender(id,"Ошибка. ID Фракций:\n\nGrove: 11\nVagos: 12\nBallas: 13\nAztec: 14\nRifa: 15\nNight Wolfs: 25")
                            else:
                                chat_sender(id,"Отсутствует доступ")


                        if str(msg).split()[0] == '/game' and id==16:
                            if db_forms.count_documents({"user":id_authora})!=0:
                                print(1)
                                if db_forms.find_one({"user":id_authora})["dostup"]=="1":
                                    forms_bd=db["forms"]
                                    a=norm_msg.replace("/game","").strip()
                                    a=a.split("\n")
                                    for i in a:
                                        forms_bd.insert_one({"forma":i,"author":id_authora,"status":0})
                                    chat_sender(16,"+")
                                else:
                                    chat_sender(16,"Access denied")
                            else:
                                chat_sender(16,"Access denied")


                        if str(msg).split()[0] == '/dostup':
                            if id_authora=="178391887" or id_authora=="180732606":
                                id_user=get_id_by_tag(str(msg).split()[1])
                                dostup=str(msg).split()[2]
                                print(dostup)
                                if db_forms.count_documents({"user":id_user})!=0:
                                    db_forms.update_one({"user":id_user},{"$set":{"dostup":dostup}})
                                    chat_sender(id,"Доступ изменен")
                                else:
                                    db_forms.insert_one({"user":id_user,"dostup":dostup})
                                    chat_sender(id,"Доступ изменен")

                        if str(msg).split()[0] == '/dr' and id==17:
                                id_user=get_id_by_tag(str(msg).split()[1])
                                dostup=str(msg).split()[3]
                                nick=norm_msg.split()[2]
                                if rakbots_dostup.count_documents({"vk":id_user})!=0:
                                    rakbots_dostup.delete_one({"vk":id_user})
                                    chat_sender(id,"Доступ изменен")
                                else:
                                    rakbots_dostup.insert_one({"vk":id_user,"dostup":dostup,"nick":nick})
                                    chat_sender(id,"Доступ изменен")
                                

                        if str(msg).split()[0]=='/zams':
                            users=collection.find({"dostup":"0"}).sort("frac_id")
                            d=""
                            c=""
                            for i in users:
                                if i["frac_id"] in ghetto_frac:
                                    c+="📝 "+i["rank"]+" "+i["frac"]+" @id"+i["id_vk"]+"("+i["nick"]+")"+"\n"
                                if i["frac_id"] in mafia_frac:
                                    d+="📝 "+i["rank"]+" "+i["frac"]+" @id"+i["id_vk"]+"("+i["nick"]+")"+"\n"
                            b=f"👤 Замы гетто:<br><br>{c}<br>👤 Замы мафий:<br><br>{d}"
                            chat_sender(id,b)
                        if str(msg).split()[0]=="/galert" and id in sled_kf:
                            msg=norm_msg.replace("/galert","")
                            lids=collection.find({"dostup":"1"})
                            tags=""
                            for i in lids:
                                if i["frac_id"] in ghetto_frac:
                                    id_vk=i["id_vk"]
                                    tags+=f"@id{id_vk}(ᅠ) "
                            Alert(4,f"📢 {msg} \n 🗣 @id{id_authora}(Администратор)\n {tags}")



                        if str(msg).split()[0]=="/malert" and id in sled_kf:
                            msg=norm_msg.replace("/malert","")
                            lids=collection.find({"dostup":"1"})
                            tags=""
                            for i in lids:
                                if i["frac_id"] in mafia_frac:
                                    id_vk=i["id_vk"]
                                    tags+=f"@id{id_vk}(ᅠ) "
                            Alert(5,f"📢 {msg} \n 🗣 @id{id_authora}(Администратор)\n {tags}")
                        if str(msg).split()[0]=='/nrpobzvon' and id in obzvon_kf:
                            nrpvopr=collection.find_one({"type":'voprosi'})["nrpvopr"].split('\n')
                            k1=1
                            t=[]
                            k=-1
                            getvoprnrp=''
                            while k1!=21:
                                k=randint(0,len(nrpvopr)-1)
                                if not(str(k) in t):
                                    getvoprnrp=getvoprnrp+'\n'+str(k1)+'. '+nrpvopr[k]+'\n'+' '
                                    k1+=1
                                    t.append(str(k))
                            chat_sender(id,getvoprnrp)
                            k1=1
                            t=[]
                            k=-1
                        if str(msg).split()[0]=='/rpobzvon' and id in obzvon_kf:
                            rpvopr=collection.find_one({"type":'voprosi'})["rpvopr"].split('\n')
                            f1=1
                            g=[]
                            f=-1
                            getvoprrp=''
                            while f1!=21:
                                f=randint(0,len(rpvopr)-1)
                                if not(str(f) in g):
                                    getvoprrp=getvoprrp+'\n'+str(f1)+'. '+rpvopr[f]+'\n'+' '
                                    f1+=1
                                    g.append(str(f))
                            chat_sender(id,getvoprrp)
                            f1=1
                            g=[]
                            f=-1
                        if str(msg).split()[0]=='/openobzvon' and id in obzvon_kf:
                            rpvopr=collection.find_one({"type":'voprosi'})["openvopr"].split('\n')
                            f1=1
                            g=[]
                            f=-1
                            getvoprrp=''
                            while f1!=21:
                                f=randint(0,len(rpvopr)-1)
                                if not(str(f) in g):
                                    getvoprrp=getvoprrp+'\n'+str(f1)+'. '+rpvopr[f]+'\n'+' '
                                    f1+=1
                                    g.append(str(f))
                            chat_sender(id,getvoprrp)
                            f1=1
                            g=[]
                            f=-1

                        if str(msg).split()[0]=='/addfr':
                            add_id1=str(str(msg).split()[1])
                            add_id=str(add_id1).split("id")[1].split("|")[0]
                            add_friend(add_id)
                            chat_sender(id,'Заявка отправлена')

                        if str(msg).split()[0]=='/setnick' and id in sled_kf:
                            id_vk=get_id_by_tag(norm_msg.split()[1])
                            new_nick=norm_msg.split()[2]
                            if "_" in norm_msg:
                                nick=collection.find_one({"id_vk":id_vk})["nick"]
                                collection.update_one({"id_vk":id_vk},{"$set":{"nick":new_nick}})
                                chat_sender(id,f"Игроку {nick} был изменен ник на {new_nick}")
                            else:
                                chat_sender(id,"Отсутствует символ _ , следящего на мыло!")

                        if str(msg).split()[0]=='/mafiiobzvon' and id in obzvon_kf:
                            mafiivopr=collection.find_one({"type":'voprosi'})["mafiivopr"].split('\n')
                            j1=1
                            u=[]
                            j=-1
                            getvoprmafii=''
                            print(mafiivopr)
                            while j1!=21:
                                j=randint(0,len(mafiivopr)-1)
                                if not(str(j) in u):
                                    getvoprmafii=getvoprmafii+'\n'+str(j1)+'. '+mafiivopr[j]+'\n'+' '
                                    j1+=1
                                    u.append(str(j))
                            chat_sender(id,getvoprmafii)
                            j1=1
                            u=[]
                            j=-1
                        if str(msg).split()[0]=='/chet':
                            ObzvMiss=str(event.object.message['text']).split()[1]+' ошибся в вопросах: '
                            balli=str(msg).split()[2]
                            chat_sender(id,str(event.object.message['text']).split()[1]+' набрал '+str(str(msg).split()[2].count('1'))+' баллов')
                            for i in range(len(balli)):
                                if balli[i]=='0':
                                    ObzvMiss+=str(i+1)+', '
                            chat_sender(id,str(ObzvMiss))
                        if str(msg).split()[0]=='/zamdel':
                            try:
                                nick=norm_msg.split()[1]
                                if (id in sled_kf) or ((collection.find_one({"id_vk":id_authora})["frac_id"]==collection.find_one({"nick":nick})["frac_id"]) and collection.find_one({"id_vk":id_authora})["dostup"]=="1" and collection.find_one({"nick":nick})["dostup"]=="0"):
                                    print(1)
                                    remove_kf(nick,id)
                                    print(2)
                                    collection.delete_one({"nick":nick})
                            except:
                                chat_sender(id,"❗Используйте /zamdel [nick]")

                        if str(msg).split()[0] == '/duplicatevopr' and id_authora=="178391887":
                            a=db["UsersCollection"]
                            collection.insert_one(a.find_one({"type":"voprosi"}))
                            chat_sender(id,"Вопросы с сервера гилберт скопированы")


                        if str(msg).split()[0]=='/add_all':
                            follow_count=session.method('users.getFollowers',{'user_id': 519824619})['count']
                            print(follow_count)
                            if follow_count>0:
                                follow_list=session.method('users.getFollowers',{'user_id': 519824619})['items']
                                chat_sender(id,'Сейчас заявок в друзья у бота: '+str(follow_count))
                                chat_sender(id,'Добавляю всех')
                                for i in range(len(follow_list)):
                                    add_friend(follow_list[i])
                                chat_sender(id,'Все пользователи были успешно добавлены')
                            else:
                                chat_sender(id,'Сейчас нет заявок в друзья')

                        if str(msg).split()[0]=='/myonl' or str(msg).split()[0]=='/myonline':
                            nick=collection.find_one({"id_vk":str(event.object.message['from_id'])})["nick"]
                            author_nick=collection.find_one({"id_vk":str(event.object.message['from_id'])})["nick"]
                            online=get_online(nick,1,author_nick)
                            chat_sender(id,online)
                        if str(msg).split()[0]=='/online':
                            nick=str(event.object.message['text']).split()[1]
                            chat_sender(id,get_online(nick,1,"1"))
                        if str(msg).split()[0]=='/lw_onl':
                            nick=str(event.object.message['text']).split()[1]
                            chat_sender(id,get_online_lw(nick,1,"1"))
                        if str(msg).split()[0]=='/goadm':
                            if id in go_adm_kf:
                                nick=str(event.object.message['text']).split()[1]
                                go_adm(id,nick)
                            else:
                                chat_sender(id,"Нет доступа")   
                        if (str(msg).split()[0]=='/vig' or str(msg).split()[0]=='/setvig') and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1]
                                prichina=" ".join(norm_msg.split()[3:])
                                edit=norm_msg.split()[2]
                                set_vig(nick,edit,prichina,id_authora,1)
                            except:
                                chat_sender(id,"❗Используйте /vig [nick] [+/-количество] [причина]")
                        if str(msg).split()[0]=='/litrbol' and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1]
                                user=collection.find_one({"nick":nick})
                                prichina=" ".join(norm_msg.split()[3:])
                                edit=norm_msg.split()[2]
                                edit=edit.replace(",",".")
                                user["main_balls"]=eval(str(user["main_balls"])+edit)
                                collection.update_one({"nick":nick},{"$set":{"main_balls":user["main_balls"]}})
                                collection.update_one({"nick":nick},{"$set":{"main_balls_history":user["main_balls_history"]+f"\nИзменены баллы @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
                                chat_sender(id,f"✅Лидеру {nick} изменены основные баллы @id{id_authora}(администратором) на {edit} по причине: {prichina}")
                                chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменены основные баллы @id{id_authora}(администратором) на {edit} по причине: {prichina}")
                            except:
                                chat_sender(id,"❗Используйте /litrbol [nick] [+/-количество] [причина]")
                        if str(msg).split()[0]=='/warn_history' and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1]
                                chat_sender(id,f"📝 {nick}<br>"+collection.find_one({"nick":nick})["warn_history"])
                            except:
                                chat_sender(id,"❗Используйте /warn_history [nick]")
                        
                        if str(msg).split()[0]=='/litrbol_history' and id in sled_kf:
                            nick=norm_msg.split()[1]
                            chat_sender(id,f"📝 {nick}<br>"+collection.find_one({"nick":nick})["main_balls_history"])


                        if (str(msg).split()[0]=='/warn' or str(msg).split()[0]=='/setwarn') and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1]
                                prichina=" ".join(norm_msg.split()[3:])
                                edit=norm_msg.split()[2]
                                set_warn(nick,edit,prichina,id_authora,1)
                            except:
                                chat_sender(id,"❗Используйте /warn [nick] [+/-количество] [причина]")


                        if str(msg).split()[0]=='/setday' and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1]
                                prichina=" ".join(norm_msg.split()[3:])
                                edit=norm_msg.split()[2]
                                set_day(nick,edit,prichina,id_authora,1)
                            except:
                                chat_sender(id,"❗Используйте /setday [nick] [+/-количество] [причина]")

                        
                        if str(msg).split()[0]=='/ahelp' and id in sled_kf:
                            helpp="""Команды:

                            /warn [nick] [+/-количество] [причина] - изменить кол-во предупреждений лидеру
                            /vig [nick] [+/-количество] [причина] - изменить кол-во выговоров лидеру
                            /setday [nick] [+/-количество] [причина] - изменить кол-во дней лидеру
                            /litrbol [nick] [+/-количество] [причина] - изменить кол-во основных баллов лидеру
                            /warn_history [nick] история наказания лидера
                            /litrbol_history [nick] история основных баллов лидера
                            /editbalance [nick] [+/- количество] [причина] - изменить баланс лидеру
                            /balance_history [nick] - история изменений баланса лидера
                            /tagfrac - ид фракций
                            /l_add - форма на постановление лидера/зама
                            /l_del [nick] [причина] - снять лидера
                            /info [@tag/nick] - узнать статистику
                            /zamdel [nick] - снять зама
                            /lids - список лидеров
                            /zams - список замов
                            /nrpobzov - генерирует вопросы для обзвона на нрп банду
                            /rpobzvon - генерирует вопросов для обзвона на рп банду
                            /mafiiobzvon - генерирует вопросы для обзвона на мафию
                            /voprrp - все вопросы в базе данных для рп банд
                            /voprnrp - все вопросы в базе данных для нрп банд
                            /voprmafii - все вопросы в базе данных для мафий"""
                            chat_sender(id,helpp)
                        if str(msg).split()[0]=='/help':
                            chat_sender(id,"""Доступны команды:
/gleaders - список лидеров гетто
/mleaders - список лидеров мафий
/zams - cписок замов 
/zamdel nick - кикнуть 9-ку из конф
/zamadd [@tag] [nick] - добавить 9-ку в кф
/info (@tag или Ni_Ck) - информация о человеке
/myonl - узнать свой онлайн(временно недоступна)
/shop - магазин для лидеров мафий""")
                        
                        if str(msg).split()[0]=='/l_del' and id in sled_kf:
                            try:
                                nick=norm_msg.split()[1].strip()
                                user=collection.find_one({"nick":nick})
                                if user["dostup"]=="1":
                                    prichina=" ".join(norm_msg.split()[2:])
                                    if prichina!="":
                                        today_date=datetime.datetime.today()
                                        date_today=str(today_date.day)+'.'+str(today_date.month)+'.'+str(today_date.year)
                                        str_send(328,f"Ник снимаемого лидера: {nick}<br>Какая фракция: "+user["frac"]+f"<br>За что снят: {prichina}<br>VK: https://vk.com/id"+user["id_vk"]+"<br>Дата снятия: "+str(date_today))
                                        remove_kf(nick,id)
                                        a=collection.find_one({"nick":nick})
                                        a["snyatie"]=str(prichina)+" "+date_today
                                        collection.delete_one({"nick":nick})
                                        archive.insert_one(a)
                                        chat_sender(id,"Лидер занесён в архив")
                                        proverka(a,1)
                                        chat_sender(id,"Лидер отправлен на проверку тех.администраторам")
                                    else:
                                        chat_sender(id,"В следующий раз с такой причиной сниму тебя!")
                                else:
                                    chat_sender(id,"Данный игрок не является лидером")
                            except:
                                chat_sender(id,"❗Используйте /l_del [nick]")

                        if str(msg).split()[0] == '/addkf' and id in sled_kf:
                            nick=norm_msg.split()[1]
                            user=collection.find_one({"nick":nick})
                            add_kf(user["id_vk"],user["frac_id"],user["rank"],user["frac"],nick)

                        if str(msg).split()[0] == '/zamadd':
                            if "_" in str(msg):
                                try:
                                    frac_id=collection.find_one({"id_vk":id_authora})["frac_id"]
                                    nick=norm_msg.split()[2]
                                    id_vk=get_id_by_tag(str(msg).split()[1])
                                    if collection.count_documents({"nick":nick})==0 and collection.count_documents({"id_vk":id_vk})==0:
                                        print(frac_id)
                                        if collection.find_one({"id_vk":id_authora})["dostup"]=="1":
                                            today_date=datetime.datetime.today()
                                            date_today=str(today_date.day)+'.'+str(today_date.month)+'.'+str(today_date.year)
                                            srok_data=today_date+datetime.timedelta(days=30)
                                            srok_data=str(srok_data.day)+'.'+str(srok_data.month)+'.'+str(srok_data.year)
                                            frac=name_fracs1[str(frac_id)]
                                            print(frac)
                                            
                                            
                                            print(nick)
                                            chat_sender(id,f"@id{id_vk}({nick})<br>📝Должность: Заместитель<br>📝Фракция:{frac}")
                                            add_kf(id_vk,frac_id,"Заместитель",frac,nick)
                                            collection.insert_one({"nick":nick,"vozrast":"15","frac":frac,"dostup":"0","rank":"Заместитель","type_add":"АБ","id_vk":id_vk,"frac_id":frac_id,"vigs":0,"preds":0,"warn_history":"","add_data":date_today,"srok_data":srok_data,"days_history":"","main_balls":0,"main_balls_history":""})
                                    else:
                                        chat_sender(id,"Игрок уже является лидером или замом")
                                except:
                                    chat_sender(id,"❗Используйте /zamadd [@tag] [nick]")
                            else:
                                chat_sender(id,"❗Отсутсвует нижнее подчёркивание в нике")

                                


                        if str(msg).split()[0] == '/hfind' and id in sled_kf:
                            argg = str(event.object.message['text']).split()[1]
                            print(argg)
                            if archive.count_documents({"nick": argg}) == 0:
                                argg = str(argg).split("id")[1].split("|")[0]
                                users = archive.find({"id_vk": argg})
                            else:
                                users=archive.find({"nick":argg}) 
                            
                            for user in users:
                                try:
                                    nick = user["nick"]
                                    print(nick)
                                    vk = "https://vk.com/id"+str(user["id_vk"])
                                    rank = user["rank"]+" "+user["frac"]
                                    id_vk = user["id_vk"]
                                    prichina = user["snyatie"]
                                    add_data = user["add_data"]
                                    chat_sender(id,'Ник: ' + '[id' + id_vk + '|' + nick + ']' + '\n' + 'ВК: ' + vk + '\n' + 'Должность: ' + rank + '\n' + "Дата постановления: " + str(add_data) + "\n" + "Причина и дата снятия: " + str(prichina) + "\n")
                                except:
                                    pass
                            if archive_gos.count_documents({"nick": argg}) == 0:
                                argg = str(argg).split("id")[1].split("|")[0]
                                users = archive_gos.find({"id_vk": argg})
                            else:
                                users=archive_gos.find({"nick":argg}) 
                            for user in users:
                                nick = user["nick"]
                                vk = "https://vk.com/id"+str(user["id_vk"])
                                rank = user["rank"]+" "+user["frac"]
                                id_vk = user["id_vk"]
                                prichina = user["snyatie"]
                                add_data = user["add_data"]
                                chat_sender(id,'Ник: ' + '[id' + id_vk + '|' + nick + ']' + '\n' + 'ВК: ' + vk + '\n' + 'Должность: ' + rank + '\n' + "Дата постановления: " + str(add_data) + "\n" + "Причина и дата снятия: " + str(prichina) + "\n")
                            
                            
                        if str(msg).split()[0] == '/oldhfind' and id in sled_kf:
                            argg = str(event.object.message['text']).split()[1]
                            if archive.count_documents({"nick": argg}) == 0:
                                argg = str(argg).split("id")[1].split("|")[0]
                                users = archive.find({"id_vk": argg})
                            else:
                                users=archive.find({"nick":argg}) 
                            
                            for user in users:
                                try:
                                    nick = user["nick"]
                                    vk = user["vk"]
                                    rank = user["rank"]
                                    id_vk = user["id_vk"]
                                    prichina = user["snyatie"]
                                    add_data = user["add_data"]
                                    chat_sender(id,'Ник: ' + '[id' + id_vk + '|' + nick + ']' + '\n' + 'ВК: ' + vk + '\n' + 'Должность: ' + rank + '\n' + "Дата постановления: " + str(add_data) + "\n" + "Причина и дата снятия: " + str(prichina) + "\n")
                                except:
                                    pass
                            if archive_gos.count_documents({"nick": argg}) == 0:
                                argg = str(argg).split("id")[1].split("|")[0]
                                users = archive_gos.find({"id_vk": argg})
                            else:
                                users=archive_gos.find({"nick":argg}) 
                            for user in users:
                                nick = user["nick"]
                                vk = user["vk"]
                                rank = user["rank"]
                                l_ip = user["last-ip"]
                                id_vk = user["id_vk"]
                                prichina = user["snyatie"]
                                add_data = user["add_data"]
                                chat_sender(id,'Ник: ' + '[id' + id_vk + '|' + nick + ']' + '\n' + 'ВК: ' + vk + '\n' + 'Должность: ' + rank + '\n' + "Дата постановления: " + str(add_data) + "\n" + "Причина и дата снятия: " + str(prichina) + "\n" + 'L-ip: ' + str(l_ip))



                        if str(msg).split()[0]=='/editbalance' and id in sled_kf:
                            nick=norm_msg.split()[1].strip()
                            edit=norm_msg.split()[2].strip()
                            prichina=" ".join(norm_msg.split()[3:])
                            user=collection.find_one({"nick":nick})
                            collection.update_one({"nick":nick},{"$set":{"balance":user["balance"]+int(edit)}})
                            collection.update_one({"nick":nick},{"$set":{"balance_history":user["balance_history"]+f"\nИзменен баланс @id{id_authora}(администратором) на {edit} по причине: {prichina}"}})
                            chat_sender(id,f"✅Лидеру {nick} изменен баланс @id{id_authora}(администратором) на {edit}$ по причине: {prichina} ")
                            chat_sender(vigs_cf[user["frac_id"]],f"✅Лидеру {nick} изменен баланс @id{id_authora}(администратором) на {edit}$ по причине: {prichina} ")
                        
                        if str(msg).split()[0]=='/buy':
                            user=collection.find_one({"id_vk":id_authora})
                            if (user["rank"]=="Лидер" and user["frac_id"] in mafia_frac) or id in sled_kf:
                                get_price=price[norm_msg.split()[1]]
                                balance=user["balance"]
                                nick=user["nick"]
                                buy=0
                                get_usl=usluga[norm_msg.split()[1]]
                                if user["balance"]<-get_price:
                                    chat_sender(id,f"На вашем счету недосточно средств! Ваш баланс: {balance}$")
                                    buy=0
                                elif norm_msg.split()[1]=="1" or norm_msg.split()[1]=="2":
                                    chat_sender(id,"✅Покупка совершена успешно, сообщение отправлено следящей администрации.")
                                    chat_sender(12,f"Лидер {nick} купил {get_usl}, срочно выпустите @all")
                                    buy=1
                                elif norm_msg.split()[1]=="3" or norm_msg.split()[1]=="4":
                                    
                                    if norm_msg.split()[1]=="3":
                                        set_warn(nick,"-1",get_usl,id_authora,0)
                                        buy=1
                                    if norm_msg.split()[1]=="4":
                                        set_vig(nick,"-1",get_usl,id_authora,0)
                                        buy=1
                                elif norm_msg.split()[1]=="5":
                                    set_day(nick,"-3",get_usl,id_authora,0)
                                    buy=1

                                if buy==1:
                                    chat_sender(id,"✅Покупка совершена успешно")
                                    collection.update_one({"nick":nick},{"$set":{"balance":balance+get_price}})
                                    collection.update_one({"nick":nick},{"$set":{"balance_history":user["balance_history"]+"\n"+f"Изменен баланс на {get_price} за {get_usl}"}})
                                    




                        if str(msg).split()[0]=='/shop':
                            user=collection.find_one({"id_vk":id_authora})
                            if (user["rank"]=="Лидер" and user["frac_id"] in mafia_frac) or id in sled_kf:
                                nick=user["nick"]
                                balance=norm_money(user["balance"])
                                chat_sender(id,f"""Приветствую, {nick}\nВаш баланс: {balance}$\n\nВ нашем банке действуют следующие расценки:\n1) За 1.000.000$ - выпустить 9(ку) с ТСР.
2) За 1.500.000$ - выпустить 10(ку) с ТСР.
3) За 3.000.000$ - получить минус устный.
4) За 5.000.000$ - получить минус строгий.
5) 10.000.000$ - получить минус 3 дня к сроку.\nДля покупки введите /buy [номер товара]\n*номера товаров указаны выше\nС уважением ООО \"Бердов-банк\"""")

                        if str(msg).split()[0]=='/balance_history' and id in sled_kf:
                            nick=norm_msg.split()[1].strip()
                            user=collection.find_one({"nick":nick})
                            chat_sender(id,user["balance_history"])


                        if str(msg).split()[0]=='/voprrp' and id in obzvon_kf:
                            allvopr=''
                            i=0
                            voprosi=collection.find_one({"type":'voprosi'})["rpvopr"]
                            voprosi=voprosi.split('\n')
                            value=len(voprosi)
                            chat_sender(id,f'В базе данных найдено вопросов: {value}')
                            for i in range(len(voprosi)):
                                allvopr+=str(i+1)+'. '+voprosi[i]+'\n'
                            chat_sender(id,allvopr)

                        if str(msg).split()[0]=='/vopropen' and id in obzvon_kf:
                            allvopr=''
                            i=0
                            voprosi=collection.find_one({"type":'voprosi'})["openvopr"]
                            voprosi=voprosi.split('\n')
                            value=len(voprosi)
                            chat_sender(id,f'В базе данных найдено вопросов: {value}')
                            for i in range(len(voprosi)):
                                allvopr+=str(i+1)+'. '+voprosi[i]+'\n'
                            chat_sender(id,allvopr)

                        if str(msg).split()[0]=='/voprnrp' and id in obzvon_kf:
                            allvopr=''
                            i=0
                            voprosi=collection.find_one({"type":'voprosi'})["nrpvopr"]
                            voprosi=voprosi.split('\n')
                            value=len(voprosi)
                            chat_sender(id,f'В базе данных найдено вопросов: {value}')
                            for i in range(len(voprosi)):
                                allvopr+=str(i+1)+'. '+voprosi[i]+'\n'
                            chat_sender(id,allvopr)

                        if str(msg).split()[0] == '/delvopropen' and id in obzvon_kf:
                            i = 0
                            allvopr = ''
                            voprosC = int(str(msg).split()[1])
                            voprosi = collection.find_one({"type": 'voprosi'})["openvopr"].split('\n')
                            vopros = voprosi[voprosC - 1]
                            try:
                                voprosi.remove(vopros)
                                for i in range(len(voprosi)):
                                    if i != len(voprosi) - 1:
                                        allvopr += voprosi[i] + '\n'
                                    else:
                                        allvopr += voprosi[i]
                                collection.update_one({"type": 'voprosi'}, {"$set": {"openvopr": allvopr}})
                                chat_sender(id, 'Вопрос: ' + vopros + ' успешно удалён из БД вопросов рп банд.')
                            except:
                                chat_sender(id, 'Вопрос: ' + vopros + ' не найден в БД вопросов рп банд.')


                        if str(msg).split()[0] == '/delvoprrp' and id in obzvon_kf:
                            i = 0
                            allvopr = ''
                            voprosC = int(str(msg).split()[1])
                            voprosi = collection.find_one({"type": 'voprosi'})["rpvopr"].split('\n')
                            vopros = voprosi[voprosC - 1]
                            try:
                                voprosi.remove(vopros)
                                for i in range(len(voprosi)):
                                    if i != len(voprosi) - 1:
                                        allvopr += voprosi[i] + '\n'
                                    else:
                                        allvopr += voprosi[i]
                                collection.update_one({"type": 'voprosi'}, {"$set": {"rpvopr": allvopr}})
                                chat_sender(id, 'Вопрос: ' + vopros + ' успешно удалён из БД вопросов рп банд.')
                            except:
                                chat_sender(id, 'Вопрос: ' + vopros + ' не найден в БД вопросов рп банд.')

                                   

                        if str(msg).split()[0]=='/voprmafii' and id in obzvon_kf:
                            allvopr=''
                            i=0
                            voprosi=collection.find_one({"type":'voprosi'})["mafiivopr"]
                            voprosi=voprosi.split('\n')
                            value=len(voprosi)
                            chat_sender(id,f'В базе данных найдено вопросов: {value}')
                            for i in range(len(voprosi)):
                                allvopr+=str(i+1)+'. '+voprosi[i]+'\n'
                            chat_sender(id,allvopr)                 

                        if str(msg).split()[0]=='/addvoprnrp' and id in obzvon_kf:
                            vopros=str(event.object.message['text']).split()[1:]
                            vopros=' '.join(vopros)
                            AddVoprNRP(vopros)
                        if str(msg).split()[0]=='/addvoprrp' and id in obzvon_kf:
                            vopros=str(event.object.message['text']).split()[1:]
                            vopros=' '.join(vopros)
                            AddVoprRP(vopros)

                        if str(msg).split()[0]=='/addvopropen' and id in obzvon_kf:
                            vopros=str(event.object.message['text']).split()[1:]
                            vopros=' '.join(vopros)
                            AddVoprOpen(vopros)


                        if str(msg).split()[0]=='/addvoprmafii' and id in obzvon_kf:
                            vopros=str(event.object.message['text']).split()[1:]
                            vopros=' '.join(vopros)
                            AddVoprMaf(vopros)





                        
                        
                       


                        if str(msg).split()[0]=='/delvoprnrp' and id in obzvon_kf:
                            i=0
                            allvopr=''
                            voprosC=int(str(msg).split()[1])
                            voprosi=collection.find_one({"type":'voprosi'})["nrpvopr"].split('\n')
                            vopros=voprosi[voprosC-1]
                            try:
                                voprosi.remove(vopros)
                                for i in range(len(voprosi)):
                                    if i!=len(voprosi)-1:
                                        allvopr+=voprosi[i]+'\n'
                                    else:
                                        allvopr+=voprosi[i] 
                                collection.update_one({"type":'voprosi'},{"$set":{"nrpvopr" : allvopr}})
                                chat_sender(id,'Вопрос: '+vopros+' успешно удалён из БД вопросов рп банд.')
                            except:
                                chat_sender(id,'Вопрос: '+vopros+' не найден в БД вопросов рп банд.')

                        if str(msg).split()[0]=='/delvoprmafii' and id in obzvon_kf:
                            i=0
                            allvopr=''
                            voprosC=int(str(msg).split()[1])
                            voprosi=collection.find_one({"type":'voprosi'})["mafiivopr"].split('\n')
                            vopros=voprosi[voprosC-1]
                            try:
                                voprosi.remove(vopros)
                                for i in range(len(voprosi)):
                                    if i!=len(voprosi)-1:
                                        allvopr+=voprosi[i]+'\n'
                                    else:
                                        allvopr+=voprosi[i] 
                                collection.update_one({"type":'voprosi'},{"$set":{"mafiivopr" : allvopr}})
                                chat_sender(id,'Вопрос: '+vopros+' успешно удалён из БД вопросов рп банд.')
                            except:
                                chat_sender(id,'Вопрос: '+vopros+' не найден в БД вопросов рп банд.')

                        

                        if str(msg).split()[0]=='/tagfrac' and id in sled_kf:
                            chat_sender(id,"""
🔍Grove »»» 11
🔍Vagos »»» 12
🔍Ballas »»» 13
🔍Aztecas »»» 14
🔍Rifa »»» 15
🔍Russian Mafia »»» 16
🔍Yakuza »»» 17
🔍La Cosa Nostra »»» 18
🔍Warlock MC »»» 19
🔍Night Wolfs »»» 25
""")
                        if str(msg).split()[0]=='/l_add' and id in sled_kf:
                            chat_sender(id,"""
▶ Тег вк:
▶ Игровой ник:
▶ Возраст:
▶ Фракция:
▶ Статус(Лидер/Заместитель):
▶ Тип назначения(Обзвон/Передача/АБ):



📋 Пример заполнения этой формы находиться ниже:

▶ Тег вк: @berdofff
▶ Игровой ник: Rafael_Camilleri
▶ Возраст: 18
▶ Фракция: 3
▶ Статус(Лидер/Заместитель): Лидер
▶ Тип назначения(Обзвон/Передача/АБ): Обзвон




""")
                        if "▶ игровой ник:" in str(msg) and (id in sled_kf) :
                            id_vk=get_id_by_tag(norm_msg.split("▶ Тег вк:")[1].split("▶")[0]).strip()
                            print(id_vk)
                            nick=norm_msg.split("▶ Игровой ник:")[1].split("▶ Возраст:")[0].strip()
                            vozrast=norm_msg.split("▶ Возраст:")[1].split("▶ Фракция:")[0].strip()
                            frac=norm_msg.split("▶ Фракция:")[1].split("▶")[0].strip()
                            role=norm_msg.split("Статус(Лидер/Заместитель):")[1].split("▶")[0].strip()
                            type_add=norm_msg.split("Тип назначения(Обзвон/Передача/АБ):")[1].split("▶")[0].strip()
                            frac_id=int(frac)
                            frac=name_fracs1[frac]
                            today_date=datetime.datetime.today()
                            date_today=str(today_date.day)+'.'+str(today_date.month)+'.'+str(today_date.year)
                            srok_data=today_date+datetime.timedelta(days=30)
                            srok_data=str(srok_data.day)+'.'+str(srok_data.month)+'.'+str(srok_data.year)
                            if role=="Лидер":
                                dostup="1"
                                add_type=type_add.lower()
                                a=f"Ник нового лидера: {nick}<br>Какая фракция: {frac}<br>Возраст: {vozrast}<br>Каким образом поставлен (обзвон / передача): {add_type}<br>Дата обзвона/передачи: {date_today}<br>VK: https://vk.com/id{id_vk}"
                                str_send(328,a)
                            elif role=="Заместитель":
                                dostup="0"
                            else:
                                chat_sender(id,"Косяк в форме")
                            print(1)
                            if collection.count_documents({"id_vk":id_vk})==0:
                                collection.insert_one({"nick":nick,"vozrast":vozrast,"frac":frac,"dostup":dostup,"rank":role,"type_add":type_add,"id_vk":id_vk,"frac_id":frac_id,"vigs":0,"preds":0,"warn_history":"","add_data":date_today,"srok_data":srok_data,"days_history":"","main_balls":0,"main_balls_history":"","balance":0,"balance_history":""})
                                chat_sender(id,f"@id{id_vk}({nick})<br>📝Возраст: {vozrast}<br>📝Должность: {role}<br>📝Фракция:{frac}")
                                add_kf(id_vk,frac_id,role,frac,nick)
                                if role.lower()=="лидер":
                                    if frac_id in ghetto_frac:
                                        chat_sender(7,f"На пост лидера {frac} назначен @id{id_vk}({nick})")
                                        chat_sender(4,f"На пост лидера {frac} назначен @id{id_vk}({nick})")
                                    if frac_id in mafia_frac:
                                        chat_sender(8,f"На пост лидера {frac} назначен @id{id_vk}({nick})")
                                        chat_sender(5,f"На пост лидера {frac} назначен @id{id_vk}({nick})")
                                    lid=collection.find_one({"nick":nick})
                                    proverka(lid,0)
                            else:
                                chat_sender(id,"Уже добавлен")
                        if str(msg).split()[0]=='/gleaders':
                            users=collection.find({"dostup":"1"}).sort("frac_id")
                            for user in users:
                                print(user["nick"])
                                if user["frac_id"] in ghetto_frac:
                                    nick=user["nick"]
                                    role=user["rank"]
                                    frac=user["frac"]
                                    id_vk=user["id_vk"]
                                    add_data=user["add_data"]
                                    srok_data=user["srok_data"]
                                    delta_days=datetime.datetime.strptime(srok_data,"%d.%m.%Y")-datetime.datetime.today()
                                    delta_days=str(delta_days).split()[0]
                                    chat_sender(id,f"@id{id_vk}(📝 {nick})<br>📝 Должность: {role}<br>📝 Фракция: {frac}<br>📝 Выговоры: "+str(user["vigs"])+"/5<br>"+"📝 Предупреждения: "+str(user["preds"])+"/3<br>"+f"📝 Встал: {add_data}<br>📝 Срок: {srok_data}<br>📝 Дней до срока: {delta_days}")
                        if str(msg).split()[0]=='/mleaders':
                            users=collection.find({"dostup":"1"}).sort("frac_id")
                            for user in users:
                                print (user["nick"])
                                if user["frac_id"] in mafia_frac:
                                    nick=user["nick"]
                                    role=user["rank"]
                                    frac=user["frac"]
                                    id_vk=user["id_vk"]
                                    add_data=user["add_data"]
                                    srok_data=user["srok_data"]
                                    delta_days=datetime.datetime.strptime(srok_data,"%d.%m.%Y")-datetime.datetime.today()
                                    delta_days=str(delta_days).split()[0].split(".")[0]
                                    litrscore=user["main_balls"] 
                                    balance=norm_money(user["balance"])
                                    chat_sender(id,f"@id{id_vk}(📝 {nick})<br>📝 Должность: {role}<br>📝 Фракция: {frac}<br>📝 Выговоры: "+str(user["vigs"])+"/5<br>"+"📝 Предупреждения: "+str(user["preds"])+"/3<br>"+f"📝 Баллы: {litrscore}<br>"+f"📝 Встал: {add_data}<br>📝 Срок: {srok_data}<br>📝 Дней до срока: {delta_days}<br>📝 Накопительный счёт: {balance}$")
                                    
                        if str(msg).split()[0]=='/info':
                            try:
                                argg=str(event.object.message['text']).split()[1]
                                try:
                                    if collection.count_documents({"nick":argg})==0:
                                        argg=str(argg).split("id")[1].split("|")[0]
                                        user=collection.find_one({"id_vk": argg})
                                    else:
                                        user=collection.find_one({"nick": argg})
                                    nick=user["nick"]
                                    role=user["rank"]
                                    frac=user["frac"]
                                    id_vk=user["id_vk"]
                                    add_data=user["add_data"]
                                    print(add_data)
                                    if role=="Заместитель":
                                        chat_sender(id,f"@id{id_vk}(📝 {nick})<br>📝 Должность: {role}<br>📝 Фракция: {frac}<br>📝 Встал: "+str(add_data))
                                    
                                    else:
                                        print(1)
                                        c=""
                                        srok_data=user["srok_data"]
                                        delta_days=datetime.datetime.strptime(srok_data,"%d.%m.%Y")-datetime.datetime.today()
                                        print(delta_days)
                                        delta_days=str(delta_days).split()[0]
                                        litrscore=user["main_balls"]
                                        if user["frac_id"] in mafia_frac:
                                            c="📝 Накопительный счёт: "+str(user["balance"])+"$"
                                        chat_sender(id,f"@id{id_vk}(📝 {nick})<br>📝 Должность: {role}<br>📝 Фракция: {frac}<br>📝 Выговоры: "+str(user["vigs"])+"/5<br>"+"📝 Предупреждения: "+str(user["preds"])+"/3<br>"+f"📝 Баллы: {litrscore}<br>"+f"📝 Встал: {add_data}<br>📝 Срок: {srok_data}<br>📝 Дней до срока: {delta_days}\n"+c)
                                    
                                except:
                                    chat_sender(id,'Данный человек не является лидером или замом')
                            except:
                                chat_sender(id,'❗Используйте /info (@tag или Ni_Ck)')

                        

                            
                except:
                    pass
except:
    time.sleep(1)
    print('Timeout')
    os.execl(sys.executable, sys.executable, *sys.argv)
