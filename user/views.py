from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
import email.message,smtplib,hashlib,random
from datetime import datetime
from django.contrib.sessions.models import Session
import uuid
from body.models import Blood_pressure,Weight,Blood_sugar,Diary_diet,UserCare
from friend.models import Friend,Friend_data
import os
import urllib
# Create your views here.
@csrf_exempt #修飾器,一定要加不然會出問題的樣子
def register(request):#def後面就接跟功能相關的單字之類
	if request.method == "POST":#防呆 這邊用到POST,API文件上面有
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		#try:
		if 1:
			account = data["account"]#這邊格式是json格式,postman在用的時候要用raw來測試
			email = data["email"]
			password = data["password"]
			#email = data["email"]
			time = datetime.now()
			timeprint = datetime.strftime(time,"%Y-%m-%d %H:%M:%s")
			uid = uuid.uuid3(uuid.NAMESPACE_DNS,account)
			invite_code = ''.join(random.sample("0123456789",6))#隨機生成0~9的6位隨機整數
			if 1:
				user=UserProfile.objects.create_user(uid=uid,account=email,email=email,invite_code=invite_code,created_at=timeprint,updated_at=timeprint)
				user.set_password(password)
				user.save()
				Medical_Information.objects.create(uid=uid)
				UserSet.objects.create(uid=uid,must_change_password=0,name=email)#後來新增change還沒測
				druginformation.objects.create(uid=uid)
				Blood_pressure.objects.create(uid=uid)
				Diary_diet.objects.create(uid=uid)#這邊body裡面在創建的時候有些不會創建uid,因為有其他選項是必填項目
				Weight.objects.create(uid=uid)
				Blood_sugar.objects.create(uid=uid)
				Friend.objects.create(uid=uid,invite_code=invite_code)
				Friend_data.objects.create(uid=uid)
				UserCare.objects.create(uid=uid)
				Share.objects.create(uid=uid)
				badge.objects.create(uid=uid)
				Notification.objects.create(uid=uid)
			message={
				"status":"0"
			}
		#except:
		#	message={
		#		"status":"1"
		#	}
		return JsonResponse(message)
@csrf_exempt
def login(request): # 登入 #測試成功    
	if request.method == "POST":
		account=request.POST.get('account')#這兩行讀使用者輸入的帳號和密碼
		password=request.POST.get('password')
		# try:
		if 1:
			print("123123")
			# user = UserProfile.objects.get(account=account)
			auth_obj = auth.authenticate(request,account=account,password=password)
			if auth_obj:
				request.session.create()
				auth.login(request, auth_obj)
			message = {"status": "0",
			"token":request.session.session_key
			}
			print(message)
			return JsonResponse(message)	
		# except:
		# 	return JsonResponse({'status':'1'})	

@csrf_exempt
def logout(request): # 登出
	if request.method == "POST":
		auth.logout(request)
		return HttpResponseRedirect('api/login')

@csrf_exempt
def send(request):  # 傳送驗證信 #測試成功
	if request.method == "POST":
		emaildata=request.POST.get('email')
		msg=email.message.EmailMessage()
		code = ''.join(random.sample("0123456789",6)) #隨機生成0~9的6位隨機整數
		content = "歡迎使用普元血糖app:\n請點選下列連結完成註冊:\n127.0.0.1:8000/api/check\n驗證碼:{}".format(code)#此行到下面server.close都是寄信的標準格式
		msg = email.message.EmailMessage()
		msg["From"] = "c0981985611@gmail.com"
		msg["To"] = request.POST.get('email')
		msg["Subject"] = "普元認證"
		print(msg["To"])
		msg.set_content(content)
		print("ssssssssssssssss")
		# return JsonResponse({'status':'0'})	
		server = smtplib.SMTP_SSL("smtp.gmail.com",465)
		# return JsonResponse({'status':'1'})	
		server.login("c0981985611@gmail.com","0981985173")#這邊是以這組帳號密碼登入發送訊息，一開始要去google帳戶裡面設定>安全性>低安全性應用程式存權設定打開
		server.send_message(msg)
		server.close()
		return JsonResponse({'status':'0'})	


