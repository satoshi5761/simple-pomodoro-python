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


def countdown_time(minutes_digits, seconds_digits):
	"""
	displays the remaining time

	parameters:
	- minutes_digits   (list of integers) : remaining minutes
	- seconds_digits   (list of integers) : remaining seconds

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


	remaining_time = Panel(Text(f'{tens_minute}{ones_minute}:{tens_second}{ones_second}', justify="center"))
	print(remaining_time)


	# applying changes made
	minutes_digits[0], minutes_digits[1] = tens_minute, ones_minute
	seconds_digits[0], seconds_digits[1] = tens_second, ones_second


	return minutes_digits, seconds_digits


def display_time(time_minutes, current_session, total_session, is_break_time=False, name_song=None):
	"""
	displays the remaining time 
	
	parameters:
	- time_minutes       (int) : the total time in minutes
	- current_session	 (int) : current_session
	- total_session      (int) : total session
	- is break time      (boolean) : determine if it is study time or break time

	stop when the time is completed
	"""

	# using lists to store values
	minutes_digits = list(map(int, str(time_minutes)))
	seconds_digits = [0, 0] 

	# case example
	# >> 30:00 >> 25:59 >> 25:58 >> ... >> 25:10 >> 25:09
	# >> 25:00 >> 24:50 >> 24:58 >> ... >> 24:10 >> 24:09
	# >> 15:00 >> 14:59 >> 14:58 >> ... >> 10:01 >> 01:01

	# handling special cases
	if time_minutes < 10:
		minutes_digits.insert(0, 0)


	while minutes_digits != [0, 0] or seconds_digits != [0, 0]:
		if is_break_time:
			print(f'now playing : {name_song}')

		print(f'{current_session}/{total_session}')

		minutes_digits, seconds_digits = countdown_time(
			minutes_digits, seconds_digits, current_session, total_session)

		# freeze the screen first then clear the terminal
		time.sleep(1)

		# portable based on operating system's terminal
		os.system('clear' if os.name == 'posix' else 'cls')



def play_song():
	"""
	play a random song
	from the musics directory

	return the name of the song
	"""
	playlist = os.listdir('musics') # get list of songs in musics directory
	pick_a_song = random.choice(playlist)


	# execute the song
	mixer.init()
	mixer.music.load(f'musics/{pick_a_song}')
	mixer.music.play(loops=-1) # unlimited loop


	return pick_a_song



#############################################################
#############################################################
#############################################################

print(f'Hello {username.title()}')
print('\\-------------------------/')
print('|welcome to pomodoro timer|'.upper())
print('/-------------------------\\')


study = True
while study:


	sessions = input('enter the number of sessions: ')
	while sessions.isdigit() is False:
		print('input error, please use an integer.')
		sessions = input('enter the number of sessions ')
	sessions = int(sessions)


	print()


	while True:
		time_minutes = input('enter the number of study time (in minutes): ')
		if time_minutes.isdigit() is False:
			print('input error, please use an integer.')
			continue
		if int(time_minutes) > 90:
			print('don\'t get ahead of yourself!')
			continue
		break
	time_minutes = int(time_minutes)


	print()


	print('very well')
	print('your timer will start in ...')
	time.sleep(1)
	print(3)
	time.sleep(1)
	print(2)
	time.sleep(1)
	print(1)


	total_session = sessions
	for current_session in range(1, sessions + 1):
		# study time
		display_time(time_minutes, current_session, total_session, is_break_time=False, name_song=None)


		# break time
		name_song = play_song()
		display_time(time_minutes=5, current_session=current_session, total_session=total_session, is_break_time=True, name_song=name_song)

		mixer.music.stop()
		mixer.music.unload()


	print('Congrulations!!!, you have completed the study sessions')
	prompt = input('would you like to study more? (y/n) ').lower()


	if prompt == 'n':
		print('do enjoy your remaining time')
		study = False

