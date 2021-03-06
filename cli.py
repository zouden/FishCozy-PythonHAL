from FishCozyHAL import FishCozyHAL
import kbhit
import sys, os, time
if len(sys.argv)<2:
    print("Usage: cli.py serial_port\nSerial_port can be 'auto', or 'false' for a simulation")
    sys.exit()
port = sys.argv[1]
if port == 'auto': port = None
if port == 'false': port = False 
commands = ['qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn']
# each group of letters corresponds to a chamber
# and each of the 3 letters corresponds to a temperature
preset_temperatures = 37, 28, 4


kb = kbhit.KBHit()

try:
    board = FishCozyHAL.Mainboard(port=port)
    board.connect()

    while True:
        try:
            board.refresh()
            print(board.chambers)
            # time.sleep(0.1)
        except TimeoutError:
            print("Timeout")
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27:  # ESC
                raise KeyboardInterrupt
            if ord(c) > 0:
                ## Set temperatures for the 6 chambers based on 3 pre-set points
                for idx, codes in enumerate(commands):
                    if c in codes:
                        temp = preset_temperatures[codes.index(c)]
                        board.chambers[idx].setpoint = temp



        
except KeyboardInterrupt:
    print('Interrupted, closing connection')
    board.disconnect()
    kb.set_normal_term()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
