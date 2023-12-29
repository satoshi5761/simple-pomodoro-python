import time
import os 
import random
import getpass

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # i don't know how this works but it removes pre hello message from pygame
from pygame import mixer # play music
from rich import print # modify output
from rich.panel import Panel # modify output
from rich.text import Text # modify output


username = getpass.getuser()


def countdown_time(minutes_digits, seconds_digits, current_session, total_session):
	"""
	displays the remaining time

	parameters:
	- minutes_digits   (list of integers) : remaining minutes
	- seconds_digits   (list of integers) : remaining seconds
	- current_session  (int)			  : current session
	- total_session    (int)			  : total session

	return list(minutes_digits) and list(seconds_digits)
	------------------core of the problems-------------------
	"""
	tens_minute = minutes_digits[0]
	ones_minute = minutes_digits[1]

	tens_second = seconds_digits[0]
	ones_second = seconds_digits[1]


	if seconds_digits == [0, 0]:
		tens_second, ones_second = 5, 9
		if ones_minute == 0:
			ones_minute = 9
			tens_minute = tens_minute - 1
		else:
			ones_minute = ones_minute - 1
	elif ones_second == 0:
		tens_second = tens_second - 1
		ones_second = 9
	else:
		ones_second = ones_second - 1


	print(f'{current_session}/{total_session}')
	remaining_time = Panel(Text(f'{tens_minute}{ones_minute}:{tens_second}{ones_second}', justify="center"))
	print(remaining_time)


	time.sleep(1)
	os.system('clear')


	# applying changes made
	minutes_digits[0], minutes_digits[1] = tens_minute, ones_minute
	seconds_digits[0], seconds_digits[1] = tens_second, ones_second


	return minutes_digits, seconds_digits


def record_study_time(study_time_minutes, current_session, total_session):
	"""
	records the study time 
	
	parameters:
	- study_time_minutes (int) : the total study time in minutes
	- current_session	 (int) : current_session
	- total_session      (int) : total session

	stop when the time is completed
	"""

	# using lists to store values
	minutes_digits = list(map(int, str(study_time_minutes)))
	seconds_digits = [0, 0] 

	# case example
	# >> 30:00 >> 25:59 >> 25:58 >> ... >> 25:10 >> 25:09
	# >> 25:00 >> 24:50 >> 24:58 >> ... >> 24:10 >> 24:09
	# >> 15:00 >> 14:59 >> 14:58 >> ... >> 10:01 >> 01:01

	# handling special cases
	if study_time_minutes < 10:
		minutes_digits.insert(0, 0)


	while minutes_digits != [0, 0] or seconds_digits != [0, 0]:
		minutes_digits, seconds_digits = countdown_time(
			minutes_digits, seconds_digits, current_session, total_session)
		

def record_break_time(current_session, total_session, break_time_minutes=5): # break_time_minutes is last because of default argument
	"""
	records the break time
	play song while in break

	parameters:
	- break_time_minutes (int) : the total break time in minutes
	- current_session	 (int) : current session
	- total_session      (int) : total session

	stop when the time is completed
	"""

	# using lists to store values
	minutes_digits = list(map(int, str(break_time_minutes)))
	seconds_digits = [0, 0]

	if break_time_minutes < 10:
		minutes_digits.insert(0, 0)


	play_song()
	while minutes_digits != [0, 0] or seconds_digits != [0, 0]:
		print(f'do enjoy your time {username}')
		minutes_digits, seconds_digits = countdown_time(
			minutes_digits, seconds_digits, current_session, total_session)


	mixer.music.stop()
	mixer.music.unload()


def play_song():
	"""
	play a random song
	from the musics directory
	"""
	playlist = os.listdir('musics') # get list of songs in musics directory
	pick_a_song = random.choice(playlist)


	# execute the song
	mixer.init()
	mixer.music.load(f'musics/{pick_a_song}')
	mixer.music.play(loops=-1) # unlimited loop




#############################################################
#############################################################
#############################################################


print('\\-------------------------/')
print('|welcome to pomodoro timer|'.upper())
print('/-------------------------\\')


study = True
while study:


	sessions = input('how many sessions would you like? ')
	while sessions.isdigit() is False:
		print('input error, please use an integer.')
		sessions = input('how many sessions would you like? ')
	sessions = int(sessions)


	print()


	while True:
		study_time_minutes = input('how many minutes your study time will be? ')
		if study_time_minutes.isdigit() is False:
			print('input error, please use an integer.')
			continue
		if int(study_time_minutes) > 90:
			print('don\'t get ahead of yourself!')
			continue
		break
	study_time_minutes = int(study_time_minutes)


	print()


	print('very well, your wish shall be granted')
	time.sleep(1.5)


	print('timer will start in')
	time.sleep(1)
	print(3)
	time.sleep(1)
	print(2)
	time.sleep(1)
	print(1)


	total_session = sessions
	for current_session in range(1, sessions + 1):
		record_study_time(study_time_minutes, current_session, total_session)
		record_break_time(current_session, total_session) # default break time is 5 minutes by default, it actually can be customized but meh 5 is good enough for me


	print('Congrulations!!!, you have completed the study sessions')
	prompt = input('would you like to study more? (y/n) ').lower()


	if prompt == 'n':
		print('do enjoy your remaining time')
		study = False

