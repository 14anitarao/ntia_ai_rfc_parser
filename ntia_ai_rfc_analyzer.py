import os
import openai
import pandas as pd
import glob
import openai

MODEL = "gpt-3.5-turbo"

'''
This is an analyzer tool to summarize text in documents previously downloaded from Regulations.gov website.
The summaries are done using OpenAI API Chat Completion feature.
'''

# Configure download location
download_loc = "/Users/anitarao/TechCongress/ntia_ai_rfc_parser/NTIA_RFC_Files"

def summarize():
    df = pd.DataFrame()

    openai.organization = "org-9haUual5BRk31ALTV1ttluGA"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    files = glob.glob(download_loc + "*.txt")

    for f in files:
        filename = f
        id =os.path.splitext(filename.split('/')[-1])[0]
        s = open(filename, 'r').read()

        message = s

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Please summarize this text in 3-5 sentences: " + s},
            ],
            temperature=0,
        )

        sum_resp = response['choices'][0]['message']['content']

        try:
            df_new_row = pd.DataFrame([{"id":id, "summary": sum_resp}])
            df = pd.concat([df, df_new_row], ignore_index=True)
        except:
            print("couldnt summarize using GPT")

    df.to_csv(download_loc + "GPT_Summaries.csv")

def main():
    summarize()


if __name__ == '__main__':
    main()
