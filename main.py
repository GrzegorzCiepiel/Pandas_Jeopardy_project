import pandas as pd
pd.set_option('display.max_columns', None)


# 1. We've provided a csv file containing data about the game show _Jeopardy!_ in a file named `jeopardy.csv`.
# Load the data into a DataFrame and investigate its contents. Try to print out specific columns.

df = pd.read_csv("jeopardy.csv")
print(df.columns)
print(df.head(3))


# 2. We may want to eventually compute aggregate statistics, like `.mean()` on the `" Value"` column.
# But right now, the values in that column are strings. Convert the`" Value"` column to floats.
# If you'd like to, you can create a new column with float values.

df = df.rename(columns={' Air Date': 'Date',
                        ' Round': 'Round',
                        ' Category': 'Category',
                        ' Value': 'Value',
                        ' Question': 'Question',
                        ' Answer': 'Answer'
                        })
print(df.columns)

df['Value'] = df['Value'].apply(lambda x: x.split('$')[-1])
df['Value'] = df['Value'].apply(lambda row: row.split(',')[0] + row.split(',')[-1] if ',' in row else row)
df['Value'] = df['Value'].apply(lambda x: 0 if x == 'no value' else x)
df['Value'] = pd.to_numeric(df['Value'])
print(df.info())

print(df.head(2))

# 3. Write a function that filters the dataset for questions that contains all of the words in a list of words.
# For example, when the list `["King", "England"]` was passed to our function, the function returned a DataFrame
# of 49 rows. Every row had the strings `"King"` and `"England"` somewhere in its `" Question"`.
# Test your function by printing out the column containing the question of each row of the dataset.

def all_words(data, words):
    filter = lambda x: all(word.lower() in x.lower() for word in words)
    return data.loc[data["Question"].apply(filter)]


print(all_words(df, ["King", "England"]))
mean_value = df.Value.mean()
print(round(mean_value, 2))

# 4. What is the average value of questions that contain the word `"King"`?

mean_k_value = df.Value[df['Question'].apply(lambda x: "King".lower() in x.lower())]
print(mean_k_value)
print(mean_k_value.mean())


# 5.  Write a function that returns the count of unique answers to all of the
# questions in a dataset. For example, after filtering the entire dataset to
# only questions containing the word `"King"`, we could then find all of the
# unique answers to those questions. The answer "Henry VIII" appeared 55 times
# and was the most common answer.

def count_unique_answers(word):
    return df.Answer[df['Question'].apply(lambda x: word.lower() in x.lower())].value_counts()


print(count_unique_answers('King'))

# 6. Investigate the ways in which questions change over time by filtering by
# the date. How many questions from the 90s use the word `"Computer"` compared
# to questions from the 2000s?

df_sorted = df['Date'].sort_values()
print(df_sorted)

df['Year'] = df.Date.apply(lambda x: x.split('-')[0])
print(df.head(2))



word_in_time = df.Year[df['Question'].apply(lambda x: "Computer".lower() in x.lower())].value_counts()

print(word_in_time)

print ("In 90s the word 'Computer' appears 98 times but between year 1990 and 1995 appears only  5 times.\nIn the 2000s word 'Computer appers 268 timmes what is almost 3 times more.")

