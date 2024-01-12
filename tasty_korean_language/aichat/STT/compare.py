import re

def compare(origin,transcription):
    
    nSen1 = re.sub('[^가-힣\s]', '', origin)
    nSen1 = re.sub('\s+', ' ', nSen1)
    nSen1 = nSen1.split()

    nSen2 = transcription.split()

    diff = []
    for i in range(0,len(nSen1)):
        try:
            if nSen1[i]!=nSen2[i]:
                diff.append([nSen2[i],nSen1[i]])
        except:
            pass

    # #틀린 부분 출력
    # print(diff)
    
    return diff
