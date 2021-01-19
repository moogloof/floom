# Library imports
import socket


# Server details
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5999

# Send data to channel
def send_channel(ch, uid, sock, b):
	connected = ch[uid]

	for addr in connected:
		sock.sendto(b, addr)

# Server loop
if __name__ == "__main__":
	# Channels that users can connect to
	channels = {}

	# User connections
	connections = {}

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
			pack, addr = sock.recvfrom(1024)

			# Handle connection
			if pack[0] == 0:
				# Connect to channel
				# Channel id
				channel_id = pack[1:].decode()

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
			elif pack[0] == 1:
				# Leave channel
				try:
					channels[connections[addr]].remove(addr)
					del connections[addr]
				except ValueError:
					print("Invalid leave request from {}:{}".format(addr[0], addr[1]))
			elif pack[0] == 2:
				# Update video frame
				# Send to channel
				send_channel(channels, connections[addr], sock, pack[1:])
	except:
		pass

	# Close socket
	sock.close()