@csrf_exempt
def check(request):  #測試成功
	if request.method == "POST":
		try:
			code=request.POST.get('code')#使用者輸入的認證碼為code
			phonedata=request.POST.get('phone')
			profile = UserProfile.objects.get(phone=phonedata)#profile來接收 phonedata那一整列
			if profile.code==code:
				return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def ForgetPwd(request): #測試成功
	if request.method == "POST":
		try:
			newpassword = ''.join(random.sample("0123456789",8)) #newpassword #隨機生成0~9的8位隨機整數
			content = "這是您的新密碼:{}".format(newpassword)
			emaildata=request.POST.get('email')#emaildata接收使用者輸入的email
			profile = UserProfile.objects.get(email=emaildata)#找到使用者輸入的EAMIL對應到資料庫那一列
			profile.set_password = newpassword#將隨機產生8位數密碼更新到那一列的密碼
			profile.save()
			msg = email.message.EmailMessage()
			msg["From"] = "nihandsomeni@gmail.com"
			msg["To"] = request.POST.get('email')
			msg["Subject"] = "普元認證"
			print(msg["To"])
			msg.set_content(content)
			server = smtplib.SMTP_SSL("smtp.gmail.com",465)
			server.login("nihandsomeni@gmail.com","ni123456ni")
			server.send_message(msg)
			server.close()
			return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def ResetPwd(request):  #測試成功
	if request.method == "POST":
		try:
			passworddata = request.POST.get('password')#使用者輸入忘記密碼產生的新密碼8位數
			newpassword = request.POST.get('newpassword')#設定新密碼
			profile = UserProfile.objects.get(password=passworddata)#找到使用者新密碼的那一列
			profile.set_password = newpassword#使用者自己訂的密碼更新到那一列的密碼
			profile.save()
			return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def recheck(request): #註冊確認uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
	if request.method == 'GET':
		user_ck = request.GET["account"]
		try:
			user = UserProfile.objects.get(username=user_ck)
			message = {'status':'1'}
		except:
			message = {'status':'0'}
		return JsonResponse(message)

def privacy_policy(request): # 隱私權聲明 FBLogin
	result = '1'
	try:
		if request.method == 'POST':
			result = '0'
	except:
		pass
	return JsonResponse({'status': result})


# @csrf_exempt
# def user_set(request):  
# 	# data=request.body #這2行是把接收到的格式轉成json格式
# 	# data=str(data,encoding="UTF-8")
# 	if request.method == "PATCH":
# 		try:
# 			name=request.POST('name')
			# birthday=request.POST.get('birthday')
			# height=request.POST.get('height')
			# gender=request.POST.get('gender')
			# address=request.POST.get('address')
			# weight=request.POST.get('weight')
			# phone=request.POST.get('phone')
			# email=request.POST.get('email')
			# UserSet.objects.create(name=name)
