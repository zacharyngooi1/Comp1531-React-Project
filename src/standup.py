from db import channel_check, get_channel_store, message_send_for_standup, get_standup_queue, member_channel_check, token_check
from datetime import datetime, timezone
import time
from error import InputError
from auth import auth_register
from channel import channels_create
from error import AccessError, InputError
from db import get_standup_queue
#This function is named standup_start because the standup/start wrapper will be placed around it.
#But really all this function does is return the time_finish and check of the token and channel_id are valid.
#"final_string":""
def standup_start(token, channel_id, length):
    """ This function begins a standup.

    Parameters:
        token (str): a token which identifies a session of a user
        channel_id (int): an integer which specifies the id of a channel
        length (int) : an integer which specifies the length of the standup

    Returns:
        {dictionary}: a dictionary containing a float with the time that the standup
        is going to finish at.
    
    """
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    current_moment_in_time = datetime.now()
    if channel['standup']['time_standup_finished'] != None:
        if current_moment_in_time.replace(tzinfo=timezone.utc).timestamp() < channel['standup']['time_standup_finished']:
            raise InputError
    get_standup_queue()['Standup_queues'].append({"final_string":""})
    channel['standup']['is_standup_active'] = True
    time_finish = length + current_moment_in_time.replace(tzinfo=timezone.utc).timestamp()
    channel['standup']['time_standup_finished'] = time_finish
    return {
        'time_finish' : time_finish #This is a unix timestamp
    }

def standup_active(token, channel_id):
    """ Returns whether a channel with channel_id is active and
    if so, what time the standup finishes

    Parameters:
        token (str): a token which identifies a session of a user
        channel_id (int): an integer which specifies the id of a channel
    
    Returns:
        (dictionary): a dictionary containing whether a standup is active and
        what time the standup finishes. If the standup is not active, this returns
        False and time finish as none.

    """

    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    current_moment_in_time = datetime.now()
    print("now:",current_moment_in_time.replace(tzinfo=timezone.utc).timestamp())
    print("then:",channel['standup']['time_standup_finished'])
    print('BEFORE THE IF STATEMENT ')
    if channel['standup']['time_standup_finished'] == None:
        return {
            'is_active' : False,
            'time_finish' : None
        }
    
    if current_moment_in_time.replace(tzinfo=timezone.utc).timestamp() < channel['standup']['time_standup_finished']:
        print('RETURN FALSE')        
        return {
            'is_active' : True,
            'time_finish' : channel['standup']['time_standup_finished']
        }
    print('RETURN TRUE')
    return {
        'is_active' : False,
        'time_finish' : None
    }
    

def standup_send(token, channel_id, message):
    """ Sending a single standup message
    
    Parameters:
        token (str): a token which identifies a session of a user
        channel_id (int): an integer which specifies the id of a channel
        message (str): A message given by a certain channel member during the standup
    
    Returns:
        (dictionary): An empty dictionary is returned.
    """
    channel_store = get_channel_store()
    channel = channel_check(channel_id)
    if channel == False:
        raise InputError
    if member_channel_check(token, channel_id) == False:
        raise AccessError
    if len(message) > 1000:
        raise InputError
    if standup_active(token,channel_id)['is_active'] == False:
        raise InputError
    user = token_check(token)
    if channel['standup']['time_standup_finished'] - datetime.now().replace(tzinfo=timezone.utc).timestamp() > 0:
        message_send_for_standup(user['u_id'], message)
    return {
    
    }

"""
input_dict = auth_register('hayden@gmail.com', 'password', 'hayden', 'smith')
print(get_channel_store())
chan_id = channels_create(input_dict['token'], 'Hayden', True)
print(standup_start(input_dict['token'], chan_id['channel_id'], 50))
print()
print("printing standup_active")
print(get_channel_store())
print(standup_active(input_dict['token'], chan_id['channel_id']))
print()
print(get_channel_store())
print()
standup_send(input_dict['token'], chan_id['channel_id'], "Hayden")
time.sleep(51)
standup_send(input_dict['token'], chan_id['channel_id'], "Smith")
standup_send(input_dict['token'], chan_id['channel_id'], "Rob")
standupqueue_store = get_standup_queue()
print(standupqueue_store)
"""
