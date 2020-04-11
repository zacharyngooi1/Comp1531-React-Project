import jwt
from db import get_user_store, add_user, login, make_user
from db import login, make_user, get_channel_store, get_messages_store
from db import token_check, channel_check, u_id_check, member_channel_check
from error import InputError, AccessError
from random import randrange
from datetime import timezone

def channel_invite(token, channel_id, u_id):

    ''' Invites a user to join a channel that they are not already in
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): unique user identification
       
    '''

    if channel_check(channel_id) == False:
        raise InputError

    if u_id_check(u_id) == False:
        return InputError

    if check_if_user_in_channel_member_uid(u_id, channel_id) == True:
        raise AccessError

    channel_store = get_channel_store()
    user = u_id_check(u_id)
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            channel["all_members"].append({"u_id": user["u_id"], "name_first": user['name_first'], "name_last" : user["name_last"]})    
    
    user['channel_id_part'].append(channel_id)

    return {} 

def channel_details(token, channel_id):
    '''Provides user with the basic information of a channel, given channel id, if 
    user is part of channel.
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
        
        Returns: 
            (dict): returns details about channel 
    
    '''
    if channel_check(channel_id) == False:
        raise InputError
    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    ch_dict = {
    }
    channel_info = channel_check(channel_id)
    ch_dict['name'] = channel_info['name']
    ch_dict['owner_members'] = channel_info['owner_members']
    ch_dict['all_members'] = channel_info['all_members']
    return ch_dict

def channel_messages(token, channel_id, start):
    '''Returns a range of 50 messages in a channel, if user is part of that channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            start (int): which message wants to start range at 
        
        Returns: 
            (list): returns list of messages from channel 
    '''
    print('This is start:',start)
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError
    
    sum_of_messages = 0
    
    message_store = get_messages_store()
    
    for x in message_store['Messages']:
            if x['channel_id'] == channel_id:
                sum_of_messages += 1
    
    if start > sum_of_messages:
        raise InputError

    proto_dict = {
        'messages':[]
    }

    final_dict = {
        'messages':[]
    }
    proto_dict = get_messages_store()['Messages']
    print()
    print('THIS IS YA PROTO DICT:',proto_dict)
    print()
    #proto_dict.reverse()
    print()
    print('THIS IS POST REVERSE:',proto_dict)
    print()
    
    print()
    print('THIS IS YA MSG STORE:',get_messages_store()['Messages'])
    print()
    #print('Messages:',get_messages_store()['Messages'])
    #print('Proto_dict:',proto_dict)
    counter = 0
    if len(proto_dict) != 0:
        print('in the if loop aye ')
        for message in reversed(proto_dict):
          #  print()
           #print()
            #print('this is it')
            if int(message['channel_id']) == int(channel_id):
                #print('SO CLOSE')
                if counter >= start:
                    #print('Ican smell it')
                    dict_to_app = {
                        'message_id':message['message_id'],
                        'u_id': message['user_id'],
                        'message': message['message'],
                        'time_created': message['time_created'].replace(tzinfo=timezone.utc).timestamp(),
                        'reacts': message['reacts'],
                        'is_pinned': message['is_pinned']
                        
                    }
                    final_dict['messages'].append(dict_to_app)    
                counter = counter + 1
            if counter >= 50:
                counter = -1
                break
    
    final_dict['start'] = start
    final_dict['end'] = counter
    
    print('This is the dictionary:',final_dict)
    return final_dict
    #for x in message_store['Messages']:
    #    if x['channel_id'] == channel_id:
    #        proto_dict['messages'].append(x['message'])

    # Now i reverse the list to get the most recent message as the first value
    #proto_dict['messages'].reverse()

    #for i in range(50):
    #    for y in proto_dict['messages']:
    #        final_dict['messages'].append(y[start + i])
    #        final_dict['start'] = start
    #        final_dict['end'] = start + 50
    #        if start + 50 >= sum_of_messages:
    #            final_dict['end'] = -1
    #print(final_dict)
    return final_dict

def channel_leave(token, channel_id):
    '''Removes member from a channel.

        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
    '''

    print("BEFORE ERROR STATEMENTS")
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_member(token, channel_id) == False:
        raise AccessError

    channel = channel_check(channel_id)
    print("TEST this is ur channel", channel)
    user = token_check(token)
    print("TEST THIS is ur user", user)
    for inner in channel['all_members']:
        if inner['u_id'] == user['u_id']:
            print(inner['u_id'], user['u_id'])
            channel['all_members'].remove(inner)
            print("USER REMOVED")

    for leave in user['channel_id_part']:
        if leave == channel_id:
            print(leave, channel_id)
            user['channel_id_part'].remove(leave)
            print("CHANNEL REMOVED")
    return {}


def channel_join(token, channel_id):
    '''Adds a member to a channel.
    
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
        
    '''
    if channel_check(channel_id) == False:
        print("enters first error")
        raise InputError

    if (check_if_channel_is_public(channel_id) == False or
    check_if_user_in_channel_member(token, channel_id) == True):
        print("enters second error")
        raise AccessError
    
    print("gets passed errors")

    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    user = token_check(token)

    for channel in channel_store["Channels"]:
        print("gets in for loop")
        if channel["channel_id"] == int(channel_id):
            print("gets in if statement")
            channel["all_members"].append({"u_id": user["u_id"], 
            "name_first": user['name_first'], "name_last" : user["name_last"]})

    user['channel_id_part'].append(channel_id)

    return {} 


