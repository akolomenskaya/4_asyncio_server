import asyncio
async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

try:
	port=int(input("Введите порт:"))
	if not 0 <= port <= 65535:
		raise ValueError
except ValueError:
		port = 9090

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', port , loop=loop)
server = loop.run_until_complete(coro)


print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass


server.close()
loop.run_until_complete(server.wait_closed())
loop.close()