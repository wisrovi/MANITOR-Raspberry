from Util.Util import Util

util = Util()
util.enviar_mqtt(uuid="1234567890abcdefghijklmnoprstuvwxyz")


print( util.read_data_scan_beacon() )