# 			user.save()
# 			return JsonResponse({'status':'0'})
# 		except:
# 			return JsonResponse({'status':'1'})	
@csrf_exempt
def user_set(request): 
	uid = request.user.uid
	if request.method == 'PATCH':  #個人資訊上傳
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		user = UserSet.objects.get(uid=uid)
		if 1:
			user.name = data['name']
			user.birthday = data['birthday']
			user.height = data['height']
			user.gender = data['gender']
			user.address = urllib.parse.unquote(data['address'])
			user.weight = data['weight']
			user.phone = data['phone']
			user.email = data['email']
			user.save()
			message = {"status":"0"}
		else:
			message = {"status":"1"}
		return JsonResponse(message,safe=False)

	if request.method == 'GET':   # 個人設定展示
		UserProfiledata = UserProfile.objects.get(uid=uid)#s['_auth_user_id']
		UserSetdata = UserSet.objects.get(uid=UserProfiledata.uid)
		if 1:
			message = {
			"status":"0",
			"user":{
			"id":UserProfiledata.id, 
			"name":UserSetdata.name,
			"account":UserProfiledata.account,
			"email":UserProfiledata.email,
			"phone":UserProfiledata.phone,
			# "fb_id":UserProfiledata.fb_id,
			"status":UserSetdata.status,
			"group":"none",
			"birthday":UserSetdata.birthday,
			"height":UserSetdata.height,
			"weight":UserSetdata.weight,
			"gender":UserSetdata.gender,
			"address":UserSetdata.address,
			"unread_records":[0,"0",0],#以上可以
			"verified":int(UserSetdata.verified),
			"privacy_policy":UserSetdata.privacy_policy,
			"must_change_password":1 if UserSetdata.must_change_password else 0,
			# "fcm_id":UserSetdata.fcm_id,
			"badge":int(UserSetdata.badge),
			"login_time":int(UserSetdata.login_times),
			"created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
			"updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")},
			"default":{
			"id": UserProfiledata.id,
			"user_id": UserSetdata.uid,
			"sugar_delta_max":UserSetdata.sugar_delta_max,
			"sugar_delta_min":UserSetdata.sugar_delta_min,
			"sugar_morning_max": UserSetdata.sugar_morning_max,
			"sugar_morning_min": UserSetdata.sugar_morning_min,
			"sugar_evening_max": UserSetdata.sugar_evening_max,
			"sugar_evening_min": UserSetdata.sugar_evening_min,
			"sugar_before_max": UserSetdata.sugar_before_max,
			"sugar_before_min": UserSetdata.sugar_before_min,
			"sugar_after_max": UserSetdata.sugar_after_max,
			"sugar_after_min":UserSetdata.sugar_after_min,
			"systolic_max": UserSetdata.systolic_max,
			"systolic_min": UserSetdata.systolic_min,
			"diastolic_max": UserSetdata.diastolic_max,
			"diastolic_min":UserSetdata.diastolic_min,
			"pulse_max": UserSetdata.pulse_max,
			"pulse_min":UserSetdata.pulse_min,
			"weight_max": UserSetdata.weight_max,
			"weight_min": UserSetdata.weight_min,
			"bmi_max": UserSetdata.bmi_max,
			"bmi_min": UserSetdata.bmi_min,
			"body_fat_max": UserSetdata.body_fat_max,
			"body_fat_min": UserSetdata.body_fat_min,
			"created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
			"updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")},

			"setting":{
			"id": UserProfiledata.id,
			"user_id":UserSetdata.uid,
			"after_recording": int(UserSetdata.after_recording),
			"no_recording_for_a_day": int(UserSetdata.no_recording_for_a_day),
			"over_max_or_under_min": int(UserSetdata.over_max_or_under_min),
			"after_meal":int(UserSetdata.after_meal),
			"unit_of_sugar": int(UserSetdata.unit_of_sugar),
			"unit_of_weight": int(UserSetdata.unit_of_weight),
			"unit_of_height": int(UserSetdata.unit_of_height),
			"created_at":datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
			"updated_at": datetime.strftime(UserProfiledata.updated_at ,"%Y-%m-%d %H:%M:%S")
			}}	
			message = message
			print(message)
		else :
			message = {"status":"1"}
		return JsonResponse(message,safe=False)

@csrf_exempt
def User_defult(request):#測試成功
	if request.method == 'PATCH':  #個人資訊預設值
		data = request.body
		data = str(data, encoding="utf-8")
		# data=json.loads(data)
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		try:
			uid = request.user.uid #(在app上測試)
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
			user = UserSet.objects.get(uid=uid)
			user.sugar_delta_max = data['sugar_delta_max']
			user.sugar_delta_min = data['sugar_delta_min']
			user.sugar_morning_max=data['sugar_morning_max']
			user.sugar_morning_min=data['sugar_morning_min']
			user.sugar_evening_max=data['sugar_evening_max']
			user.sugar_evening_min=data['sugar_evening_min']
			user.sugar_before_max=data['sugar_before_max']
			user.sugar_before_min=data['sugar_before_min']
			user.sugar_after_max = data['sugar_after_max']
			user.sugar_after_min = data['sugar_after_min']
			user.systolic_max=data['systolic_max']
			user.systolic_min=data['systolic_min']
			user.diastolic_max=data['diastolic_max']
			user.diastolic_min=data['diastolic_min']
			user.pulse_max=data['pulse_max']
			user.pulse_min=data['pulse_min']
			user.weight_max=data['weight_max']
			user.weight_min=data['weight_min']
			user.bmi_max=data['bmi_max']
			user.bmi_min=data['bmi_min']
			user.body_fat_max=data['body_fat_max']
			user.body_fat_min=data['body_fat_min']
			user.save()
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def User_setting(request):#測試成功
	if request.method == 'PATCH':  #個人設定
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		try:
			uid = data['token']
			user = UserSet.objects.get(uid=uid)
			uid = request.user.uid 
			user.after_recording = data['after_recording']
			user.no_recording_for_a_day = data['no_recording_for_a_day']
			user.over_max_or_under_min = data['over_max_or_under_min']
			user.after_meal = data['after_meal']
			user.unit_of_sugar = data['unit_of_sugar']
			user.unit_of_weight = data['unit_of_weight']
			user.unit_of_height = data['unit_of_height']
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)


