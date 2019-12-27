from model.accessory.mq import *
import sys, time

class MQ2():

    def __init__(self):
        pass

    def get_data(self):

        try:
            mq = MQ()
            perc = mq.MQPercentage()

            return True, {
                'LPG'   : perc["GAS_LPG"] * 1000,
                'CO'    : perc["CO"] * 1000,
                'Smoke' : perc["SMOKE"] * 1000
            }

        except:
            return False, {
                'LPG'   : None,
                'CO'    : None,
                'Smoke' : None
            }
