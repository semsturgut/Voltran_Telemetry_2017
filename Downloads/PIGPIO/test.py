import pigpio

pigpio.start()

for g in range (0,32):
	print("gpio {} is {}".format(g, pigpio.read(g)))

pigpio.stop()
