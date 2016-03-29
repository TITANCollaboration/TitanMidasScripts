import cycletime as ct
import pythonmidas.pythonmidas as Midas

try:
    runtime = ct.run_time()
    msg = "The next run will take: " + str(runtime) + " min."
except Exception as e:
    msg = "Error: " + str(e)

Midas.sendmessage("CycleTime", msg)
