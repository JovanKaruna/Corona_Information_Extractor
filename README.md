# Information Extraction using pattern Matching
Making a web app to extract information from txt file

### Prerequisite
1. pip install nltk
2. pip install flask
3. Make a file 
  ```
  import nltk 
  nltk.download('punkt')
  ```
4. run the file to download nltk punkt

### Compile and Running
Can run in both Windows and Linux
1. Open Command Prompt and go to src directory
1. type `python main.py`
1. There will be local https `http://127.0.0.1:5000/`
1. Copy and paste it into your web app


### File Structure
```
│   README.md
│
├───docs
│       Tucil4StrAlgo_13518024_Laporan
├───src
│   │   main.py
│   │
│   └───templates
│           main.html
│
└───test
        cnbcindo1.txt
        cnnindo1.txt
        cnnindo2.txt
        detik1.txt
        detik2.txt
        kompas1.txt
        kompas2.txt
        kompas3.txt
        kompas4.txt
        kompas5.txt
```

### Input
- txt file from test
- Choose which algorithm to extract information
- input keyword to match in text file

### Output
- Jumlah
- Waktu 
- Sentences

## Acknowledgement
This project is made to fulfill IF2211 Algorithm and Strategy assignment.
Created By : Jovan Karuna Cahyadi 
