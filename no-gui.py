from datetime import datetime
import sched
import time
import parserc
import dateparser
import simpleaudio as sa
import pystray
import sys
import PIL.Image



image = PIL.Image.open('icon.png')

def close_app():
    icon.stop()
    event_schedule.cancel(event_schedule.queue[0])
    print(event_schedule.queue)


def stop_adthan(dell):
    play_obj.stop()

icon = pystray.Icon('SleekAdthan', image, menu=pystray.Menu(
    pystray.MenuItem("Stop Adthan", lambda:stop_adthan(False)),
    pystray.MenuItem("Exit", close_app)
))

event_schedule = sched.scheduler(time.time, time.sleep)



city = "Toronto"

#setup prayer times

def get_new_times():
    global r
    r = parserc.prayer(city)
    del r['today']['Sunrise']




icon.run_detached()



def time_check():
    event_schedule.enter(60, 1, time_check)
    if dateparser.parse(r['date'],languages=['en'],settings={'DATE_ORDER': 'DMY'}).date() == datetime.today().date():
        print(r['today'])
        for prayer,times in r['today'].items():
            print(datetime.now().strftime("%H:%M"), times)
            if datetime.now().strftime("%H:%M") == times:
                wave_obj = sa.WaveObject.from_wave_file("Abdul-Basit.wav")
                global play_obj
                play_obj = wave_obj.play()
                icon.notify(
                    f"Salam, It is {prayer} time",
                    ''
                )
                print('done')
    else:
        get_new_times()




get_new_times()
time_check()

event_schedule.run()