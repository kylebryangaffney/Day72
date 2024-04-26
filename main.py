import pandas
import pandas

df = pandas.read_csv('salaries_by_college_major.csv')
pandas.options.display.float_format = '{:,.2f}'.format
# df.head()
clean_df = df.dropna()
# highest_start_id = clean_df['Starting Median Salary'].idxmax()
# print(clean_df.loc[highest_start_id])

# highest_mid_id = clean_df['Mid-Career Median Salary'].idxmax()
# print(clean_df.loc[highest_mid_id])

# lowest_start_id = clean_df['Starting Median Salary'].idxmin()
# print(clean_df.loc[lowest_start_id])

# lowest_mid_id = clean_df['Mid-Career Median Salary'].idxmin()
# print(clean_df.loc[lowest_mid_id])

spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
clean_df.insert(1, 'Spread', spread_col)
# low_risk = clean_df.sort_values('Spread', ascending=False)
# low_risk[['Undergraduate Major', 'Spread']].head()

# high_risk = clean_df.sort_values('Spread', ascending=False)
# high_risk[['Undergraduate Major', 'Spread']].head()

# highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
# highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
numeric_colummns = ['Spread', 'Starting Median Salary', 'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary', 'Mid-Career 90th Percentile Salary']
clean_df.groupby('Group')[numeric_colummns].mean()



## get new data from payscale.com
table_from_html = pandas.read_html("https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")
## add the new data to a dataframe
df = table_from_html[0].copy()
df.columns = ["Rank", "Major", "Type", "EarlyCareerPay", "MidCareerPay", "HighMeaning"]
 
# Add tables from new pages into original dataframe
for i in range(2, 35):
    table_from_html = pandas.read_html(f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{i}")
    i_df = table_from_html[0].copy()
    i_df.columns = ["Rank", "Major", "Type", "EarlyCareerPay", "MidCareerPay", "HighMeaning"]
    df = df.append(i_df, ignore_index=True)
 
# Select necessary columns only
df = df[["Major", "EarlyCareerPay", "MidCareerPay"]]
 
# Clean columns
df.replace({"^Major:": "", "^Early Career Pay:\$": "", "^Mid-Career Pay:\$": "", ",": ""}, regex=True, inplace=True)
 
# Change datatype of numeric columns
df[["EarlyCareerPay", "MidCareerPay"]] = df[["EarlyCareerPay", "MidCareerPay"]].apply(pandas.to_numeric)