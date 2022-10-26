from rubika import Bot
from json import load , dump
import time

bot = Bot("jehwjdsugensznqdxmtedwfqyrgltdls")
target = "g0BfWEp02b9cefd9901ab61cc9014b27"


def hasAds(msg):
	links = ["rubika.ir/"] # you can develop it
	for i in links:
		if i in msg.lower():
			return True


def searchUserInGroup(guid):
	user = bot.getUserInfo(guid)["data"]["user"]["username"]
	members = bot.getGroupAllMembers(user,target)["in_chat_members"]
	if members != [] and members[0]["username"] == user:
		return True
	
	

# static variable
answered, sleeped, retries = [], False, {}

# option lists
blacklist, exemption, auto_lock , no_alerts , no_stars =  [] , [] , False , [] , []
alerts, stars = {} , {}
auto_lock , locked , gif_lock = False , False , False


# alert function
def alert(guid,user,alert_text=""):
	no_alerts.append(guid)
	alert_count = int(no_alerts.count(guid))

	alerts[user] = alert_count

	max_alert = 3    # you can change it


	if alert_count == max_alert:
		blacklist.append(guid)
		bot.sendMessage(target, "\n 🚫 User [ @"+user+" ] \n ("+ str(max_alert) +") He received a warning, so he is being fired now.", msg["message_id"])
		bot.banGroupMember(target, guid)
		return

	for i in range(max_alert):
		no = i+1
		if alert_count == no:
			bot.sendMessage(target, "🔹 Warning [ @"+user+" ] \n\n"+ str(alert_text) +" You ("+ str(no) +"/"+ str(max_alert) +") You have received a warning.\n\nAfter receiving "+ str(max_alert) +" Warning, you will be expelled from the group.", msg["message_id"])
			return

# star function
def star(guid,user):
	no_stars.append(guid)
	star_count = int(no_stars.count(guid))
	stars[user] = star_count

	bot.sendMessage(target, "⭐ User @"+ user +" Received points.\n\n Number of user points so far = "+ str(star_count), msg["message_id"])
	return


