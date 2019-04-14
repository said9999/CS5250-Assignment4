import csv

def print_metrix(waiting_times, meta):
    #print(waiting_times)
    #print(meta)
    print(1.0*sum(waiting_times)/len(waiting_times))
 

class FCFS:
    
    def schedule(self, fname, inputs):
        f = open(fname + ".csv", 'w')
        csv_writer = csv.writer(f)
        waiting_times = []
        meta = []
        time = 0
        for i in inputs:
            time = max(time, i[1])
            print(i[0], max(time, i[1]), i[2])
            csv_writer.writerow([i[0], max(time, i[1]), i[2]])
            time += i[2]

            t = time - (i[3]+i[4])
            waiting_times.append(t)
            meta.append([i[0], t])

        print_metrix(waiting_times, meta)
        f.close()

class RR:
    def __init__(self, q):
        self._q = q
    
    # input (pid, arrive_time, burst_time, original_arrive_time, original_burst_time)
    def schedule(self, fname, inputs):
        self._active = []
        time = 0
        waiting_times = []
        meta = []
        
        f = open(fname + ".csv", 'w')
        csv_writer = csv.writer(f)
        while self._active or inputs:
            while True:
                if len(inputs) and inputs[0][1] <= time:
                    self._active.append(inputs.pop(0))
                else:
                    break
            
            if len(self._active) == 0:
                time += 1
                continue
        
            # process active queue
            job = self._active.pop(0)
            print(job[0], time, min(self._q, job[2]))
            csv_writer.writerow([job[0], time, min(self._q, job[2])])
            
            time += min(self._q, job[2])
            if job[2] > self._q:
                job[2] -= self._q
                while True:
                    if len(inputs) and inputs[0][1] <= time:
                        self._active.append(inputs.pop(0))
                    else:
                        break
                self._active.append(job)
            else:
                t = time-(job[3]+job[4])
                waiting_times.append(t)
                meta.append([job[0], t])
        
        print_metrix(waiting_times, meta)
        f.close()
        

from Queue import PriorityQueue

class SRTF:
    def schedule(self, fname, inputs):
        active = PriorityQueue()
        time = 0
        agg = []
        waiting_times = []
        meta = []
        f = open(fname + ".csv", 'w')
        csv_writer = csv.writer(f)
        while active.qsize() or inputs:
            if len(inputs) and inputs[0][1] <= time:
                job = inputs.pop(0)
                active.put((job[2], job))

            c_job = None
            if active.qsize() > 0:
                obj = active.get()
                p, job = obj
                
                p -= 1
                job[2] -= 1
                if p != 0:
                    active.put((p, job))
                else:
                    t = time+1-(job[3]+job[4])
                    waiting_times.append(t)
                    meta.append([job[0], t])
                
                c_job = job

            if c_job:
                if agg and agg[-1][0] == c_job[0]: # same task, extend it
                    agg[-1][2] += 1
                else:
                    agg.append([c_job[0], time, 1])
                    # print(job[0], time, 1)
                    
            time+=1
        
        for i in agg:
            csv_writer.writerow(i)
            print(i)
        
        print_metrix(waiting_times, meta)
        f.close()


class SJF:
    def __init__(self, alpha, default_time):
        self._alpha = alpha
        self._default_time = default_time


    def schedule(self, fname, inputs):
        active = PriorityQueue()
        time = 0
        prev_time = {}
        waiting_times = []
        meta = []
        f = open(fname + ".csv", 'w')
        csv_writer = csv.writer(f)
        while active.qsize() or inputs:
            while True:
                if len(inputs) and inputs[0][1] <= time:
                    job = inputs.pop(0)
                    t, d = prev_time.get(job[0], (0, self._default_time))
                    p = self._alpha * t + (1 - self._alpha) * d
                    active.put((p, job))
                else:
                    break

            if active.qsize() > 0:
                p, job = active.get()
                prev_time[job[0]] = (job[2], p)
                print(job[0], time, job[2])
                csv_writer.writerow([job[0], time, job[2]])
                time += job[2]

                t = time-(job[3]+job[4])
                waiting_times.append(t)
                meta.append([job[0], t])
            
            time+=1
        
        print_metrix(waiting_times, meta)
        f.close()


def get_input():
    inputs_number = []
    f = open('input.txt', 'r')
    inputs = f.read().split('\n')
    for i in inputs:
        a_str, b_str, c_str = i.split(' ')
        inputs_number.append([int(a_str), int(b_str), int(c_str), int(b_str), int(c_str)])
    
    return inputs_number

if __name__ == '__main__':
    print("using FCFS")
    c = FCFS()
    c.schedule("FCFS", get_input())

    print("using RR")
    c = RR(2)
    c.schedule("RR", get_input())

    print("using SRTF")
    c = SRTF()
    c.schedule("SRTF", get_input())

    print("using SJF")
    c = SJF(0.5, 5)
    c.schedule("SJF", get_input())