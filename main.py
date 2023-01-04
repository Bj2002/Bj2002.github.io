import datetime
import matplotlib.pyplot as plt

maxprob = 100
maxpeople = 100
maxday = 200
d0 = datetime.datetime (2022, 9, 27, 0, 0, 0)
fileCnt = 100



id2name = {}
probvis = {}
stuvis = {}

file = open ("id2name.txt" , "r")
line = file.readline()

while (line) :
  line = line.split()
  line = line[0].split(',')
  id2name[line[0]] = line[1]

  line =file.readline()

subVis = {}
def checkDate (s : str) ->bool :
  return (len(s) == 10 and s[4] == '/')

sList = []
for i in range(1 , fileCnt + 1) :
  file = open (str(i) + ".txt" , "r" , encoding="utf-8")

  line = file.readline ()
  while (line) :
    line = line.split()

    for s in line :

      if (checkDate(s)) :

        date = s.replace ('/' , '')
        time = line[1].replace(':' , '')
        res = file.readline ().split()[0]
        file.readline()
        score = file.readline().strip()
        prob = file.readline().strip()
        while (len(prob) == 0 or prob[0] > '9' or prob[0] < '0') :
          prob = file.readline().strip()

        sid = file.readline().strip()
        while (id2name.get(sid , None) == None) :
          sid = file.readline().strip()

        #print (date , time , res , score , prob , id2name[sid])

        Submission = date + ' ' + time + ' ' + res + ' ' + score + ' ' + prob + ' ' + sid

        hashVal = hash(Submission)
        if (subVis.get(hashVal , 0) == 0 ) :
          #print(Submission , hash(Submission))

          sList.append (Submission)
          subVis[hashVal] = 1

    line = file.readline ()
sList.sort()

tot = [[ 0 for _ in range(maxprob)] for _ in range(maxpeople)]
sum = [[ 0 for _ in range(maxday)] for _ in range(maxday)]

probCnt = 0
stuCnt = 0

dayCnt = 0
print (d0)
for s in sList :

  iList = s.split()

  year = iList[0][0:4]
  month = iList[0][4:6]
  day = iList[0][6:8]

  score = int(iList[3])
  sid = iList[5]
  prob = iList[4]

  stuID = stuvis.get (sid , 0)
  if (stuID == 0) :
    stuCnt = stuCnt + 1
    stuvis[sid] = stuCnt
    stuID = stuCnt

  probID = probvis.get (prob ,0)
  if (probID == 0):
    probCnt = probCnt + 1
    probvis[prob] = probCnt
    probID = probCnt

  bef = tot[stuID][probID]

  thisDay = datetime.datetime ( int(year ), int(month) , int(day) )
  dayID = (thisDay - d0).days
  dayCnt = max (dayCnt , dayID)
  
  if (score > bef ) :
    tot[stuID][probID] = score
    sum[stuID][dayID] = score - bef + sum[stuID][dayID]
  #print(stuID , probID)
  #print(iList)

for i in range(1 , dayCnt + 1) :

  for j in range(1 , stuCnt + 1 ) :
    sum[j][i] = sum[j][i] + sum[j][i - 1]

X = [i for i in range(0,dayCnt + 1)]

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

def findMaxkey (dic ) :

  maxv = -1
  maxi = None
  for x in dic :
    if (dic[x] > maxv) :
      maxv = dic[x]
      maxi = x
  return maxi
for sid in stuvis :
  plt.cla()

  #stuID = stuvis[sid]
  #temp = sum[stuID][0:dayCnt+1]

  #plt.plot(X , temp)
  #plt.savefig (sid + ".jpeg")
  scnt = 0
  stateCnt = {}
  timeCnt = {}
  lateList = {}
  dayCnt = {}
  monCnt = {}
  print (sid , id2name[sid])
  for s in sList :
    if (s.find (sid) != -1 ) :
      scnt =scnt + 1
      iList = s.split()

      timeCnt[iList[1][0:2]] = timeCnt.get(iList[1][0:2] , 0) + 1
      stateCnt[iList[2]] = stateCnt.get (iList[2] , 0) + 1 
      year = iList[0][0:4]
      month = iList[0][4:6]
      day = iList[0][6:8]


      
      t = int(iList[1][0:2])

      dayCnt[iList[0]] = dayCnt.get(iList[0] , 0) + 1
      monCnt[iList[0][0:6] ]= monCnt.get(iList[0][0:6] , 0) + 1
      if (t <= 5) :
        lateList[iList[0]] = lateList.get (iList[0] , 0) + 1

  print(lateList)
  print(stateCnt)
  print (timeCnt)#每天都在啥时候交
  print(dayCnt)
  print(monCnt)

  moban = open ("template.html" , "r")

  res = open (sid + ".html" , "w")
  print(sid + ".html")
  line = moban.readline()

  maxfaultState = None
  maxcnt = 0
  for i in stateCnt :

    if (i != "答案正确") :
      if (maxfaultState == None or maxcnt < stateCnt[i]) :
        maxcnt = stateCnt[i]
        maxfaultState = i

  print(maxfaultState , maxcnt)
  print (findMaxkey(timeCnt))
  while (line) :

    line = line.replace ("sid" , sid)
    line = line.replace ("TOT_SUBMISSION" , str(scnt))
    line = line.replace ("TOT_ACCEPTED" , str(stateCnt.get("答案正确" , 0)))
    line = line.replace ("COMMON_FAULT_NAME" , maxfaultState)
    line = line.replace ("COMMON_FAULT_CNT" , str(maxcnt))
    line = line.replace ("SUBMIT_HOUR" , "每天的"+findMaxkey(timeCnt)+"点左右")
    line = line.replace ("SUBMIT_MONTH" , findMaxkey(monCnt)[0:4]+"年" + findMaxkey(monCnt)[4:6]+"月")
    line = line.replace ("SUBMIT_DAY" , findMaxkey(dayCnt)[0:4]+"年" + findMaxkey(dayCnt)[4:6]+"月" +findMaxkey(dayCnt)[6:8] +"日")
    line = line.replace ("S_UBMIT_DAY_CNT" , str(dayCnt[findMaxkey(dayCnt)]))
    line = line.replace ("LATE_CNT" , str(len(lateList)))
    
    #if (line.find(sid)==-1) :
      #print(line)
    #print(line)

    res.write(line)
    line = moban.readline()
    
  res.close()
  moban.close()

tpl = open ("idxTemplate.txt" , "r")
index = open ("index.html" , "w" ,encoding='UTF-8')

line = tpl.readline()

while (line) :
  
  line = tpl.readline()

  if (line.find("sid") != -1) :
    for i in stuvis :

      t = line.replace ("sid" , i)
      t = t.replace ("name" , id2name[i])
      print(i , id2name[i])
      index.write(t)
  else :
    index.write(line)
index.close ()
tpl.close ()

