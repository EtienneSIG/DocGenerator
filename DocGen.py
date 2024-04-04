#System Library
import argparse
import os
import sys
import subprocess

#OpenAI Library
from openai import AzureOpenAI
import nltk

#Json Library
import json

#GUI Library
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from tkinter.filedialog import asksaveasfile
from tkinter import *

#Pre-requisites test and config variables

nltk.download('punkt')

###########################################################
#Check if the library is installed, if not install it.
###########################################################
print("####################################################")
print("##START - Sanity check")
print("####################################################")

print("##Python dependencies\n")
Mandatory_Library=['openai','nltk','tkinter']

for lib in Mandatory_Library:
    if lib not in sys.modules:
        print("Module "+lib+" is not installed.")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lib'])

print("All python library is installed\n")
print("##Varaibles check\n")
# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)

# Set up config var 

Mandatory_Config=['OPENAI_API_KEY','OPENAI_API_BASE','OPENAI_NB_TOKENS','COMPLETIONS_MODEL','OPENAI_API_VERSION']
i=0
print("      VARIABLE     | Status")
for configM in Mandatory_Config:
    if config_details[configM] == "" :
        n_occur=""
        if len(configM) < 18 :
            n_occur = " " * (18-len(configM))
        print(configM+ " | KO ")
    else : 
        n_occur=""
        if len(configM) < 18 :
            n_occur = " " * (18-len(configM))
        print(configM+n_occur+ " | OK ")
        i=i+1

gpt_key = config_details['OPENAI_API_KEY']
gpt_endpoint = config_details['OPENAI_API_BASE']
gpt_token_max = config_details['OPENAI_NB_TOKENS']
gpt_model_id=config_details['COMPLETIONS_MODEL']
gpt_api_version=config_details['OPENAI_API_VERSION']

if i != 5: 
    print("Please could you fill the config file to use the demo")
    sys.exit(0)

print("\n####################################################")
print("##END - Sanity check")
print("####################################################")
###########################################################
# Core functions
###########################################################
def get_token_count(prompt):
    return len(nltk.word_tokenize(prompt))

def openaiTraduction(prompt,endpoint,key,model_id,api_version,nb_token_max):

    #Query openAI


    #print("=*=**=*=*=*=*=*=*=*=*=*=*===*=*nb of token "+str(maxTokenF))
    client= AzureOpenAI(
        azure_endpoint = endpoint,
        #api_version="2023-12-01-preview",
        api_version=api_version,
        api_key = key
        #api_key=os.getenv("AZURE_OPENAI_KEY"),  
    )
    nb_token=get_token_count(prompt)

    prompt=[{"role": "user", "content": prompt }]
    print(nb_token)
    completion = client.chat.completions.create(model=model_id,
                                                  messages=prompt,
                                                  #max_tokens=get_token_count(prompt)*2 +96,
                                                  max_tokens=nb_token_max-nb_token,
                                                  # stop=".",
                                                  temperature=0.7,
                                                  n=1,
                                                  top_p=0.95,
                                                  frequency_penalty=0,
                                                  presence_penalty=0,
                                                  stop=None
                                                  )

    answer = f"{completion.choices[0].message.content}"
    print("End of doc generation")
    return answer

#not use
def writeOuput(strOpenAI,DocumentName) :
    print("documentName : "+DocumentName) 
    docDir="./Doc/"
    if not os.path.exists(docDir):
        os.makedirs(docDir)
    file1 = open(docDir+DocumentName+".md", "w")
    file1.write(strOpenAI)
    file1.close()
    print("Save successfully")


###########################################################
#GUI 
###########################################################

#Size of apps
windows_width=1500
windows_height=400

## root window
root = tk.Tk()
root.geometry('1000x600')
root.resizable(False, False)
root.title('Generate documentation from source code')

##init var 
GPT_PROMPT = StringVar(root, name = "")
MD_DOC = StringVar(root, name = "")
FILE_NAME = StringVar(root, name = "")
WIN_HEIGHT = IntVar(root,windows_height)
WIN_WIDTH = IntVar(root, windows_width)

#Open file function
def openFile():
    tf =fd.askopenfilename(
        initialdir="./", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),
                   ("Text Files", "*.py"),
                   ("Text Files", "*.java"),)
        )
    FILE_NAME.set(str(os.path.splitext(os.path.basename(tf))[0]))
    tf = open(tf)  # or tf = open(tf, 'r')
    data = tf.read()
    GPT_PROMPT.set("Act as developper, generate the technical and functional markdown documentation with summary of the follwing script :\n"+ data)
    txtarea.insert("1.0", data)
    tf.close()

#Display the source code
txtarea = tk.Text(root, width=100, height=15)
txtarea.grid(column=1, row=1, sticky='nswe', padx=10, pady=10)

#GUI to open source code
file_button=ttk.Button(
    root, 
    text="Open File", 
    command=openFile
    )

file_button.grid(column=0, row=1, sticky='nswe', padx=10, pady=10)


#Documentation generation
def GptFile():
    gptanswer = openaiTraduction(GPT_PROMPT.get(),gpt_endpoint,gpt_key,gpt_model_id,gpt_api_version,gpt_token_max)
    MD_DOC.set(gptanswer)
    gptarea.insert("1.0", gptanswer)
    gptarea.mark_names()
    gptarea.mark_set(INSERT,1.1)
    gptarea.mark_gravity(INSERT,RIGHT)

#Display the documentation
gptarea = tk.Text(root, width=100, height=15)
gptarea.grid(column=1, row=2, sticky='nswe', padx=10, pady=10)

#GUI to generate the doc
doc_button=ttk.Button(
    root, 
    text="Documentation Generation", 
    command=GptFile
    )

doc_button.grid(column=0, row=2, sticky='nswe', padx=10, pady=10)

def download_clicked():
    showinfo(
        #title='Information',
        #message='Download button clicked!',
        command=writeOuput(MD_DOC.get(),FILE_NAME.get())
    )

def save_file():
   my_doc=MD_DOC.get()
   f = asksaveasfile(initialfile = FILE_NAME.get(),defaultextension=".md",filetypes=[("All Files","*.*"),("Text Documents","*.md")])
   f.write(my_doc)
   f.close()



download_icon = tk.PhotoImage(file=".\\icon\\download_small.png")

download_button = ttk.Button(
    root,
    image=download_icon,
    text='Download',
    compound=tk.LEFT,
    command=save_file
    #command=download_clicked
)

download_button.grid(row=3,column=0, columnspan=3, sticky='nswe', padx=10, pady=10)

scroll_bar = tk.Scrollbar(txtarea, orient="vertical")
scroll_bar.config()
root.mainloop()