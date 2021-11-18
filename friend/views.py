from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
from user.models import UserSet,UserProfile,druginformation,Medical_Information
from datetime import datetime
# Create your views here.
@csrf_exempt
def friend_code(request):
	if request.method == 'GET':  #獲取空糖團邀請碼
		# data = request.body
		# data = str(data, encoding="utf-8")
		# data=json.loads(data)
		if 1:
			uid = request.user.uid #(在app上測試)
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			user = Friend.objects.get(uid=uid)
			message = { 
			"status":"0",
			'invite_code':user.invite_code
			}
		else:
			message = {"status":"1"}
		return JsonResponse(message)
@csrf_exempt
def friend_list(request): # 控糖團列表!
	uid = request.user.uid 
	friends = []
	friends_list = Friend_data.objects.filter(relation_id=uid, status=1)  # 好友列表(被邀請人)
	if friends_list:
		for friend in friends_list:
			friend_profile = UserProfile.objects.get(uid=uid)  # 好友登入資料
			friend_set = UserSet.objects.get(uid=uid)  # 好友個人資料
			friends.append(
				{
					"id": friend_profile.id,
					"name": "test",
					"account": friend_profile.account,
					"email": friend_profile.email,
					"phone": friend_profile.phone,
					# "fb_id": friend_profile.fb_id,
					"status": friend_set.status,
					"group": friend_set.group,
					"birthday": friend_set.birthday,
					"height": friend_set.height,
					"gender": int(friend_set.gender) if friend_set.gender != None else friend_set.gender,
					"verified": int(friend_set.verified),
					"privacy_policy": int(friend_set.privacy_policy),
					"must_change_password": int(friend_set.must_change_password),
					"badge": friend_set.badge,
					# "created_at": friend_set.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					# "updated_at": friend_set.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
					"relation_type": friend.friend_type
				}
			)
	message = {"status": "0", "friends": friends}
	return JsonResponse(message)


@csrf_exempt
def friend_requests(request):#測試完成
	if request.method == 'GET':  #獲取空糖團邀請碼
		uid = request.user.uid 
		requests = Friend_data.objects.filter(relation_id=uid, status=0)
		if requests:
			user = UserSet.objects.get(uid=uid)
			user1 = UserProfile.objects.get(uid=uid)
			user2 = Friend_data.objects.get(uid=uid)
			user3 = druginformation.objects.get(uid=uid)
			user4 = Medical_Information.objects.get(uid=uid)
			list=[]
			message_list = { 
			"status":"0",
			"requests":
			{
			"id":user.id,
			"user_id":user4.user_id,
			"relation_id":"1",
			"type":user3.drugtype,
			"created_at": user1.created_at,
			"updated_at": user1.updated_at},
			"user":
			{
			"id":user.id,
			"name": "test",
			"account":user1.account,
			"email": user.email,
			"phone": user.phone,
			# "fb_id": user1.fb_id,
			"status": "1",
			"group": "1",
			"birthday": user.birthday,
			"height": user.height,
			"gender": user.gender,
			"verified": "1",
			"privacy_policy": "1",
			"must_change_password": user.must_change_password,
			"badge": "87",
			"created_at": user1.created_at,
			"updated_at": user1.updated_at,}
			}
			list.append(message_list)
			message = {"status":"0", "requests":list}
		else:
			uid = request.user.uid #(在app上測試)
			user = UserSet.objects.get(uid=uid)
			user1 = UserProfile.objects.get(uid=uid)
			user2 = Friend_data.objects.get(uid=uid)
			user3 = druginformation.objects.get(uid=uid)
			user4 = Medical_Information.objects.get(uid=uid)
			message = { 
			"status":"0",
			"requests":
			{
			"id":user.id,
			"user_id":user4.user_id,
			"relation_id":"1",
			"type":user3.drugtype,
			"created_at": user1.created_at,
			"updated_at": user1.updated_at},
			"user":
			{
			"id":user.id,
			"name": user.name,
			"account":user1.account,
			"email": user.email,
			"phone": user.phone,
			# "fb_id": user1.fb_id,
			"status": "Normal",
			"group": "???",
			"birthday": user.birthday,
			"height": user.height,
			"gender": user.gender,
			"verified": "1",
			"privacy_policy": "1",
			"must_change_password": user.must_change_password,
			"badge": "87",
			"created_at": user1.created_at,
			"updated_at": user1.updated_at,}
			}
		return JsonResponse(message)
