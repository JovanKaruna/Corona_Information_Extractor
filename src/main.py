import re
import nltk
from nltk.tokenize import sent_tokenize
from flask import Flask, render_template, request

def regexMatch(text, pattern): #Pattern matching with regex
    text = text.lower()
    pattern = pattern.lower()
    result = re.findall(str(pattern), str(text))
    return result


def kmpMatch(text, pattern): #pattern matching with KMP
    text = text.lower() #lowercase
    pattern = pattern.lower() #lowercase
    text_length = len(text)
    pattern_length = len(pattern)
    fail = computeFail(pattern)
    i = 0
    j = 0
    while(i < text_length):
        if(pattern[j] == text[i]):
            if(j == pattern_length - 1):
                return i - pattern_length + 1 # match
            i += 1
            j += 1
        elif(j > 0):
            j = fail[j-1]
        else:
            i += 1
    return -1 #no match

def computeFail(pattern): #fail function for KMP
    fail = [0 for i in range (len(pattern))]
    fail[0] = 0
    pattern_length = len(pattern)
    i =1
    j =0
    while(i < pattern_length):
        if(pattern[j]== pattern[i]):
            fail[i] = j+1
            i += 1
            j += 1
        elif(j > 0):
            j = fail[j-1]
        else:
            fail[i]=0
            i += 1
    return fail

def bmMatch(text, pattern): #Pattern matching for BM
    text = text.lower()
    pattern = pattern.lower()
    last = buildLast(pattern)
    text_length = len(text)
    pattern_length = len(pattern)
    i = pattern_length - 1
    if(i > text_length - 1):
        return -1
    j = pattern_length - 1
    while True:
        if(pattern[j] == text[i]):
            if(j == 0):
                return i  #match
            else:
                i -= 1
                j -= 1
        else:
            lo = last[ord(text[i])]
            i = i + pattern_length - min(j, 1+lo)
            j = pattern_length - 1
        if(i > text_length - 1):
            break
    return -1 #no match

def buildLast(pattern): #Initialize array for BM
    last = [-1 for i in range(128)]
    for i in range(len(pattern)):
        last[ord(pattern[i])] = i
    return last

def findJumlah(text,pattern): #Find jumlah from text
    pattern_length = len(pattern)
    start_pos = kmpMatch(text,pattern)
    text = text.replace('.', '')
    list = re.findall('(?<=\s)\d+(?=\s)', text) #find all numbers with space between it
    result = -1
    diff_pos = 99999999999 #initialize largest position
    for num in list:
        pos_front = abs(kmpMatch(text,num) - start_pos) #position of numbers from the front of pattern
        pos_back = abs(kmpMatch(text,num) - start_pos + pattern_length) #position of numbers from the back of pattern
        if(pos_back < pos_front):
            pos = pos_back
        else:
            pos = pos_front
        if(pos < diff_pos): #find the smallest difference position to pattern
            diff_pos = pos
            result = num #the number that is closer to the pattern is put into result
    return result

def findWaktu(content): #find all waktu using regex, I use 4 regex for waktu
    content = content.lower()
    list = re.findall('(?:\(\d+\/\d+\/\d+\)|\d+\/\d+\/\d+),\s*(?:pukul\s+(?:\d+:\d+|\d+.\d+)|(?:\d+:\d+|\d+.\d+))\s*(?:wib|wita|wit|'')',content)
    temporary = re.findall('(?:senin|selasa|rabu|kamis|jumat|sabtu|minggu|'')(?:,|'')\s\d+\s(?:jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|nov|des)\s\d{4}\s\d{2}:\d{2}\s(?:wib|wita|wit)',content)
    for temp in temporary:
        list.append(temp)
    temporary = re.findall('(?:senin|selasa|rabu|kamis|jumat|sabtu|minggu)(?:,|'')\s+(?:\(\d+\/\d+\/\d+\)|\d+\/\d+\/\d+|\(\d+\/\d+\))\s*(?:pukul\s+(?:\d+:\d+|\d+.\d+)|(?:\d+:\d+|\d+.\d+)|'')\s*(?:wib|wita|wit|'')',content)
    for temp in temporary:
        list.append(temp)
    temporary = re.findall('\d+\s(?:jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|nov|des|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s*\d{4}',content)
    for temp in temporary:
        list.append(temp)
    return list #return list of waktu from the content

