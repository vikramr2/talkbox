import mido

ports = mido.get_input_names()
print(ports)

port_name = ports[1]
port = mido.open_input(port_name)

while True:
    for message in port.iter_pending():
        print(message)