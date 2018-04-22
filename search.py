from variables import *
from workout import *
from exercise import *
from flask_pymongo import PyMongo
import re

#User object for search result
class SearchedUser(object):
    name = ""
    objId = ""
    isFriend = False

#Creates searchedUser object
def make_user(name, id, isFriend):
    searchedUser = SearchedUser()
    searchedUser.name = name
    searchedUser.objId = id
    searchedUser.isFriend = isFriend
    return searchedUser

class SearchResult(object):
    #Users
    users = []
    #Workouts
    workouts = []

#Searches a MDB called "mongo" with the query "search"
def searchQuery(search, mongo, current_user):
    searchResult = SearchResult()
    #Code to find users
    regex = re.compile(".*" + search + ".*", re.IGNORECASE)
    searchedUsers = mongo.db.users.find({"name": regex})
    searchResult.users.clear()
    for user in searchedUsers:
        if (user['_id'] != current_user['_id']): #You cannot search your own profile
            if (user['_id'] not in current_user['user_friends']): #You can only follow users you do not follow already
                searchResult.users.append(make_user(user['name'], user['_id'], True))
            else:
                searchResult.users.append(make_user(user['name'], user['_id'], False))

    #Code to find workouts
    searchedWorkouts = mongo.db.workouts.find({"tags": regex})
    for workout in searchedWorkouts:
        if (workout['_id'] not in current_user['user_workouts']):
            print("searched")
            if (workout['_id'] not in searchResult.workouts):
                print("added")
                searchResult.workouts.append(workout['_id'])
    return searchResult