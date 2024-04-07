import requests
import json
# we also pip installed flask and flask-sqlalchemy
# we ran pip freeze > requirements.txt so know what all of the dependencies are 

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')

print(response) # returns 200 which means successful

# print(response.json()) # returns the entire json response

for questionData in (response.json()['items']):

    if questionData['answer_count'] == 0:
        print(questionData['title'])
        print(questionData['link']  + "\n")
    # else:
    #     print('skipped')
    # print() #same as printing a new line
