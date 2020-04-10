from db import get_messages_store, get_user_store, get_channel_store, make_message 
from db import member_channel_check, owner_channel_check, react_check, member_channel_check
from db import token_check, channel_check, u_id_check, check_user_in_channel, message_check
from error import InputError, AccessError
import datetime
from datetime import timezone
import time



from auth import auth_register
from channel import channels_create,channel_invite

def message_send(token, channel_id, message):
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)
    if channel == None: 
        raise InputError
    #if check_user_in_channel(user['u_id'], channel_id) == False: 
    #    raise AccessError
    if (len(message) > 1000): 
        raise InputError
    
    if member_channel_check(token, channel_id) == False:
        raise AccessError
   # message_store = get_messages_store()
    for member in channel['all_members']: 
        if user['u_id'] == member['u_id']: 
            message_id = make_message(message, channel_id, user['u_id'], 0)
    return {
        'message_id': message_id,
    }

def message_send_later(token, channel_id, message, time_sent): 
    print('1')
    user = token_check(token)
    if user == False:  
        raise InputError
    channel = channel_check(channel_id)
    print('2')
    if channel == False: 
        raise InputError
    print('3')
    if member_channel_check(token, channel_id) == False: 
        raise AccessError
    if (len(message) > 1000): 
        raise InputError
    print('4')
    print('TIME_SENT',time_sent) 
    print('now',datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()) 
    if int(time_sent) < int(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()): 
        print('ENTERS IF STATEMENT')
        raise InputError
    message_store = get_messages_store()
    print('5')
    for member in channel['all_members']: 
        if user['u_id'] == member['u_id']:
            #time.mktime(t.timetuple())
            
            wait_time = time_sent - datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp() 
            time.sleep(wait_time)
            #wait_time = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(time_sent.timetuple())
            message_id = make_message(message, channel_id, user['u_id'], 0)
            
    return {
        'message_id': message_id,
    }


def message_react(token, message_id , react_id): 
    message = message_check(message_id)
    #print("This is message----->", message)
    if message == None:
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
        raise InputError   

    user = token_check(token)
    if user == None:
        raise AccessError
    
    if react_check(message_id, user['u_id'], react_id) == True:
        raise InputError

    is_this_user_reacted = False;    

    flag = 0
    for reacts in message['reacts']:
        if reacts['react_id'] == react_id:
            reacts['u_ids'].append(int(user['u_id']))
            flag = 1
            if reacts['is_this_user_reacted'] == True:
                is_this_user_reacted = True

    if message['user_id'] == user['u_id']:
        is_this_user_reacted = True
        
    if flag ==0:    
        dict_append  = { 'u_ids': [int(user['u_id'])], 'react_id' : int(react_id), 'is_this_user_reacted' : is_this_user_reacted  }
        message['reacts'].append(dict_append)
    return{
    }

def message_unreact(token, message_id , react_id): 
    message = message_check(message_id)
    #print("This is message----->", message)
    if message == None:
        raise InputError
    if react_id != 1:   #This is assuming that there's only 1 react id (1)
        raise InputError    
    user = token_check(token)
    if user == None:
        raise AccessError
    
    if react_check(message_id, user['u_id'], react_id) == False:
        raise InputError

    flag = 0 
    for reacts in message['reacts']:
        if reacts['react_id'] == react_id:
            if user['u_id'] in reacts['u_ids']:
                reacts['u_ids'].remove(user['u_id'])
                if len(reacts['u_ids']) == 0:
                    flag = 1

    if flag == 1:
        #dict_append  = { 'u_ids': user['u_id'], 'react_id' : react_id  }
        
        for react in message['reacts']:
            if react_id == react['react_id']:
                break
        message['reacts'].remove(react)
    return{

    }

def message_pin(token, message_id): 
    message = message_check(message_id)
    if message == None:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError
    if owner_channel_check(token, message['channel_id']) == False:
        raise InputError
    if message['is_pinned'] == True:
        raise InputError
    message['is_pinned'] = True
    return {

    }


def message_unpin(token, message_id): 
    message = message_check(message_id)
    if message == None:
        raise InputError
    if member_channel_check(token, message['channel_id']) == False:
        raise AccessError 
    if owner_channel_check(token, message['channel_id']) == False:
        raise InputError   
    if message['is_pinned'] == False:
        raise InputError    
    message['is_pinned'] = False 
    return {

    }
def message_remove(token, message_id):
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == None:
        raise AccessError

    is_sender = False
    #print("message----->",message)
    if user['u_id'] == message['user_id']:
        is_sender = True

    print('is owner: ',is_owner,'is_sender:', is_sender)
    if (is_owner or is_sender) == False:
        raise AccessError

    message_data = get_messages_store()
    message_data['Messages'].remove(message)
    return {
    }


def message_edit(token, message_id, edited_message):
    message = message_check(message_id)
    if message == None:
        raise InputError
    is_owner = owner_channel_check(token, message['channel_id'])
    user = token_check(token)
    if user == False:
        raise AccessError

    is_sender = False
    #print("message----->",message)
    if user['u_id'] == message['user_id']:
        is_sender = True

    if (is_owner or is_sender) == False:
        raise AccessError

    message['message'] = edited_message
 
    #message_data = get_messages_store()
    #message_data['Messages'].remove(message)
    return {
    }



hayden_dict =  auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
chan_id = channels_create(hayden_dict['token'], 'Hayden', True)
rob_dict = auth_register("rob@gmail.com", "paswword123", "Rob", "Ever")
message_id = message_send(hayden_dict['token'], chan_id['channel_id'], "Haydens Message")


print('Hayden:', hayden_dict)
print()
print('Rob:', rob_dict)
print()
print()
print()
message_react(hayden_dict['token'],message_id['message_id'] , 1)
channel_invite(hayden_dict['token'], chan_id["channel_id"], rob_dict["u_id"])
message_react(rob_dict['token'],message_id['message_id'] , 1)
print(get_messages_store())