@csrf_exempt
def hba1c(request):
	if request.method == "GET":
		try:
			uid = request.user.uid 
			a1cs = []
			user_alc_list = Medical_Information.objects.filter(uid=uid)
			if user_alc_list:
				for user_alc in user_alc_list:
					a1cs.append(
						{
							"id": user_alc.id,
							"user_id": user_alc.user_id,
							"a1c": user_alc.a1c,
							"recorded_at": user_alc.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
							"created_at": user_alc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
							"updated_at": user_alc.updated_at.strftime('%Y-%m-%d %H:%M:%S')
						}
					)
		except Exception as e:
			message = {"status": "1"}
		else:
			print("get a1c" + " " + "success")
			message = {"status": "0", "a1cs": a1cs}
		finally:
			return JsonResponse(message)

	if request.method == 'POST':  #送糖化血色素
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.uid 
			a1c=data['a1c']
			# recorded_at= str(datetime.strptime(data['recorded_at'], "%Y-%m-%d"))
			Medical_Information.objects.create(uid=uid, a1c=a1c)
			message = {"status":"0"}
		else :
			message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'DELETE':  #刪除糖化血色素
		uid = request.user.uid 
		try:
			if request.GET.getlist("ids[]"):
				for id in request.GET.getlist("ids[]"):
					Medical_Information.objects.filter(
						uid=uid).delete()
		except Exception as e:
			message = {"status": "1"}
		else:
			print("delete a1c" + " " + "success")
			message = {"status": "0"}
		finally:
			return JsonResponse(message)


