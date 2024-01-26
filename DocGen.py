import ntpath
import argparse
import os
import sys
import re
from openai import AzureOpenAI

import nltk
import json

nltk.download('punkt')

# Load config values
with open(r'config.json') as config_file:
    config_details = json.load(config_file)

# Setting up the model detail
gpt_key = config_details['OPENAI_API_KEY']
gpt_endpoint = config_details['OPENAI_API_BASE']
gpt_token_max = config_details['OPENAI_NB_TOKENS']
gpt_model_id=config_details['COMPLETIONS_MODEL']
gpt_api_version=config_details['OPENAI_API_VERSION']

def get_token_count(prompt):
    return len(nltk.word_tokenize(prompt))

def openaiTraduction(prompt,endpoint,key,model_id,api_version):

    #Query openAI


    #print("=*=**=*=*=*=*=*=*=*=*=*=*===*=*nb of token "+str(maxTokenF))
    client= AzureOpenAI(
        azure_endpoint = endpoint,
        #api_version="2023-12-01-preview",
        api_version=api_version,
        api_key = key
        #api_key=os.getenv("AZURE_OPENAI_KEY"),  
    )

    prompt=[{"role": "user", "content": prompt }]
    completion = client.chat.completions.create(model=model_id,
                                                  messages=prompt,
                                                  #max_tokens=get_token_count(prompt)*2 +96,
                                                  max_tokens=20000,
                                                  # stop=".",
                                                  temperature=0.7,
                                                  n=1,
                                                  top_p=0.95,
                                                  frequency_penalty=0,
                                                  presence_penalty=0,
                                                  stop=None
                                                  )

    answer = f"{completion.choices[0].message.content}"
    return answer

def writeOuput(strOpenAI,DocumentName) : 
    docDir="./Doc/"
    if not os.path.exists(docDir):
        os.makedirs(docDir)
    file1 = open(docDir+DocumentName+".md", "w")
    file1.write(strOpenAI)
    file1.close()


if __name__ == "__main__":
    #Command line
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--FileName", help = "python DocGen.py -f <filename> ", required=True)
    
    #Read argument
    args = parser.parse_args()
    
    input_file=args.FileName
    #input_file="FmkUserHome.java"
    DocumentName=os.path.splitext(os.path.basename(input_file))[0]
 
    file2txt=""
    with open(input_file) as infile:
        for line in infile:
            file2txt = file2txt + line


    prompt = "Act as developper, generate the technical and functional markdown documentation with summary of the follwing script :\n"+ file2txt
    #print(prompt)
    answerOpenAI=openaiTraduction(prompt,gpt_endpoint,gpt_key,gpt_model_id,gpt_api_version)
    writeOuput(answerOpenAI,DocumentName)