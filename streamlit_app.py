import streamlit as sl
import pandas as pd

# 1. import answers file
# 2. import results file
# 3. print exceptions

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, lineterminator='\r\n').encode('utf-8')


sl.sidebar.write("___________________")
sl.sidebar.write("CONFIGURATION PANEL")
answers_file = sl.sidebar.file_uploader("Select answers file (.xlsx)")
results_file = sl.sidebar.file_uploader("Select results file (.csv)")

if answers_file != None:
    # Load the Excel file
    answers_df = pd.read_excel(answers_file)
    sl.write(answers_df)

if results_file != None:
    # Load the Excel file
    results_df = pd.read_csv(results_file, sep="\t")

    sl.write(results_df)

go = sl.button("do it!")
if go:
    #make sure the email field is a string
    results_df['core.email'] = results_df['core.email'].astype(str)
    #for each row in results where there's an email address..
        #for each row in Answers, get the question code and check the column
            #if

    #hold all the wrong answers here
    output_df = pd.DataFrame(columns=['email', 'question', 'answer_given', 'correct_answer'])

    for index, row in results_df.iterrows():
        if row['core.email'].find('@')>0:
        # Perform actions on this row
            email = row['core.email']
            sl.sidebar.write("Checking "+email)
            for code in answers_df['Question_coding']:
                if code in row.index:
                    answer = int(row[code])
                    correct_answer = int(answers_df.loc[answers_df['Question_coding'] == code]['Answer'])
                    question_text = answers_df.loc[answers_df['Question_coding'] == code, 'Question_text'].values[0]
                    wrong_answer_text = answers_df.loc[answers_df['Question_coding'] == code, answer].values[0]
                    correct_answer_text = answers_df.loc[answers_df['Question_coding'] == code, correct_answer].values[0]
                    #sl.sidebar.write(wrong_answer_text)
                    if answer == correct_answer:
                        #don't care about correct answer
                        do_nothing=True
                        #sl.write(email+" got "+code+" correct")
                    else:
                        sl.write(email+" got "+code+" wrong")
                        sl.write("Question was: "+question_text)
                        sl.write("They answered: "+wrong_answer_text)
                        sl.write("Correct answer was: " + correct_answer_text)

                        # streamlit cloud didnt like this command
                        #output_df = output_df.append({'email': email, 'question': question_text, 'answer_given': wrong_answer_text,
                        #                'correct_answer': correct_answer_text}, ignore_index=True)
                        
                        output_df = pd.concat([output_df, pd.DataFrame({'email': [email],
                                                          'question': [question_text],
                                                          'answer_given': [wrong_answer_text],
                                                          'correct_answer': [correct_answer_text]})])

    sl.write(output_df)
    csv = convert_df(output_df)
    sl.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="wrong answers",
        mime='text/csv',
    )
