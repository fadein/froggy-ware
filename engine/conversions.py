def minutes_to_ms(time_input):

	print(f"TIME INPUT IS {time_input}")
	break_point = time_input.index(":")

	mins = time_input[0:break_point]

	seconds =  time_input[(break_point+1):]
	
	if ":" in seconds:
		# if the song length pulled is in the hour limit (which is unlikely), seconds will 
		# contain a seconds ":" in the formatting. This must be broken up further 		

		hours = int(mins)
		new_break_point = seconds.index(":")
		
		mins = int(seconds[0:new_break_point])

		seconds = int(seconds[(new_break_point+1):])
		
		ms_time = (hours * 3600000) + (mins * 60000) + (seconds * 1000)
	else:
		ms_time = (int(mins) * 60000) + (int(seconds) * 1000)

	return ms_time

def ms_to_min(time_ms):
	mins = time_ms / 60000

	string_min = str(mins)
	
	decimal =  (string_min.index("."))

	seconds  = int((float(string_min[decimal:]))*60)

	minutes = int(string_min[0:decimal])

	returnString = f"{minutes}:{seconds}"

	return returnString