@csrf_exempt
def med_inf(request):
	if request.method == 'GET': #就醫資訊  #測試成功
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			message = {
			"status":"0",
			"medical_info": {
			"id":user.id,
			"user_id":user.user_id,
			"diabetes_type":user.diabetes_type,
			"oad":user.oad,
			"insulin":user.insulin,
			"anti_hypertensives":user.anti_hypertensives,
			"created_at":user.created_at,
			"updated_at":user.updated_at 
			}
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'PATCH':  #更新就醫資訊 #測試成功
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			user.diabetes_type = data['diabetes_type']
			user.oad = data['oad']
			user.insulin = data['insulin']
			user.anti_hypertensives = data['anti_hypertensives']
			user.save()
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
@csrf_exempt
def drug_inf(request):
	if request.method == 'GET':  # 藥物資訊展示  測試完成
		try:
			drug_useds = []
			uid = request.user.uid 
			drug_list = druginformation.objects.filter(uid=uid)
			if drug_list:
				for drug in drug_list:
					drug_useds.append(
						{
							"id": drug.id,
							"user_id": drug.uid,
							"type": drug.drugtype,
							"name": drug.drugname,
							"recorded_at": drug.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
						}
					)
		except Exception as e:
			message = {"status": "1"}
		else:
			print("get drug" + " " + "success")
			message = {"status": "0", "drug_useds": drug_useds}
		finally:
			return JsonResponse(message)
	if request.method == 'POST':  #藥物資訊 上傳 #測試完成
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			drugtype = data['type']
			uid = request.user.uid 
			druginformation.objects.create(
            uid=uid, drugtype=drugtype,drugname=urllib.parse.unquote(data['name']))
			message = {
			"status":"0"
			}
		else:
	 		message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'DELETE':  #刪除藥物資訊
		uid = request.user.uid 
		try:
			if request.GET.getlist("ids[]"):
				for ID in request.GET.getlist("ids[]"):
					druginformation.objects.filter(id=ID, uid=uid).delete()
		except Exception as e:
			message = {"status": "1"}
		else:
			print("delete" + " " + "success")
			message = {"status": "0"}
		finally:
			return JsonResponse(message)

@csrf_exempt
def notification(request):
	if request.method == 'POST':  #親友團通知
		data = request.body
		data = str(data, encoding="utf-8")
		# data=json.loads(data)
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		try:
			uid = request.user.uid 
			user = Notification.objects.get(uid=uid)
			user.message = data['message']
			user.save()
			message = {
			"status":"0"
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def share(request):
	if request.method == 'POST':  #分享
		data = request.body
		data = str(data, encoding="utf-8")
		# data=json.loads(data)
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.uid 			
			user = Share.objects.get(uid=uid)
			user.data_type = data['type']
			user.fid= data['id']
			user.relation_type = data['relation_type']
			user.save()
			message = {
			"status":"0"
			}
		else:
			message = {"status":"1"}
		return JsonResponse(message)
		
@csrf_exempt
def share_check(request):
	if request.method == 'GET':  # 查看分享（含自己分享出去的）!
		uid = request.user.uid 		
		user_pro = UserProfile.objects.get(uid=uid)
		user = UserSet.objects.get(uid=uid)
		print("123123")
		if Share.data_type == '0' :
			share_data = Blood_pressure.objects.get(uid=uid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"systolic":share_data.systolic,
				"diastolic":share_data.diastolic,
				"pulse":share_data.pulse,
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":0,
				"user":
					{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if Share.data_type == '1' :
			share_data = Weight.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"weight":float(share_data.weight),
				"body_fat":float(share_data.body_fat),
				"bmi":float(share_data.bmi),
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":1,
				"user":
					{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if Share.data_type == '2' :
			share_data = Blood_sugar.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"sugar":float(share_data.sugar),
				"timeperiod":int(share_data.timeperiod),
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":2,
				"user":
					{
					"id":user_pro.id,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if Share.data_type == '3' :
			share_data = Diary_diet.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			image = str(share_data.image)
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"description":share_data.description,
				"meal":int(share_data.meal),
				"tag":share_data.tag,
				"image":str(image),
				"lat":share_data.lat,
				"lng":share_data.lng,
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":3,
				"user":{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		message = {"status":"0"}
	else:
		message = {"status":"1"}
	return JsonResponse(message)


@csrf_exempt
def newnews(request): #最新消息
	if request.method == 'GET':
		uid = request.user.uid 		
		# user = UserProfile.objects.get(uid=uid)
		# user1 = UserSet.objects.get(uid=uid)
		# user2 = Notification.objects.get(uid=uid)
		if 1:
			message = {
			'status':'0',
			'news':{
				"id": 2,
                "member_id": 1,
                "group": 1,
                "message": "456",
                "pushed_at": "2017-11-16 16:33:06",
                "created_at": "null",
                "updated_at": "null"
				}
			}
		else:
			message = {'status':'1'}
		return JsonResponse(message)

@csrf_exempt
def badge1(request):
	if request.method == 'PUT': #更新badge
			# data = request.body
			# data = str(data, encoding="utf-8")
			# data = {
			# i.split('=')[0]: i.split('=')[1]
			# for i in data.replace("%40","@").split('&') if i.split('=')[1]
			# }

			# s = Session.objects.get(
			# pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()

			# UserProfiledata = UserProfile.objects.get(id=s['_auth_user_id'])
			# user = UserSet.objects.get(uid=UserProfiledata.uid)
			if 1:
				# user.badge = data['badge']
				# user.save()
				status = {"status":"0"}
			else:
				status = {"status":"1"}

			return JsonResponse(status)