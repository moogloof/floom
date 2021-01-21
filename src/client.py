# Library imports
import pyaudio
import socket
import sys
import threading


# Socket consts
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
CHANNEL_ID = sys.argv[3].encode()

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

try:
	# Connect to server and channel
	sock.sendto(b"\x00" + CHANNEL_ID, (SERVER_IP, SERVER_PORT))
	r, _ = sock.recvfrom(1024)

	# Start mic daemon
	mic_thread.start()

	if r == b"\x00":
		print("Successfully connected to server.")

		# Output data received from server
		while True:
			d, addr = sock.recvfrom(CHUNK)
			ostream.write(d)
	else:
		print("Could not connect to server.")
except KeyboardInterrupt:
	pass


# Leave from server
print("Disconnecting from channel...")
sock.sendto(b"\x01", (SERVER_IP, SERVER_PORT))

# Close streams
print("Terminating streams...")
istream.stop_stream()
ostream.stop_stream()
istream.close()
ostream.close()
audio.terminate()

# Close socket
print("Quitting client...")
sock.close()

