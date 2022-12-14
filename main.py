from typing import MutableSequence
import cv2 as cv
import time
import numpy as np
from pynput.mouse import Button, Controller
from recognition import get_text
from click_pos import click_pos
from text_processing import text_processing
from windowcapture import Capture
from vision import Vision

screen1 = None

win1 = Capture('[BOT1]')
hideout_logo = Vision(screen1, 'hideout')    
net_error = Vision(screen1, 'error')
page_refresh = Vision(screen1, 'page_refresh')

mouse = Controller()

video_watching_time = 10 * 60
start_state = 0


# this is the main loop

while(True):
    
    #if it starts first time make 4 second delay
    if start_state == 0:
        time.sleep(4)
        start_state += 1
        
    #take screenshot && get win position
    screen1 = win1.get_screenshot()
    screen1_pos = win1.get_win_pos()

    #update screen for website logo, error state and whole window
    hideout_logo.window = screen1
    net_error.window = screen1
    page_refresh.window = screen1
           
    #connection error often occures when we lose internet for very short time
    #to avoid our bot being stopped by this 'fake' error we gonna check for it
    #in case error occures, we reload page, which usually helps
    if net_error.get_error_state() == 'true':
        print('CONNECTION ERROR, RELOADING')
        refresh_click_pos = click_pos(screen1_pos, page_refresh.get_object_pos())
        mouse.position = (refresh_click_pos[0], refresh_click_pos[1])
        mouse.click(Button.left)
        time.sleep(6)
        #print('refresh_click_pos', refresh_click_pos)
        #print('The current pointer position is {0}'.format(mouse.position))
    else:

        #by clicking on the website logo we get to the main menu
        #get window1 and center of hideout logo  and click on it
        logo_pos = hideout_logo.get_object_pos()
        logo_click_pos = click_pos(screen1_pos, logo_pos)
        mouse.position = (logo_click_pos[0], logo_click_pos[1])
        mouse.click(Button.left)
        print('going to main menu')
        time.sleep(5)
        text1_img = win1.get_text_part()[0]
        text2_img = win1.get_text_part()[1]
        #we want to watch as short video as possible, because for 30 sec video and for 1h video we get almost the same reward
        #we capture both videos length 
        text1 = get_text(text1_img)
        text2 = get_text(text2_img)
        #we decide which video to watch
        to_do = text_processing(text1, text2)[0]
        if text1 != 'error' and text2 != 'error':
            ts_error = 0
        else:
            ts_error = 1

        # if both videos are too long for us we scroll the page looking for another pair
        # if we scrolled 3 time, we reload page and search for new videos
        #at the same time always checking for connection error 
        count = 0
        if ts_error == 0:
            while to_do == 'skip':
                

                screen1 = win1.get_screenshot()
                screen1_pos = win1.get_win_pos()
                hideout_logo.window = screen1
                net_error.window = screen1
                page_refresh.window = screen1
                text1_img = win1.get_text_part()[0]
                text2_img = win1.get_text_part()[1]

                if count <= 2:
                    print('scrolling page')
                    logo_pos = hideout_logo.get_object_pos()
                    logo_click_pos = click_pos(screen1_pos, logo_pos)
                    mouse.position = (logo_click_pos[0], logo_click_pos[1] + 150)
                    mouse.scroll(0, -2.2)
                    count += 1
                    time.sleep(3)

                    screen1 = win1.get_screenshot()
                    screen1_pos = win1.get_win_pos()
                    text1_img = win1.get_text_part()[0]
                    text2_img = win1.get_text_part()[1]
                    text1 = get_text(text1_img)
                    text2 = get_text(text2_img)

                    to_do = text_processing(text1, text2)[0]

                    if to_do != 'skip':
                        break

                else:
                    print('scrolled 3 times, reloading')
                    logo_pos = hideout_logo.get_object_pos()
                    logo_click_pos = click_pos(screen1_pos, logo_pos)
                    mouse.position = (logo_click_pos[0], logo_click_pos[1])
                    mouse.click(Button.left)
                    count = 0
                    time.sleep(3)

                    screen1 = win1.get_screenshot()
                    screen1_pos = win1.get_win_pos()
                    hideout_logo.window = screen1
                    net_error.window = screen1
                    page_refresh.window = screen1

                    if net_error.get_error_state() == 'true':
                        print('CONNECTION ERROR, RELOADING')
                        refresh_click_pos = click_pos(screen1_pos, page_refresh.get_object_pos())
                        mouse.position = (refresh_click_pos[0], refresh_click_pos[1])
                        mouse.click(Button.left)
                        time.sleep(5)
                    if to_do != 'skip':
                        break
            #always update screen parts which are important to us
            screen1 = win1.get_screenshot()
            screen1_pos = win1.get_win_pos()
            hideout_logo.window = screen1
            net_error.window = screen1
            page_refresh.window = screen1
            text1_img = win1.get_text_part()[0]
            text2_img = win1.get_text_part()[1]

            #if we decided that the left video is short enough to watch, we watch it
            #after short videos usually shorts video play next, so we watch next videos for our 'watching time'
            #always check for connection error
            if to_do == 'text1':
                text1_pos = win1.get_text_part()[2], win1.get_text_part()[4]
                mouse.position = (text1_pos[0], text1_pos[1])
                mouse.click(Button.left)
                print('going to video, text1')
                timeout = time.time() + video_watching_time
                while time.time() < timeout:
                    screen1 = win1.get_screenshot()
                    net_error.window = screen1
                    if net_error.get_error_state() == 'true':
                        print('CONNECTION ERROR, RELOADING')
                        refresh_click_pos = click_pos(screen1_pos, page_refresh.get_object_pos())
                        mouse.position = (refresh_click_pos[0], refresh_click_pos[1])
                        mouse.click(Button.left)
                        time.sleep(5)
             #if we decided that the right video is short enough to watch, we watch it
            #after short videos usually shorts video play next, so we watch next videos for our 'watching time'
            #always check for connection error
            if to_do == 'text2':
                text2_pos = win1.get_text_part()[3], win1.get_text_part()[4]
                mouse.position = (text2_pos[0], text2_pos[1])
                mouse.click(Button.left)
                print('going to video, text2')
                timeout = time.time() + video_watching_time
                while time.time() < timeout:
                    screen1 = win1.get_screenshot()
                    net_error.window = screen1
                    if net_error.get_error_state() == 'true':
                        print('CONNECTION ERROR, RELOADING')
                        refresh_click_pos = click_pos(screen1_pos, page_refresh.get_object_pos())
                        mouse.position = (refresh_click_pos[0], refresh_click_pos[1])
                        mouse.click(Button.left)
                        time.sleep(5)
            
    '''#convert video for correct work of cv.cirlce
    screen1 = np.ascontiguousarray(screen1, dtype=np.uint8)
    #cv.circle(screen1, page_refresh.get_object_pos(), 5, (0, 0, 255), -4)
    print('text1', text1)
    print('text2', text2)
    print('to do: ', to_do)

    cv.imshow('BOT1', screen1)
    cv.imshow('text1', text1_img)
    cv.imshow('text2', text2_img)
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()'''
print('done')