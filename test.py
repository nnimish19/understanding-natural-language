import re
import itertools
import operator
import stopwords        #Online gathered stopwords of english language
import StemmerFile      #Online PorterStemmer to find root/stem word of english words

porter=StemmerFile.PorterStemmer()

#DATA
users = []              #Maintains Speaker list
word_count = {}         #Maintains unique words and its count for each speaker
turn_count = {}         #Maintains turn count for each speaker


###SECTION- PREPARE

#...
#This function separates out non-alphanumeric words from the text, then replaces each word with its root/stem word, and finally removes the stopwords
#...
def separateAndFilterWords(text):
    splitter=re.compile('\\W*')     #\W* ->nonalpha(not a-zA-Z0-9)
    words= [s.lower( ) for s in splitter.split(text) if s!='']
    words = [s for s in words if (len(s)>1 and s!="re" and s!="ve")]
#    words=[porter.stem(s, 0,len(s)-1) for s in words]
    return [s for s in words if s not in stopwords.ignorewords]

#...
#This function removes content within square brackets
#...
def removeTags(s):
    while True:
        ob=s.find("[")
        cb=s.find("]",ob)
        if ob==-1 or cb==-1:
            break
        s=s[:ob]+s[cb+1:]
    return s

#...
#This function finds the current speaker of this line
#...
def checkNewTurn(line):
    list = line.split(":")
    if len(list) == 1: return []

    #alpha numeric check
    splitter=re.compile('\\W*')
    cur_speaker = splitter.split(list[0])
    return cur_speaker if len(cur_speaker)==1 else []

#...
#This is the Main Function that iterates the corpus line by line
#...
def main():
    file = open('/Users/nj/nimish/UFL/NLP/hw1/data1.txt', 'r')
    for line in file:
        cur_line = removeTags(line)
        prev_speaker = ''

        #Find the speaker of this line
        speaker = checkNewTurn(cur_line)
        if speaker==[]:
            cur_speaker = prev_speaker
            dialog_start_pos=0
        else:
            cur_speaker = speaker[0]
            dialog_start_pos = cur_line.find(":") +1

        #Fill in the data structures "users","turn_count","word_count"
        if cur_speaker == '': continue
        if cur_speaker not in users: users.append(cur_speaker)
        if cur_speaker not in turn_count: turn_count[cur_speaker] = 0
        if cur_speaker not in word_count: word_count[cur_speaker] = {}

        turn_count[cur_speaker]+=1;
        words = separateAndFilterWords(cur_line[dialog_start_pos:])
        for w in words:
            if w not in word_count[cur_speaker]: word_count[cur_speaker][w] = 0
            word_count[cur_speaker][w] +=1

        prev_speaker=cur_speaker


###SECTION- PROCESS
#---------------------------------------------------------------------------------------------
#...
#This function calculates - How many dialogue turns did each interlocutor make?
#...
def findTotalDialogTurns():
    map={}
    for u in users:
        map[u] = turn_count[u]
    return map

#...
#This function calculates - How many total words did each interlocutor say?
#...
def findTotalSpokenWords(user=''):
    map = {}
    total_words=0
    if user is not '':
        for k,v in word_count[user].items():  total_words += v         #array of hashes
        map[user] = total_words
        return map

    for u in users:
        total_words = 0
        for (k,v) in word_count[u].items():   #array of hashes
            total_words+=v
        map[u]=total_words

    return map

#...
#This function calculates - How many words per turn on average did each interlocutor make?
#...
def findAvgWordPerTurn():
    map={}
    for u in users:
        map[u]= findTotalSpokenWords(u)[u] / turn_count[u]
    return map

#...
#This function calculates - What is the average length of word that each interlocutor made?
#...
def findAvgLengthOfWord():
    map={}
    for u in users:
        sum_length=0
        total_words=0
        for k,v in word_count[u].items():   #array of hashes
            sum_length += len(k)*v      #Sum(length of each word)/ total number of words
            total_words += v
        map[u]=sum_length/total_words
    return map

#...
#This function calculates - n most frequent uttrances by each interlocutor?
#...
def findMostFrequentUttrances(n):
    map = {}
    for u in users:
        #sort array of hashes on the basis of values
        map[u] = sorted(word_count[u].items(), key = operator.itemgetter(1), reverse = True)
        map[u] = map[u][:n]
    return map


###SECTION- RUN
#---------------------------------------------------------------------------------------------
main()
print "\n\n\n"
print "findTotalDialogTurns", findTotalDialogTurns(),"\n"
print "findTotalSpokenWords",findTotalSpokenWords(),"\n"
print "findAvgWordPerTurn", findAvgWordPerTurn(), "\n"
print "findAvgLengthOfWord",findAvgLengthOfWord(), "\n"
print "findmostFrequentWords", findMostFrequentUttrances(10), "\n"


print "313efcwaf"








