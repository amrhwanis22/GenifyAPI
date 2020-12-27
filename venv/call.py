import requests

BASE = 'http://127.0.0.1:5000/'

vidz = [{'name':'amr33','views':90,'likes':20},
        {'name':'amr22','views':90,'likes':20},
        {'name':'amr2','views':90,'likes':20},
        {'name':'amr1','views':90,'likes':20}]

# for i in range(len(vidz)):
#     response =requests.put(BASE+'video/'+str(i),vidz[i])
# response = requests.put(BASE+'video/1',{'name':'amr','views':90,'likes':20})
#     print(response.json())
# print(requests.get(BASE+'recodemo').json())
headers = {'Content-type': 'application/json'}

response = requests.post(BASE+'/recodemo/',json={},headers=headers)
print(response)
#
# response = requests.post(BASE+'helloworld')
# print(response.json()['data'])
