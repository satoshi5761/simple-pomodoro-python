import time
import os 
import random
import getpass

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # it removes pre hello message from pygame
from pygame import mixer # play music
mixer.init()
from rich import print # modify output
from rich.panel import Panel # modify output
from rich.text import Text # modify output


username = getpass.getuser()


def countdown_time(minutes_digits, seconds_digits):
	"""
	update the remaining time

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


def display_time(time_minutes, current_hour, total_hour, is_break_time=False, name_song=None):
	"""
	displays the remaining time 
	
	parameters:
	- time_minutes   (int) : the total time in minutes
	- current_hour	 (int) : current_hour
	- total_hour     (int) : total hour
	- is break time  (boolean) : determine if it is study time or break time

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
			if minutes_digits == [0, 0] and seconds_digits == [1, 7]:
				play_break_song() # time is almost up
		

		print(f'{current_hour}/{total_hour}')

		minutes_digits, seconds_digits = countdown_time(minutes_digits, seconds_digits)

		# freeze the screen first then clear the terminal
		time.sleep(1)

		# portable based on operating system's terminal
		os.system('clear' if os.name == 'posix' else 'cls')

	if is_break_time:
		play_break_finished() # break time done

def play_song():
	"""
	play a random song
	from the musics directory

	return the name of the song
	"""
	playlist = os.listdir('musics') # get list of songs in musics directory
	pick_a_song = random.choice(playlist)


	# execute the song
	mixer.music.load(f'musics/{pick_a_song}')
	mixer.music.play(loops=-1) # unlimited loop

	return pick_a_song

def play_intro_song():
	intro_song = mixer.Sound("musics1.1/intro.mp3")
	intro_song.play()

def play_break_song():
	break_song = mixer.Sound("musics1.1/break.mp3")
	break_song.play()

def play_break_finished():
	break_finished_song = mixer.Sound("musics1.1/break_finished.mp3")
	break_finished_song.play()


#############################################################
#############################################################
#############################################################

print(f'Hello {username.title()}')
print('\\-------------------------/')
print('|welcome to pomodoro timer|'.upper())
print('/-------------------------\\')


study = True
while study:


	hours = input('how many hours would you like: ')
	while hours.isdigit() is False:
		print('input error, please use an integer.')
		hours = input('how many hours would you like: ')
	hours = int(hours)


	# calculate finish time
	current_time = time.localtime()
	tm_hour = current_time[3]
	tm_minute = current_time[4]

	tm_minute = tm_minute + hours * 2 * 5
	tm_hour = tm_hour + hours + tm_minute // 60 # will be screwed if I study at hour 20 and up
	tm_minute = tm_minute % 60

	if tm_minute < 10:
		tm_minute = "0" + str(tm_minute)
	print(f"Your study will be finished at {tm_hour}:{tm_minute}")
	time.sleep(1.5)

	print()


	print('very well')
	print('your timer will start in ...')
	time.sleep(1)
	print(3)
	time.sleep(1)
	print(2)
	time.sleep(1)
	print(1)
	time.sleep(1)
	play_intro_song()


	total_hour = hours
	current_hour = 0
	for _ in range(hours * 2):
		# study time
		time_minutes = 30 # default
		display_time(time_minutes, current_hour, total_hour, is_break_time=False, name_song=None)


		# break time
		play_break_song()
		time.sleep(0.3)
		display_time(time_minutes=5, current_hour=current_hour, total_hour=total_hour, is_break_time=True, name_song=None)


		# increment hour
		current_hour = current_hour + 0.5


	print('Congratulations!!!, you have completed the study hours')
	prompt = input('would you like to study more? (y/n) ').lower()


	if prompt.startswith("n"):
		study = False

