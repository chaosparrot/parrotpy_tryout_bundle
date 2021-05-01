from lib.modes.base_mode import *
import pyautogui
import time
import random

POWER_SCALING = 1000
SCROLLING_GRACE_PERIOD_IN_SECONDS = 5

from sys import platform
IS_LINUX = platform == "linux" or platform == "linux2"
SCROLL_SCALING = 20 if not IS_LINUX else 0.5

class StarterMode(BaseMode):
    momentum = 0
    scroll_direction = 1
    expand_timestamp = 0

    patterns = [
        {
            'name': 'left_click',
            'sounds': ['click_alveolar'],
            'threshold': {
                'percentage': 60,
                'power': 40 * POWER_SCALING,
                'times': 2,
            },
            'throttle': {
                'left_click': 0.13
            }
        },
        {
            'name': 'right_click',
            'sounds': ['click_lateral'],
            'threshold': {
                'percentage': 85,
                'power': 70 * POWER_SCALING,
                'times': 2,
            },
            'throttle': {
                'right_click': 0.15
            }
        },
        {
            'name': 'terminator_noise',
            'sounds': ['click_palatal'],
            'threshold': {
                'percentage': 83,
                'power': 100 * POWER_SCALING,
                'times': 2
            },
            'throttle': {
                'terminator_noise': 0.15
            }
        },
        {
            'name': 'scroll_up',
            'sounds': ['fricative_f'],
            'threshold': {
                'percentage': 75,
                'power': 10 * POWER_SCALING,
            },
            'throttle': {
                'right_click': 0.15,
                'terminator_noise': 0.05,
                'scroll_down': 0.15
            }
        },
        {
            'name': 'scroll_down',
            'sounds': ['sibilant_sh', 'sibilant_ch'],
            'threshold': {
                'percentage': 70,
                'power': 10 * POWER_SCALING,
            },
            'throttle': {
                'terminator_noise': 0.05
            }
        },
        {
            'name': 'background_sounds',
            'sounds': ['background_noise_keyboard', 'background_noise_mouse'],
            'threshold': {
                'percentage': 90
            },
            'throttle': {
                'left_click': 0.1,
                'right_click': 0.1
            }
        }
    ]
    
    def start( self ):
        self.enable('expanded_set')
        
    def handle_sounds( self, dataDicts ):
        self.momentum = self.momentum * 0.9759
        if (self.momentum < 0.01):
            self.momentum = 0
        
    	# Throttle sounds that might trigger from things like typing or mouse usage
        self.detect('background_sounds')
    
        timestamp = time.time()
        if (self.detect('terminator_noise')):
        
            # Time out scrolling when we are making the palatal click sound
            if (self.momentum != 0):
                self.momentum = 0
                self.expand_timestamp = timestamp
            else:
                self.expand_timestamp = timestamp + SCROLLING_GRACE_PERIOD_IN_SECONDS if (self.expand_timestamp == 0 or self.momentum == 0 or self.expand_timestamp < timestamp) else timestamp
            
        if (self.detect('left_click')):
            # Stop the scrolling on click
            if (self.momentum > 0 ):
                self.momentum = 0
            else:
                self.leftclick()
        elif (self.detect('right_click')):
            if (self.momentum > 0 ):
                self.momentum = 0
            else:
                self.rightclick()
            
        # Only activated if the terminator noise has been uttered
        if (self.expand_timestamp > timestamp):
            if (self.detect('scroll_down')):
                self.calculate_momentum(dataDicts[-1]['silence']['power'], -1)
                self.expand_timestamp = timestamp + 5
            elif (self.detect('scroll_up')):
                self.calculate_momentum(dataDicts[-1]['silence']['power'], 1)
                self.expand_timestamp = timestamp + 5

        if(self.momentum > 0):
            scroll = 0.025 * SCROLL_SCALING * self.momentum

            # When the scrolling is below a threshold, just stop the momentum
            # To decrease the odds of the users counter scrolls being stopped by the scrolling still being invisibly active
            if (scroll < 0.3 ):
                self.momentum = 0
            # Scroll scaling in Xorg seems to be a bit iffy
            # So instead simulate sort of smooth scrolling by random chance ( This still feels off, but it's better than the sudden halt )
            if (scroll < 1 and IS_LINUX):
            	scroll = 1 if random.uniform(0, 1) < scroll else 0

            pyautogui.scroll(int(scroll * self.scroll_direction))
            
    def calculate_momentum(self, power, direction):
        if (direction != self.scroll_direction):
            self.scroll_direction = direction
            self.momentum = 0
    
        new_momentum = power / (POWER_SCALING * 0.7)
        self.momentum = new_momentum if new_momentum > self.momentum else self.momentum
