# Library imports
import socket
import sys
import threading


# Server details
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5999

if len(sys.argv) == 3:
	SERVER_IP = sys.argv[1]
	SERVER_PORT = int(sys.argv[2])
else:
	print("Using default server address")


# Channels that users can connect to
channels = {}

# User connections
connections = {}


# Send data to channel
def send_channel(ch, uid, sock, b):
	connected = ch[uid]

	for addr in connected:
		sock.sendto(b, addr)

# Packet handler
def handler(pack, addr, sock):
	# Handle connection
	if pack[0] == 0:
		# Connect to channel
		# Channel id
		channel_id = pack[1:]

		if channel_id in channels.keys():
			# Connect to existing channel
			channels[channel_id].append(addr)
		else:
			# Create new channel
			channels[channel_id] = [addr]

		# Add connection
		connections[addr] = channel_id

		# Verify connect packet
		sock.sendto(b"\x00", addr)

		print("User {}:{} joined on {}".format(addr[0], addr[1], channel_id))
	elif pack[0] == 1:
		# Leave channel
		try:
			channels[connections[addr]].remove(addr)
			del connections[addr]

			print("User {}:{} left.".format(addr[0], addr[1]))
		except ValueError:
			print("Invalid leave request from {}:{}".format(addr[0], addr[1]))
	elif pack[0] == 2:
		# Update video frame
		# Send to channel
		send_channel(channels, connections[addr], sock, pack[1:])


# Server loop
if __name__ == "__main__":
	# Startup server
	print("Starting up server...")
	# Open UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((SERVER_IP, SERVER_PORT))

	print("Opened at {} on port {}".format(SERVER_IP, SERVER_PORT))

	# Server loop
	try:
		while True:
			# Recv packet
			pack, addr = sock.recvfrom(1025)

			# Run handler thread
			handler_thread = threading.Thread(target=handler, args=(pack, addr, sock))
			handler_thread.daemon = True
			handler_thread.start()
	except KeyboardInterrupt:
		pass

	print("Shutting down...")

	# Close socket
	sock.close()