@csrf_exempt
def friend_send(request):#測試完成
	if request.method == 'POST':  #送出控糖團邀請
		data = request.body
		data = str(data, encoding="utf-8")
		# data=json.loads(data)
		data = {
			i.split('=')[0]: i.split('=')[1]
			for i in data.replace("%40","@").split('&') if i.split('=')[1]
		}
		if 1:
			uid = request.user.uid #(在app上測試)
			# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)	
			user = Friend.objects.get(uid=uid)
			try:
				invite_code = data['invite_code']
				profile = Friend.objects.get(invite_code=invite_code)
				if profile:
					message = {"status":"0"}
				# if profile.invite_code=="123456":
				# 	message = {"status":"0"}
			except:
				message = {"status":"1"}
		else:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def friend_accept(request):
	if request.method == 'GET':  #接受控糖團邀請
		uid = request.user.uid 
		# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
		if 1:
			check = Friend_data.objects.get(uid =uid,status=0)
			check.friend_type="1"
			check.relation_id=uid
			check.read = True
			check.status = 1
			# check.updated_at = nowtime
			check.save()
			output = {"status":"1"}
		else:
			output = {"status":"0"}
		return JsonResponse(output,safe=False)

@csrf_exempt
def friend_refuse(request): # 拒絕控糖團邀請
	if request.method == 'GET':
		uid = request.user.id
		# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
		if 1:
			check = Friend_data.objects.get(uid =uid,status=0)
			check.read = True
			check.friend_type="1"
			check.status = 2
			# check.updated_at = nowtime
			check.save()
			output = {"status":"0"}
		else:
			output = {"status":"1"}
		return JsonResponse(output,safe=False)

@csrf_exempt
def friend_remove(request,friend_data_id): # 刪除控糖團邀請
	uid = request.user.id
	if request.method == 'GET':
		try:
			Friend_data.objects.filter(id=friend_data_id, status=0).delete()
		except:
			message = {"status":"1"}
		else:
			message = {"status":"0"}
		return JsonResponse(message)

@csrf_exempt
def friend_results(request): # 控糖團結果!
	uid = request.user.id
	# uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
	if request.method == 'GET':
		if Friend_data.objects.filter(uid=uid, read=True, imread=False):
			results = []
			result = Friend_data.objects.filter(uid=uid, read=True, imread=False).latest('updated_at')
			user_pro = UserProfile.objects.get(id=result.relation_id)
			relation = UserSet.objects.get(uid=user_pro.uid)
			created_at_friendata = datetime.strftime(result.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_friendata = datetime.strftime(result.updated_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":result.id,
				"user_id":result.uid,
				"relation_id":result.relation_id,
				"type":result.friend_type,
				"status":int(result.status),
				"read":result.read,
				"created_at":created_at_friendata,
				"updated_at":updated_at_friendata,
				"relation":
						{
							"id":user_pro.id,
							"name":relation.name,
							"account":relation.email,
							"email":relation.email,
							"phone":relation.phone,
							"fb_id":user_pro.fb_id,
							"status":relation.status,
							"group":relation.group,
							"birthday":str(relation.birthday),
							"height":relation.height,
							"gender":relation.gender,
							"verified":relation.verified,
							"privacy_policy":relation.privacy_policy,
							"must_change_password":relation.must_change_password,
							"badge":int(relation.badge),
							"created_at":created_at_userfile,
							"updated_at":updated_at_userfile
						}
					}
			result.imread = True
			result.save()
			results.append(r)
			output = {"status":"0", "results":results}
		else:
			output = {"status":"1"}
	return JsonResponse(output)
@csrf_exempt
def friend_remove_more(request): # 刪除更多好友!
	uid = request.user.id
	if request.method == "GET":
		try:
			if Friend.objects.filter(user_ID=uid, status=0):
				Friend.objects.filter(
					user_ID=uid, status=0).delete()
			else:
				raise Exception("ErrorFriendID")
		except Exception as e:
			message = {"status": "1"}
		else:
			message = {"status": "0"}
		finally:
			print("friend get remove" + " " + "success")
			return JsonResponse(message)
	elif request.method == "DELETE":
		try:
			if Friend_data.objects.filter(user_ID=uid, status=1):
				Friend_data.objects.filter(
					relation_id=uid, status=1).delete()
			else:
				raise Exception("ErrorFriendID")
			# 邀請人
			# if Friend_data.objects.filter(relation_id=uid, status=1):
			# 	Friend.objects.filter(
			# 		uid=uid, relation_=ID, status=1).delete()
			# 被邀請人
			# Friend.objects.filter(uid="0f2541f1-8953-3ed4-9673-fb41519e21c2", relation_id=uid, status=1).delete()
		except Exception as e:
			message = {"status": "1"}
		else:
			message = {"status": "0"}
		finally:
			return JsonResponse(message)
