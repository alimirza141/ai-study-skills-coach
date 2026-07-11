topic = input("enter topic naame: ")
conf = null
while conf not in range(0,6) 
  conf = int(input("rate your confidence from 1-5: ")

nextdate = input("When would you like to revise next?: ")
print(f'Your confidence level in {topic} is {conf} and your next study session is on {nextdate}.)
if conf <=2:
  print(f'I suggest you revise {topic} soon.')

