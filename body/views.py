from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import auth
from django.core.mail import send_mail, send_mass_mail
import uuid,email.message,smtplib,hashlib,random
from django.contrib.sessions.models import Session
import uuid
from friend.models import Friend_data
from imgurpython import ImgurClient
# Create your views here.

@csrf_exempt
def b_pressure(request):#上傳成功,但是終端機會報錯
	if request.method == 'POST':  #上傳血壓測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.id #(在app上測試)			
			user = Blood_pressure.objects.get(id=uid)
			user.systolic = data['systolic']
			user.diastolic = data['diastolic']
			user.pulse = data['pulse']
			# user.recorded_at=recorded_at
			user.save()
			return JsonResponse({"status":"0"})
		else:
			return JsonResponse({"status":"1"})

@csrf_exempt
def weight(request):#上傳成功,但是終端機會報錯
	if request.method == 'POST':#上傳體重測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.id #(在app上測試)
			user = Weight.objects.get(id=uid)
			user.weight=data['weight']
			user.body_fat=data['body_fat']
			user.bmi=data['bmi']
			# user.recorded_at=data['recorded_at']
			user.save()
			return JsonResponse({"status":"0"})
		else:
			return JsonResponse({"status":"1"})
			
@csrf_exempt
def b_sugar(request):#上傳成功,但是終端機會報錯  #串完
	if request.method == 'POST':#上傳體重測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		print("123")
		if 1:
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			uid = request.user.id #(在app上測試)
			user = Blood_sugar.objects.get(id=uid)
			user.sugar=data['sugar']
			user.timeperiod=data['timeperiod']
			user.recorded_at=data['recorded_at']
			user.save()
			return JsonResponse({"status":"0"})
		else:
			return JsonResponse({"status":"1"})

@csrf_exempt
def last_upload(request):#測試成功
	if request.method == 'GET':#最後上傳時間
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		uid = request.user.id #(在app上測試)
		user = Weight.objects.get(id=uid)
		user1 = Blood_sugar.objects.get(id=uid)
		user2 = Blood_pressure.objects.get(id=uid)
		try:
			user.save()
			return JsonResponse({
			"status": "0",
			"last_upload": {
			"blood_pressure": user2.pulse,
			"weight": user.weight,
			"blood_sugar": user1.sugar
			# "diet": user1.date
			}
			})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def records(request):#測試成功   #串完
	uid = request.user.id
	if request.method == 'POST':#上一筆紀錄資訊
		# data = request.body
		# data = str(data, encoding="utf-8")
		# print(data)
		# data=json.loads(data) #少一個input "diets"
		# print("777")
		if 1:
			print("123123")
			user = Blood_sugar.objects.get(id=uid)
			print("234234")
			user1 = Blood_pressure.objects.get(id=uid)
			print("234456567674234")
			user2 = Weight.objects.get(id=uid)
			return JsonResponse({
			"status":"0",
			"blood_sugars":{
			"id":user.id,
			"user_id":user.user_id,
			"sugar":user.sugar,
			"timeperiod":user.timeperiod,
			"recorded_at":str(user.recorded_at)
			},
			"blood_pressures":{
			"id":user1.id,
			"user_id":user1.user_id,
			"systolic":user1.systolic,
			"diastolic":user1.diastolic,
			"pulse":user1.pulse,
			"recorded_at":str(user1.recorded_at)
			},
			"weights":{
			"id":user2.id,
			"user_id":user2.user_id,
			"weight":user2.weight,
			"body_fat":user2.body_fat,
			"bmi":user2.bmi,
			"recorded_at":str(user2.recorded_at)
			}
			})
		# return JsonResponse({"status":"1"})
	if request.method == 'DELETE':#刪除日記記錄
		try:
			user = Blood_sugar.objects.get(id=uid)
			user.delete()
			user1 = Blood_pressure.objects.get(id=uid)
			user1.delete()
			user2 = Weight.objects.get(id=uid)
			user2.delete()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def diary(request):
	if request.method == 'GET':#日記列表資料
		uid = request.user.id
		date = request.GET.get("date")
		diary = []
		if date:
			if Blood_pressure.objects.filter(uid=uid):
				blood_pressures = Blood_pressure.objects.filter(uid=uid, date=date)
				for blood_pressure in blood_pressures:
					r = {
							"id":blood_pressure.id,
							"user_id":blood_pressure.uid, 
							"systolic":blood_pressure.systolic,
							"diastolic":blood_pressure.diastolic,
							"pulse":blood_pressure.pulse,
							"recorded_at":str(blood_pressure.recorded_at),
							"type":"blood_pressure"
						}
					diary.append(r)
			if Weight.objects.filter(uid=uid):
				weights = Weight.objects.filter(uid=uid, date=date)
				for weight in weights:
					r = {
							"id":weight.id,
							"user_id":weight.uid,
							"weight":weight.weight,
							"body_fat":weight.body_fat,
							"bmi":weight.bmi,
							"recorded_at":str(weight.recorded_at),
							"type":"weight"
						}
					diary.append(r)
			if Blood_sugar.objects.filter(uid=uid):
				blood_sugars = Blood_sugar.objects.filter(uid=uid, date=date)
				for blood_sugar in blood_sugars:
					r = {
							"id":blood_sugar.id,
							"user_id":blood_sugar.uid, 
							"sugar":int(blood_sugar.sugar), 
							"timeperiod":int(blood_sugar.timeperiod), 
							"recorded_at":str(blood_sugar.recorded_at),
							"type":"blood_sugar"
						}
					diary.append(r)
			output = {"status":"0", "diary":diary}      
		else:
			output = {"status":"1"}
		# print(json.dumps(output))
		return JsonResponse(output)

