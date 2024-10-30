import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col="date")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 6))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group and unstack data
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    df_bar.columns = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(15, 10), xlabel='Years', ylabel='Average Page Views').figure
    plt.legend(title='Months')
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Draw box plots (using Seaborn)
    fig, (axe1, axe2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Year-wise Box Plot (Trend)
    sns.boxplot(data=df_box, x='year', y='value', ax=axe1, hue='year', palette="Set2")
    axe1.set_title("Year-wise Box Plot (Trend)")
    axe1.set_xlabel("Year")
    axe1.set_ylabel("Page Views")
    
    # Month-wise Box Plot (Seasonality)
    sns.boxplot(data=df_box, x='month', y='value', ax=axe2,  hue='month', palette="Set2", order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 
                                                                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 
                                                                   'Nov', 'Dec'])
    axe2.set_title("Month-wise Box Plot (Seasonality)")
    axe2.set_xlabel("Month")
    axe2.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