def file_read(file): #Read a file and return the content
    f= open(file, "r")
    content = f.read() #read file
    #preProcess the content before dividing into sentences 
    content = content.replace('.\n', '. ') 
    content = content.replace('\n\n', '. ')
    content = content.replace('\n', '. ')
    return content
    
def get_sentences(content):    #divide the content into sentences using nltk
    text = sent_tokenize(content) #using nltk to divide the content into lists of sentences
    return text

#This function used if user choose to use BM algorithm from the web app
def BM_Algorithm(content,pattern): #this is the BM_Algorithm to give all sentences, jumlah, and waktu.
    result = []
    jumlah = []
    waktu = []
    time = findWaktu(content) #find waktu in full text
    text = get_sentences(content)
    for line in text: #iterate every sentences
        pos = bmMatch(line, pattern) #use bmMatch to find position
        if(pos != -1): #match
            num= findJumlah(line, pattern) #find jumlah from line
            if(num == -1): #no jumlah in line
                num = "Tidak ada jumlah"
            time1 = findWaktu(line) #find waktu from line
            if(len(time1)==0): #no waktu from line
                waktu.append(time[0]) #append the first waktu from full text, it supposed to be the news date
            else:
                waktu.append(time1[0])
            jumlah.append(num)
            result.append(line)
    return result,jumlah,waktu


#This function used if user choose to use KMP algorithm from the web app
def KMP_Algorithm(content,pattern):
    result = []
    jumlah = []
    waktu = []
    time = findWaktu(content) #find waktu in full text
    text = get_sentences(content)
    for line in text:   #iterate every sentences
        pos = kmpMatch(line, pattern) #use kmpMatch to fine position
        if(pos != -1): #match
            num= findJumlah(line, pattern) #find jumlah from line
            if(num == -1): #nojumlah found from line
                num = "Tidak ada jumlah"
            time1 = findWaktu(line) # find waktu from line
            if(len(time1)==0): #no waktu found from line
                waktu.append(time[0]) #append the first waktu from full text, it supposed to be the news date
            else:
                waktu.append(time1[0])
            jumlah.append(num)
            result.append(line)
    return result,jumlah, waktu


#This function used if user choose to use Regex algorithm from the web app
def Regex_Algorithm(content, pattern):
    result =[]
    jumlah = []
    waktu = []
    time = findWaktu(content) #find waktu in full text
    text = get_sentences(content)
    list = regexMatch(content,pattern)
    if(len(list)>0): #terdapat pattern di text
        for line in text:
            list_line = regexMatch(line, pattern)
            if(len(list_line)>0): #terdapat pattern match di line tersebut
                num= findJumlah(line, pattern)
                if(num == -1):
                    num = "Tidak Ditemukan"
                time1 = findWaktu(line)
                if(len(time1)==0):
                    waktu.append(time[0]) #append the first waktu from full text, it supposed to be the news date
                else:
                    waktu.append(time1[0])
                jumlah.append(num)
                result.append(line)
    return result,jumlah, waktu

app = Flask(__name__)
path = "../test/"

#main page of web
@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        try:
            file = request.form['file']
            key = request.form['ky']
            option = request.form['options']
        except :
            return render_template('main.html', cek=0)
        content = file_read(path + file)
        result =[]
        jumlah =[]
        waktu = []
        if(option == 'BM'): #if user choose BM algorithm
            result, jumlah, waktu = BM_Algorithm(content,key)
        elif(option == 'KMP'): #user choose KMP algorithm
            result, jumlah, waktu = KMP_Algorithm(content,key)
        elif(option == 'Regex'): #user choose Regex algorithm
            result,jumlah, waktu = Regex_Algorithm(content,key)
        size = len(result)
        return render_template('main.html', keyword=key, size=size, result=result, jumlah=jumlah, file=file,waktu = waktu, cek =1)
    else:
        return render_template('main.html', cek=0)


if __name__ == '__main__':
   app.run(debug = True)