while True:
	if auto_lock:
		if not locked and time.localtime().tm_hour == 00:
			bot.setMembersAccess(target, ["AddMember"])
			bot.sendMessage(target, "(⏰) It's time to auto-lock the group.\n - The group is closed until [08:00].")
			locked , sleeped = True , True

		if locked and time.localtime().tm_hour == 8:
			bot.setMembersAccess(target, ["SendMessages","AddMember"])
			bot.sendMessage(target, "(⏰) The group auto-lock time has expired.\n - Members can now chat in groups.")
			locked , sleeped = False , False		


	# time.sleep(15)
	try:

		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		with open("learn.json","r",encoding="utf-8") as learn:
			data = load(learn)

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				# Check Bot is Sleeped or Not
				if not sleeped:

					# Get Text Messages
					if msg["type"]=="Text" and not msg["message_id"] in answered:


						# Admin Commands
						if msg["author_object_guid"] in admins:

							if msg["text"] == "ربات خاموش" or msg["text"] == "/sleep" :
								sleeped = True
								bot.sendMessage(target, "💤 The robot is now off.", msg["message_id"])


							elif msg["text"] == "bot" or msg["text"] == "Bot" :
								bot.sendMessage(target, "The panel was reviewed\n Error not received\n The robot is on (✅)", msg["message_id"])
							
							elif msg["text"].startswith("یادبگیر") or msg["text"].startswith("/learn"):
								try:
									text = msg["text"].replace("یادبگیر ","").replace("/learn ","").split(":")
									word = text[0]
									answer = text[1]

									data[word] = answer
									with open("learn.json","w",encoding="utf-8") as learn:
										dump(data, learn)

									bot.sendMessage(target, "(✅) was saved", msg["message_id"])
								except:
									bot.sendMessage(target, "❌Error executing command", msg["message_id"])


							elif msg["text"].startswith("افزودن ادمین") or msg["text"].startswith("/add_admin") :

								try:
									user = msg["text"].replace("افزودن ادمین ","").replace("/add_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										bot.setGroupAdmin(target, guid)
										bot.sendMessage(target, "(✅) User @"+ str(user) +" Successfully became an admin.", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ User is now an admin", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										
										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "(✅) User @"+ str(user) +" Successfully became an admin.", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ User is now an admin", msg["message_id"])
									except:
										bot.sendMessage(target, "❌Error executing command", msg["message_id"])

							elif msg["text"].startswith("حذف ادمین") or msg["text"].startswith("/del_admin") :
								try:
									user = msg["text"].replace("حذف ادمین ","").replace("/del_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]

									if guid in admins :
										bot.deleteGroupAdmin(target, guid)
										bot.sendMessage(target, "(✅) User @"+ str(user) +" Successfully removed from admin.", msg["message_id"])
									else:
										bot.sendMessage(target, "(❌) The user is not a group admin", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "(✅) User @"+ str(user) +" Successfully removed from admin.", msg["message_id"])
										else:
											bot.sendMessage(target, "(❌) The user is not a group admin", msg["message_id"])
									except:
										bot.sendMessage(target, "❌Error executing command", msg["message_id"])
							

							
							elif msg["text"].startswith("معاف") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("معاف ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if not guid in exemption:
											exemption.append(guid)
											bot.sendMessage(target, "(✅) The user was successfully exempted.", msg["message_id"])
										else:
											bot.sendMessage(target, "(❌) The user is currently exempt.", msg["message_id"])
								
									else :
										bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins:
											if not guid in exemption:
												exemption.append(guid)
												bot.sendMessage(target, "(✅) The user was successfully exempted.", msg["message_id"])
											else:
												bot.sendMessage(target, "(❌) The user is currently exempt.", msg["message_id"])

										else :
											bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])


							elif msg["text"].startswith("حذف معاف") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("حذف معاف ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if guid in exemption:
											exemption.remove(guid)
											bot.sendMessage(target, "(✅) The user was removed from the exemption", msg["message_id"])
										else:
											bot.sendMessage(target, "(❌) The user is not exempt.", msg["message_id"])
									else :
										bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins and guid in exemption:
											if guid in exemption:
												exemption.remove(guid)
												bot.sendMessage(target, "(✅) The user was removed from the exemption", msg["message_id"])
											else:
												bot.sendMessage(target, "(❌) The user is not exempt.", msg["message_id"])

										else :
											bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
									
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
							

							
							elif msg["text"] == "لیست امتیاز" or msg["text"] == "/star_list":
								try:
									text = "💎 Group users rating list :\n\n"
									stars_list = ""
									for i in stars:
										stars_list += (" - @"+i+" \t= "+str(stars[i])+"\n")
									bot.sendMessage(target, text + str(stars_list), msg["message_id"])
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
							
							
							elif msg["text"] == "لیست اخطار" or msg["text"] == "/alert_list":
								try:
									text = "⚠️ Group user alerts list :\n\n"
									alert_list = ""
									for i in alerts:
										alert_list += (" - @"+i+" \t= "+str(alerts[i])+"\n")
									bot.sendMessage(target, text + str(alert_list), msg["message_id"])
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							
							elif msg["text"].startswith("حذف اخطار") or msg["text"].startswith("/del_alert"):
								try:
									user = msg["text"].replace("حذف اخطار ","").replace("/del_alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if guid in no_alerts:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										alerts[user] = 0
										bot.sendMessage(target, "(✅) User warnings deleted.", msg["message_id"])
									else:
										bot.sendMessage(target, "(❌) The user has no warning.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if guid in no_alerts:
											for i in range(no_alerts.count(guid)):
												no_alerts.remove(guid)
											alerts[user] = 0
											bot.sendMessage(target, "(✅) User warnings deleted.", msg["message_id"])
										else:
											bot.sendMessage(target, "(❌) The user has no warning.", msg["message_id"])

									except:
										bot.sendMessage(target, "(❌) Please enter the command correctly", msg["message_id"])
								


							elif msg["text"].startswith("اخطار")  or msg["text"].startswith("/alert"):
								try:
									user = msg["text"].replace("اخطار ","").replace("/alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										alert(guid,user)
									else :
										bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										if not guid in admins:
											alert(guid,user)
										else:
											bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
							
							
							
							elif msg["text"].startswith("حالت آرام") or msg["text"].startswith("/slow"):
								try:
									number = int(msg["text"].replace("حالت آرام ","").replace("/slow ",""))

									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "(⏰) Calm mode for "+str(number)+"Activated seconds", msg["message_id"])

								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
								
							elif msg["text"] == "حذف حالت آرام" or msg["text"] == "/off_slow":
								try:
									number = 0
									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "(⏰) Silent mode is disabled", msg["message_id"])
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
								
							# elif msg["text"] == "قفل گیف" or msg["text"] == "/gif_lock":
							# 	gif_lock = True
							# 	bot.sendMessage(target, "(✅) Gif lock and sticker activated.", msg["message_id"])

							
							# elif msg["text"] == "حذف قفل گیف" or msg["text"] == "/del_gif_lock":
							# 	gif_lock = False
							# 	bot.sendMessage(target, "(✅) Gif lock and sticker activated.", msg["message_id"])


							elif msg["text"] == "قفل خودکار" or msg["text"] == "/auto_lock":
								try:
									auto_lock = True
									# time = msg["text"].split(" ")[2].split(":") start=time[0] , end=time[1]
									start = "00:00"
									end = "08:00"
									# open("time.txt","w").write(start +"-"+ end)
									bot.sendMessage(target, "(🔒) Automatic lock was activated for the group.\n\n Clock group [ "+ start +" ] Will be locked \n And on the clock [ "+ end +" ] And on the clock", msg["message_id"])
										
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							
							elif msg["text"] == "حذف قفل خودکار" or msg["text"] == "/del_auto_lock":
								auto_lock = False
								bot.sendMessage(target, "(🔓) Automatic lock removed.", msg["message_id"])


							elif msg["text"].startswith("اخراج") or msg["text"].startswith("/ban") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("اخراج ","").replace("/ban ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										bot.banGroupMember(target, guid)
										# bot.sendMessage(target, "(✅) The user was successfully expelled from the group", msg["message_id"])
									else :
										bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins :
											bot.banGroupMember(target, guid)
											# bot.sendMessage(target, "(✅) The user was successfully expelled from the group", msg["message_id"])
										else :
											bot.sendMessage(target, "(❌) The user is an admin.", msg["message_id"])
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							
							elif msg["text"].startswith("حذف") or msg["text"].startswith("/del"):
								try:
									number = int(msg["text"].replace("حذف ","").replace("/del ",""))
									if number > 50:
										bot.sendMessage(target, "(❌) The bot deletes only up to 50 recent messages.", msg["message_id"])
									else:
										answered.reverse()
										bot.deleteMessages(target, answered[0:number])

										bot.sendMessage(target, "(✅)"+ str(number) +" Recent message successfully deleted", msg["message_id"])
										answered.reverse()

								except:
									try:
										bot.deleteMessages(target, [msg["reply_to_message_id"]])
										bot.sendMessage(target, "(✅) The message was successfully deleted", msg["message_id"])
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							
							elif msg["text"].startswith("آپدیت قوانین") or msg["text"].startswith("/update_rules"):
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg["text"].replace("آپدیت قوانین","").replace("/update_rules","")))
								bot.sendMessage(target, "(✅) Rules updated", msg["message_id"])
								# rules.close()
								

							
							elif msg["text"].startswith("امتیاز") or msg["text"].startswith("/star"):
								try:
									user = msg["text"].replace("امتیاز ","").replace("/star ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									star(guid,user)
									
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										star(guid,user)
									except:
										bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							
							
							elif msg["text"] == "قفل گروه" or msg["text"] == "/lock":
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "(🔒) The group was locked", msg["message_id"])


							elif msg["text"] == "بازکردن گروه" or msg["text"] == "/unlock" :
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "(🔓) The group is now open", msg["message_id"])
							

							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.invite(target, [guid])
									
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])
							
							elif msg["text"] == "/jrat":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()
							
							elif msg["text"] == "بازی":
								commands = open("commands.txt","r",encoding='utf-8').read()
								bot.sendMessage(target,str(commands),msg["message_id"])             
								
					
						# User Commands
						else:
                            
							if hasAds(msg["text"]) and not msg["author_object_guid"] in exemption:
								guid = msg["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								bot.deleteMessages(target, [msg["message_id"]])
								alert(guid,user,"It is forbidden to put a link in the group.\n\n")
							
							elif msg["text"] == "بازی":
								commands = open("commands.txt","r",encoding='utf-8').read()
								bot.sendMessage(target,str(commands),msg["message_id"])
							
							elif msg["text"] == "/jrat":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()
							
							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										bot.sendMessage(target, "(❌) The user is blacklisted and only the admin can add the person to the group.", msg["message_id"])
									else:
										bot.invite(target, [guid])
										# bot.sendMessage(target, "✅ User is now a member of the group", msg["message_id"])
									
								except:
									bot.sendMessage(target, "(❌) Error executing command", msg["message_id"])

							elif msg["text"] == "لینک":
								group = bot.getGroupLink(target)["data"]["join_link"]
								bot.sendMessage(target, "(🔗) Group link :\n"+str(group), msg["message_id"])
                            
							for i in data.keys():
								if i == msg["text"]:
									bot.sendMessage(target, str(data[i]), msg["message_id"])


					elif msg["type"]=="Event" and not msg["message_id"] in answered:
						answered.append(msg["message_id"])

						name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
						data = msg['event_data']
						if data["type"]=="RemoveGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"🚨 User {user} Successfully removed from the group.", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="AddedGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hello {user} dear (🌹) \n• Welcome to the {name} group (😍)\n Please follow the rules (💎).\n Send the word (rules) to see enough rules.", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="LeaveGroup":
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Goodbye", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							
						elif data["type"]=="JoinedGroupByLink":
							guid = data['performer_object']['object_guid']
							user = bot.getUserInfo(guid)["data"]["user"]["first_name"]
							bot.sendMessage(target, f"Hello {user} dear (🌹) \n• Welcome to the {name} group (😍)\n Please follow the rules (💎).\n Send the word (rules) to see enough rules.", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							if guid in blacklist:
								for i in range(no_alerts.count(guid)):
									no_alerts.remove(guid)
								blacklist.remove(guid)
					
					# elif msg["type"]=="Gif" or msg["type"]=="Sticker" and not msg["message_id"] in answered:
					# 	if gif_lock and not msg["author_object_guid"] in admins:
					# 		guid = msg["author_object_guid"]
					# 		user = bot.getUserInfo(guid)["data"]["user"]["username"]
					# 		bot.deleteMessages(target, [msg["message_id"]])
					# 		alert(guid,user,"ارسال گیف و استیکر در گروه ممنوع میباشد .")

					elif msg["text"] == "تست یک" or msg["text"] == "تست یک" :
								bot.sendMessage(target, "(✅)", msg["message_id"])

					else:
						if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg["message_id"]])[0]["forwarded_from"]["type_from"] == "Channel" and not msg["author_object_guid"] in exemption:
							bot.deleteMessages(target, [msg["message_id"]])
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg["message_id"]])
							alert(guid,user,"Forwarding messages in the group is prohibited.\n\n")
						
						answered.append(msg["message_id"])
						continue
				
				else:
					if msg["text"] == "ربات روشن" or msg["text"] == "/wakeup":
						sleeped = False
						bot.sendMessage(target, "(✅) The robot is now on.", msg["message_id"])
					
			except:
				continue

			answered.append(msg["message_id"])
			print("[" + msg["message_id"]+ "] >>> " + msg["text"] + "\n")

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


		
