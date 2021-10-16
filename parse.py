# simply run this in parsec's main dir: C:\ProgramData\Parsec


import time
import socket
import threading

# this snippet is from https://www.beardmonkey.eu/tplink/hs110/2017/11/21/collect-and-store-realtime-data-from-the-tp-link-hs110.html
def store_metrics(statDict):
    current_time = time.time()
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_sock.connect(("192.168.1.198", 2003))
        tcp_sock.send("parsec.collin.avgFPS {0} {1} \n".format(statDict["avgFPS"], current_time).encode())
        tcp_sock.send("parsec.collin.maxFPS {0} {1} \n".format(statDict["maxFPS"], current_time).encode())
        tcp_sock.send("parsec.collin.avgLatency {0} {1} \n".format(statDict["avgLatency"], current_time).encode())
        tcp_sock.send("parsec.collin.maxLatency {0} {1} \n".format(statDict["maxLatency"], current_time).encode())
        tcp_sock.send("parsec.collin.currentBitrate {0} {1} \n".format(statDict["currentBitrate"], current_time).encode())
        tcp_sock.send("parsec.collin.maxBitrate {0} {1} \n".format(statDict["maxBitrate"], current_time).encode())
        tcp_sock.send("parsec.collin.slowReTrans {0} {1} \n".format(statDict["slowReTrans"], current_time).encode())
        tcp_sock.send("parsec.collin.fastReTrans {0} {1} \n".format(statDict["fastReTrans"], current_time).encode())
        tcp_sock.send("parsec.collin.numCongestion {0} {1} \n".format(statDict["numCongestion"], current_time).encode())
    finally:
        tcp_sock.close()

def storeDebug(statDict):
  for item in statDict:
    print(statDict[item])

def run():
  threading.Timer(5.0, run).start()
  statDict = {
      'avgFPS': 0,
      'maxFPS': 0,
      'avgLatency': 0,
      'maxLatency': 0,
      'currentBitrate': 0,
      'maxBitrate': 0,
      'slowReTrans': 0,
      'fastReTrans': 0,
      'numCongestion': 0
    }

  with open('log.txt', 'r') as f:
    lastLine = ''
    categoryList = []
    lines = f.readlines()
    # strip() removes trailing \n char
    lastLine = lines[-1].strip()
    # gets the useful stats
    categoryList = lastLine.split()
    for i in range(0, len(categoryList)-1):
      stats = categoryList[i] 
      if ',' in stats:
        categoryList[i] = categoryList[i].replace(',', '')
    print(lastLine)
    # if not connected, set value to 0
    if("disconnected" in lastLine):
      store_metrics(statDict)
      #storeDebug(statDict)
      return
    # separated into its categories
    fps = categoryList[4]
    latency = categoryList[5]
    bitrate = categoryList[6]
    network = categoryList[7]
    print(fps, latency, bitrate, network)

    # refer to https://support.parsec.app/hc/en-us/articles/115002875791-Interpreting-The-Parsec-Console-Outputs
    # format: latency(ms) in last 100 frames
    # 
    # FPS: [avg]/[max] 
    # L: [avg]/[max]
    # B: [current]/[max]
    # N: [slowReTrans]/[fastReTrans]/[numCongestion]
    # 
    # Note that the maximum frametime for 60FPS is 16.67ms
    # Anything >16.67ms or higher will cause stuttering among other issues (1000ms/60fps = 16.67ms)
    # Network should ideally be close to 0

    # this can be more efficient by making avgFPS, maxFPS, etc into a list then
    # using a for loop to find the right indexes but fk it
    statDict = {
      'avgFPS': fps[fps.index(':')+1:fps.index('/')],
      'maxFPS': fps[fps.index('/')+1:],
      'avgLatency': latency[latency.index(':')+1:latency.index('/')],
      'maxLatency': latency[latency.index('/')+1:],
      'currentBitrate': bitrate[bitrate.index(':')+1:bitrate.index('/')],
      'maxBitrate': bitrate[bitrate.index('/')+1:],
      'slowReTrans': network[network.index(':')+1:network.index('/')],
      'fastReTrans': network[network.index('/')+1:network.index('/', network.index('/')+1)],
      'numCongestion': network[network.index('/', network.index('/')+1)+1:]
    }
    store_metrics(statDict)
    #storeDebug(statDict)

run()