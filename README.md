# pinyin-input-method



```tree
D:\_WANGKE\0\MYPINYIN        
│  .gitignore
│  all_requirements.txt      
│  requirements.txt
├─db
│  │  correct.txt
│  │  pinyin.txt
│  │  preprocess.py
│  │  wordfreq.txt
│  │
│  └─corpus
├─images
├─model
│  │  emission_log_probability.json  
│  │  start_log_probability.json     
│  │  transition_log_probability.json
│  │
│  └─reverse
│          compute_nxt.json
│          reversed_emission.json    
│          reversed_transition.json  
│
├─path
│      mypinyin.pth
│
└─src
   │  main.py
   │
   ├─conf
   │     config.py
   │   
   ├─hmm
   │  │  hmm.py
   │  │
   │  └─train
   │        freqdata.py
   │        train.py
   │ 
   ├─interface
   │     ime.py
   │     imeui.py
   │     imeui.ui
   │
   ├─split
   │     pycut.py
   │  
   ├─test
   │      test.py
   │
   └─util
         tools.py

```
