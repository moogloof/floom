# Library imports
import pyaudio
import socket
import sys
import threading


# Socket consts
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

# Audio consts
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Mic input daemon
def mic_input(sock, istream):
	try:
		while True:
			d = istream.read(CHUNK)
			sock.sendto(b"\x02" + d, (SERVER_IP, SERVER_PORT))
	except OSError:
		pass
	else:
		sys.exit(-1)

# Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Pyaudio stream
audio = pyaudio.PyAudio()
istream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
ostream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Mic input thread
mic_thread = threading.Thread(target=mic_input, args=(sock, istream))
mic_thread.daemon = True
mic_thread.start()

try:
	# Connect to server
	sock.sendto(b"\x00\x69", (SERVER_IP, SERVER_PORT))
	sock.recvfrom(1024)

	# Output data received from server
	while True:
		d, addr = sock.recvfrom(CHUNK)
		ostream.write(d)
except KeyboardInterrupt:
	pass


# Leave from server
sock.sendto(b"\x01", (SERVER_IP, SERVER_PORT))

# Close streams
istream.stop_stream()
ostream.stop_stream()
istream.close()
ostream.close()
audio.terminate()

# Close socket
sock.close()

