# floom
A UDP voice chat thing. You can connect to specific channels and talk.

### Run Server
Basically do the following to start a server at an IP or PORT.
```sh
cd path/to/repository
python src/server.py <IP|127.0.0.1> <PORT|5999>
```

### Run Client
Basically do the following to run a client. The `CHANNEL_ID` can be any channel.
```sh
cd path/to/repository
python src/client.py <IP> <PORT> <CHANNEL_ID>
```

### Server Packet Types
#### Join Packet
| Type | Name | Value |
| - | - | - |
| byte | Packet ID | 0x00 |
| str | Channel ID | A channel ID string of any length. |
#### Leave Packet
| Type | Name | Value |
| - | - | - |
| byte | Packet ID | 0x01 |
#### Audio Input Packet
| Type | Name | Value |
| - | - | - |
| byte | Packet ID | 0x02 |
| bytes | Audio Chunk | Audio chunk bytes of any length |
