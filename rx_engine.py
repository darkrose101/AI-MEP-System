import time

functions = []

time_quantum = 1


for i in range(len(functions)):
  current_function = functions[i]
  
  start_time = time.time()
  current_function()
  end_time = time.time()
  elapsed_time = end_time - start_time
  if elapsed_time < time_quantum:
    time.sleep(time_quantum - elapsed_time)

  else:
    print(f"Function {i} took longer than {time_quantum} seconds to execute")
    functions.append(current_function)
    functions.remove(current_function)