@csrf_exempt
def diary_diet(request):
	if request.method == 'POST':#飲食日記
		data = request.body
		data = str(data, encoding="utf-8")
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			uid = request.user.id #(在app上測試)
			user = Diary_diet.objects.get(id=uid)
			print("2")
			user.meal=data['meal']
			user.tag = request.POST.getlist("tag[][]")
			image = request.POST.get("image")
			# user.description = data['description']
			user.image_count = image
			user.lat=data['lat']
			user.lng=data['lng']
			user.recorded_at=data['recorded_at']
			user.save()
			# return JsonResponse(output = {"status":"0", "image_url":"http://211.23.17.100:3001/diet_1_2021-10-21_11:11:11_0"})
			return JsonResponse(output = {"status":"0"})
		else:
			return JsonResponse({"status":"1"})

@csrf_exempt
def care(request):  
	if request.method == 'POST':  #發送關懷諮詢 #測試完成
		data = request.body
		data = str(data, encoding="utf-8")
		# data=json.loads(data)
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.id #(在app上測試)
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			user = UserCare.objects.get(id=uid)
			user.message = data['message']
			user.save()
			return JsonResponse({"status":"0"})
		else:
			return JsonResponse({"status":"1"})
	if request.method == 'GET':#獲取關懷諮詢 #測試完成
		# data = request.body
		# data = str(data, encoding="utf-8")
		# # data=json.loads(data)
		# data = {
		# 	i.split('=')[0]: i.split('=')[1]
		# 	for i in data.replace("%40","@").split('&') if i.split('=')[1]
		# }
		uid = request.user.id #(在app上測試)
		# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
		user = UserCare.objects.get(id=uid)
		if 1:
			return JsonResponse(
			{
			"status": "0",
			"cares":
			{
			"id":user.id,
			"user_id":user.uid, 
			"member_id": user.member_id,
			"reply_id": user.reply_id,
			"message": user.message, 
			"created_at": user.created_at,
			"updated_at": user.updated_at
			}
			}
			)
		else:
			return JsonResponse({"status":"1"})
			