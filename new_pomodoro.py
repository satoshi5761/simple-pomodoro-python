import time
import os 
import random
import getpass

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # it removes pre hello message from pygame
from pygame import mixer # play music
from rich import print # modify output
from rich.panel import Panel # modify output
from rich.text import Text # modify output


TIME_MINUTES = 1 # default for study time
BREAK_MINUTES = 3 # default for break time
username = getpass.getuser()



def display_time(time_minutes, current_hour, total_hour, my_song=None, is_break_time=False):
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
			minutes_song_play, seconds_song_play = when_to_play_song(my_song)
			if minutes_digits == minutes_song_play and seconds_digits == seconds_song_play:
				my_song.play() # time is almost up but please enjoy the song
		

		print(f'{current_hour}/{total_hour}')

		minutes_digits, seconds_digits = countdown_time(minutes_digits, seconds_digits)

		# freeze the screen first then clear the terminal
		time.sleep(1)

		# portable based on operating system's terminal
		os.system('clear' if os.name == 'posix' else 'cls')


def countdown_time(minutes_digits, seconds_digits):
	"""
	update the remaining time

	parameters:
	- minutes_digits   (list of integers) : remaining minutes
	- seconds_digits   (list of integers) : remaining seconds

	return list(minutes_digits) and list(seconds_digits)
	------------------core of the problem-------------------
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


def random_song() -> str:
	"""
	get a random song
	from the musics directory
	return the name of the song
	"""
	playlist = os.listdir('musics') # get list of songs in musics directory
	pick_a_song = random.choice(playlist)

	return pick_a_song


def when_to_play_song(song) -> tuple[list[int], list[int]]:
	"""
	calculate precisely when is the right time to play the song 
	which is near the end of break time
	"""
	length_of_song = song.get_length() # in seconds
	minutes_song = int(length_of_song / 60)
	seconds_song = int(length_of_song - minutes_song * 60)
	return [0, minutes_song], [seconds_song // 10, seconds_song % 10] # ajaran Pak Yuan Lukito ternyata berguna


def choose_your_song():
	"""
	pick your song(s) to be played in the end of break time
	"""
	playlist = {idx: song for (idx, song) in enumerate(os.listdir("musics"), start=1)}
	for (idx, song) in playlist.items():
		print(f"[{idx}] {song}")
	
	while True:
		try:
			song = list(map(int, input("Choose your -song(s)- (0 for random): ").split()))
		except:
			print("Please input an integer(s)")
			continue
		else:
			if song == 0:
				return random_song()
			return [playlist[idx] for idx in song]

def get_study_time_finished(hours: int) -> None:
	"""
	calculate the finish time
	"""
	current_time = time.localtime()
	time_hour = current_time[3]
	time_minute = current_time[4]

	time_minute = time_minute + hours * BREAK_MINUTES * 2
	time_hour = time_hour + hours + time_minute // 60

	time_hour = time_hour % 24
	time_minute = time_minute % 60

	if time_hour < 10:
		time_hour = "0" + str(time_hour)
	if time_minute < 10:
		time_minute = "0" + str(time_minute)

	print(f"Your study will be finished at {time_hour}:{time_minute}")

mixer.init()
intro_song = mixer.Sound("musics1.1/intro.mp3")
break_song = mixer.Sound("musics1.1/break.mp3")
##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################
##############################################################################################################################################################

print(f'Hello {username.title()}')
print('\\-------------------------/')
print('|welcome to pomodoro timer|'.upper())
print('/-------------------------\\')


study = True
while study:

	my_song_list = choose_your_song()

	hours = input('how many hours would you like: ')
	while hours.isdigit() is False:
		print('input error, please use an integer.')
		hours = input('how many hours would you like: ')
	hours = int(hours)

	get_study_time_finished(hours)
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
	intro_song.play()


	total_hour = hours
	current_hour = 0 
	for i in range(hours * 2):
		# study time
		display_time(TIME_MINUTES, current_hour, total_hour)


		# break time
		break_song.play()
		my_song = mixer.Sound(f"musics/{my_song_list[i % len(my_song_list)]}")
		print(my_song)
		time.sleep(0.3)
		display_time(BREAK_MINUTES, current_hour, total_hour, my_song, is_break_time=True)


		# increment hour
		current_hour = current_hour + 0.5


	print('Congratulations!!!, you have completed the study hours')
	prompt = input('would you like to study more? (y/n) ').lower()


	if prompt.startswith("n"):
		study = False

