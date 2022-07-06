import numpy as np

class ThreshClassifier:

    # 3
    def __init__(self):
        self.LP_history = [0, 0]
        self.LP_counter = 0
        self.flag_v_pd = 0
        self.flag_v_lp = 0
        self.last_spike_lp_t = 0
        self.ignore_lp = False
        self.last_lp_isi_t = np.inf





    def classify(self, dataExtra, dataPD, thresholdLP, thresholdPD, thresholdPDLow):
        self.state = 'undef'
        self.LP_counter += 1

        #print("LP %f PD %f"%(dataExtra, dataPD))
        #print("Thresh LP %f PD %f PDlow %f"%(thresholdLP, thresholdPD, thresholdPDLow))


        if (dataPD >= thresholdPD and self.flag_v_pd == 1):
            # PD burst starts
            self.flag_v_pd = 0
            self.state = 'PD_start'
            #print("PD_start")

            # LP burst ends (extracellular)
            #self.flag_v_lp = 1

        elif(dataPD >= thresholdPD):
            # New spike of ongoing PD burst
            self.state = 'PD_spike'
            #print("PD_spike")

        elif (dataPD < thresholdPDLow and self.flag_v_pd == 0):
            # PD burst ends
            self.flag_v_pd = 1
            self.flag_v_lp = 1
            #print("PD_end")



        if (self.LP_history[-1] >= thresholdLP and self.flag_v_lp == 1):
            if (self.LP_counter > 2) and (dataExtra < self.LP_history[-1]) and (self.LP_history[-1] > self.LP_history[-2]):
                # LP burst starts
                self.flag_v_lp = 0
                self.state = 'LP_start'
                self.LP_counter = 0
                self.LP_history = [0, 0]
                self.last_spike_lp_t = 0
                self.ignore_lp = False
                self.last_lp_isi_t = np.inf
                #print("LP_start")

        elif (self.LP_history[-1] >= thresholdLP) and self.ignore_lp==False:
            #print("Counter %d Last %d diff %d ISI %f"%(self.LP_counter, self.last_spike_lp_t, self.LP_counter - self.last_spike_lp_t, self.last_lp_isi_t))
            #print("-2 %f\t1 %f\t0 %.2f"%(self.LP_history[-2], self.LP_history[-1], dataExtra))
            if (self.LP_counter - self.last_spike_lp_t) > 3*self.last_lp_isi_t:
                # Ignore isolated spikes (possible artifacts)
                self.ignore_lp = True

            elif (self.LP_counter > 2) and (dataExtra < self.LP_history[-1]) and (self.LP_history[-1] > self.LP_history[-2]):
                self.last_lp_isi_t = self.LP_counter - self.last_spike_lp_t
                #print(self.last_spike_lp_t)

                self.last_spike_lp_t = self.LP_counter-1

                # New spike of ongoing LP burst
                self.state = 'LP_spike'
                #print("LP_spike")


        # Update LP history
        self.LP_history[-2] = self.LP_history[-1]
        self.LP_history[-1] = dataExtra

        #if self.state == "undef":
        #    print("undef")

        return self.state





            