def channel_addowner(token, channel_id, u_id):
    '''Adds someone as owner to a channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): user identification 
        
    '''
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == True:
        raise InputError
    
    permission_error = token_check(token)

    if check_if_user_in_channel_owner(token, channel_id) == False:
        if permission_error['permission_id'] != 1:
            raise AccessError
        else:
            pass

    
    channel_store = get_channel_store()
    user = u_id_check(u_id)

    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            if member_channel_check(user['token'], channel_id) == False:
                channel["all_members"].append({"u_id": user["u_id"],
             "name_first": user['name_first'], "name_last" : user["name_last"]})
            channel["owner_members"].append({"u_id": user["u_id"],
             "name_first": user['name_first'], "name_last" : user["name_last"]})

            

    user['channel_id_owned'].append(channel_id)
    user['channel_id_part'].append(channel_id)
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    '''Removes someone from owner to a channel.
   
        Parameters: 
            token (str): authorization hash 
            channel_id (int): channel identification
            u_id (int): user identification 
        
    '''
    if channel_check(channel_id) == False:
        raise InputError

    if check_if_user_in_channel_owner_uid(u_id, channel_id) == False:
        raise InputError

    permission_error = token_check(token)

    if check_if_user_in_channel_owner(token, channel_id) == False:
        if permission_error['permission_id'] != 1:
            raise AccessError
        else:
            pass

    user = u_id_check(u_id)
    channel_store = get_channel_store()
    for channel in channel_store["Channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["owner_members"]:
                if member["u_id"] == u_id:
                    channel["owner_members"].remove(member)

    for leave in user['channel_id_owned']:
        if leave == channel_id:
            user['channel_id_owned'].remove(leave)

    return {}

def channels_create(token, name, is_public):
    '''Creates a new channel.
   
        Parameters: 
            token (str): authorization hash 
            name (string): what channel will be named
            is_public (bool): true/false for public channel
        
        Returns: 
            (int): channel id 
        
    '''
    if len(name) > 20:
        raise InputError

    channel_dict = {
        'channel_id': len(name) + len(token) + randrange(25000),
        'owner_members':[],
        'all_members':[],
        'is_public': is_public,
        'name' : name,
        'standup' : {'is_standup_active':False, 'time_standup_finished':None, "standup_message":""}
    }

    store = get_channel_store()
    
    user_store = token_check(token)
    if user_store == False:
         raise InputError

    channel_dict['owner_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    channel_dict['all_members'].append({'u_id': user_store['u_id'], 'name_first': user_store['name_first'], 'name_last': user_store['name_last']})
    
    store['Channels'].append(channel_dict)
    user_store['channel_id_owned'].append(channel_dict["channel_id"])
    user_store['channel_id_part'].append(channel_dict["channel_id"])
    return {
        'channel_id' : channel_dict["channel_id"]
    }

def channels_list_all(token):
    '''Returns all channels.
    
        Parameters: 
            token (str): authorization hash 
        
        Returns: 
            (list):  list of channels
    '''
    if token_check(token) == False:
        raise InputError
    channel_store = get_channel_store()
    empty_list = []
    for channels in channel_store['Channels']:
        empty_list.append({"channel_id" : channels["channel_id"], "name" : channels["name"]})
    return {'channels':empty_list}

def channel_list(token):
    '''Lists channels a user is apart of.

        Parameters: 
            token (str): authorization hash 
            name (string): what channel will be named
            is_public (bool): true/false for public channel
        
        Returns: 
            (int): channel id 
    '''
    if token_check(token) == False:
        raise InputError
    channel_store = get_channel_store()
    user = token_check(token)
    empty_list = []
    for channels in channel_store["Channels"]:
        for member in channels['all_members']:
            if member["u_id"] == user["u_id"]:
                empty_list.append({"channel_id" : channels["channel_id"], "name" : channels["name"]})
    return {'channels':empty_list}


#####################################
##        Checker functions        ##
#####################################

def check_if_user_in_channel_member(token, channel_id):
    user = token_check(token)
    channel_store = get_channel_store()
    result = False
    print("in check")
    print(channel_store)
    for mem_check in channel_store["Channels"]:
        print("in for loop")
        print(mem_check['channel_id'])
        print()
        print(channel_id)
        if mem_check['channel_id'] == int(channel_id):
            print("gets to first if statement")
            print()
            for mem in mem_check['all_members']:
                print("in second for loop")
                if mem["u_id"] == user["u_id"]:
                    print("gets to second if statemtn")
                    result = True
            for mem2 in mem_check['owner_members']:
                print("in second for loop")
                if mem2["u_id"] == user["u_id"]:
                    print("gets to second if statemtn")
                    result = True
    return result

def check_if_user_in_channel_owner(token, channel_id):
    user = token_check(token)
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['owner_members']:
                if mem["u_id"] == user["u_id"]:
                    result = True
    return result

def check_if_user_in_channel_owner_uid(u_id, channel_id):
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['owner_members']:
                if mem["u_id"] == u_id:
                    result = True
    return result

def check_if_user_in_channel_member_uid(u_id, channel_id):
    channel_store = get_channel_store()
    result = False
    for mem_check in channel_store["Channels"]:
        if mem_check['channel_id'] == channel_id:
            for mem in mem_check['all_members']:
                if mem["u_id"] == u_id:
                    result = True
    return result

def check_if_channel_is_public(channel_id):
    channel_store = get_channel_store()
    result = False
    for pub in channel_store['Channels']:
        if pub['channel_id'] == channel_id:
            if pub['is_public'] == True:
                result = True
    return result
