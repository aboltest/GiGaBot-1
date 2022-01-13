from re import findall
from rubika import Bot
import time

bot = Bot("YOUR-AUTH")
target = "GUID"

# Coded By : github.com/HiByeDev ~ rubika -> @Develover
# Tnx to github.com/Bahman-ahmadi

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
	

# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گزاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "ربات خاموش" and msg.get("author_object_guid") in admins :
							sleeped = True
							bot.sendMessage(target, "✅ ربات اکنون خاموش است", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("اخراج") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدود میباشد", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))

						
						elif msg.get("text") == "دستورات":
							bot.sendMessage(target, "⚠ دستورات ربات ⚠ \n\n ♟ برای کاربران عادی  : 🔻  \n\n ➖ دستورات = نمایش لیست دستورات \n\n ➖ قوانین = نمایش قوانین گروه\n\n ➖ افزودن @username =  افزودن کاربر به گروه با (آیدی) \n\n\n  👑 برای ادمین های گروه : 🔻  \n\n ➖ ربات خاموش = خاموش کردن ربات \n\n ➖ ربات روشن = روشن کردن ربات \n\n ➖ حذف = حذف کردن پیام با (ریپلای) \n\n ➖ حذف 10 = حذف پیام ها براساس (تعداد) مشخص شده \n\n ➖ اخراج = اخراج کاربر از گروه با (آیدی) یا (ریپلای) \n\n ➖ حالت آرام = قراردادن حالت آرام برای ارسال پیام ها (10 ثانیه) \n\n ➖ برداشتن حالت آرام = برداشتن حالت آرام برای ارسال پیام ها \n\n ➖ آپدیت قوانین = بروزرسانی قوانین گروه با نوشتن متن قوانین بعداز کلمه (آپدیت قوانین) \n\n ➖ اخطار = اخطار دادن به کاربر با (آیدی) یا (ریپلای) \n\n ➖ قفل گروه = قفل گروه برای ارسال پیام \n\n ➖ بازکردن گروه = بازکردن گروه برای ارسال پیام \n\n\n 💎 سازنده ربات : github.com/HiByeDev", message_id=msg.get("message_id"))
						
						elif msg.get("text") == "قوانین":
							rules = open("rules.txt","r",encoding='utf-8').read()
							bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "✅  قوانین بروزرسانی شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("حالت آرام") and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
						elif msg.get("text").startswith("برداشتن حالت آرام") and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							bot.setMembersAccess(target, ["AddMember"])
							bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))

						elif msg.get("text") == "بازکردن گروه" and msg.get("author_object_guid") in admins :
							bot.setMembersAccess(target, ["SendMessages","AddMember"])
							bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))

					else:
						if msg.get("text") == "ربات روشن" and msg.get("author_object_guid") in admins :
							sleeped = False
							bot.sendMessage(target, "✅ ربات اکنون روشن است", message_id=msg.get("message_id"))

				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"🚨 کاربر {user} با موفقیت از گروه حذف شد .", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
					
					elif data["type"]=="AddedGroupMembers":
						user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n • به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
					
					elif data["type"]=="LeaveGroup":
						user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"خدانگهدار {user} 👋 ", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
						
					elif data["type"]=="JoinedGroupByLink":
						user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
						bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n• به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", message_id=msg["message_id"])
						# bot.deleteMessages(target, [msg["message_id"]])
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue