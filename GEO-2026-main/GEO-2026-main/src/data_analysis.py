import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def analyze_geo_data():
    """
    Comprehensive analysis of the geo dummy data containing clothing production information
    """
    # Load the data
    file_path = "./data/geo dummy  - Sheet1 (1).csv"
    df = pd.read_csv(file_path)
    
    print("="*60)
    print("COMPREHENSIVE DATA ANALYSIS REPORT")
    print("="*60)
    
    # Basic info about the dataset
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of Records: {len(df)}")
    print(f"Number of Features: {len(df.columns)}")
    print(f"Features: {list(df.columns)}")
    
    # Data types
    print(f"\nData Types:")
    print(df.dtypes)
    
    # Check for missing values
    print(f"\nMissing Values:")
    print(df.isnull().sum())
    
    # Display first few records
    print(f"\nFirst 5 Records:")
    print(df.head())
    
    # Convert date columns to datetime
    df['Project Start'] = pd.to_datetime(df['Project Start'], format='%d/%m/%Y', errors='coerce')
    df['Project Deadline'] = pd.to_datetime(df['Project Deadline'], format='%d/%m/%Y', errors='coerce')
    
    # Feature Engineering
    df['Days_to_Complete'] = df['Time Needed (in days)']
    df['Hours_per_Clothing'] = df['Working Time per Clothes (in hours)']
    df['Daily_Working_Hours'] = df['Working time per day (in hours)']
    df['Clothes_Assigned'] = df['Clothes Assigned']
    df['Project_Window_Days'] = df['Project Window']
    
    # Calculate productivity metrics
    df['Effective_Hours_Per_Day'] = df['Hours_per_Clothing'] * df['Clothes_Assigned'] / df['Days_to_Complete']
    df['Productivity_Rate'] = df['Clothes_Assigned'] / df['Days_to_Complete']  # clothes per day
    
    print(f"\nStatistical Summary:")
    print(df.describe())
    
    # Analysis of categorical variables
    print(f"\nClothes Category Distribution:")
    print(df['Clothes Category'].value_counts())
    
    print(f"\nClothes Type Distribution:")
    print(df['Clothes Type'].value_counts())
    
    print(f"\nSpecialist Distribution:")
    print(df['Specialist'].value_counts())
    
    # Analysis of numerical variables
    print(f"\nAverage Days to Complete by Category:")
    print(df.groupby('Clothes Category')['Days_to_Complete'].mean())
    
    print(f"\nAverage Hours per Clothing by Category:")
    print(df.groupby('Clothes Category')['Hours_per_Clothing'].mean())
    
    # Create visualizations
    create_visualizations(df)
    create_scatter_matrix(df)
    
    # Detailed analysis sections
    analyze_project_timelines(df)
    analyze_clothing_categories(df)
    analyze_worker_performance(df)
    analyze_productivity_metrics(df)
    
    print(f"\nAnalysis completed successfully!")
    return df

def create_visualizations(df):
    """
    Create various visualizations to understand the data
    """
    # Create a directory for plots if it doesn't exist
    plot_dir = "./plots"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    # Figure 1: Distribution of numerical features
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Distribution of Key Numerical Features', fontsize=16)
    
    # Days to Complete
    axes[0, 0].hist(df['Days_to_Complete'], bins=20, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of Days to Complete')
    axes[0, 0].set_xlabel('Days to Complete')
    axes[0, 0].set_ylabel('Frequency')
    
    # Hours per Clothing
    axes[0, 1].hist(df['Hours_per_Clothing'], bins=20, edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Distribution of Hours per Clothing')
    axes[0, 1].set_xlabel('Hours per Clothing')
    axes[0, 1].set_ylabel('Frequency')
    
    # Daily Working Hours
    axes[0, 2].hist(df['Daily_Working_Hours'], bins=20, edgecolor='black', alpha=0.7)
    axes[0, 2].set_title('Distribution of Daily Working Hours')
    axes[0, 2].set_xlabel('Daily Working Hours')
    axes[0, 2].set_ylabel('Frequency')
    
    # Clothes Assigned
    axes[1, 0].hist(df['Clothes_Assigned'], bins=20, edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Distribution of Clothes Assigned')
    axes[1, 0].set_xlabel('Clothes Assigned')
    axes[1, 0].set_ylabel('Frequency')
    
    # Productivity Rate
    axes[1, 1].hist(df['Productivity_Rate'], bins=20, edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('Distribution of Productivity Rate (Clothes/Day)')
    axes[1, 1].set_xlabel('Productivity Rate')
    axes[1, 1].set_ylabel('Frequency')
    
    # Project Window
    axes[1, 2].hist(df['Project_Window_Days'], bins=20, edgecolor='black', alpha=0.7)
    axes[1, 2].set_title('Distribution of Project Window (Days)')
    axes[1, 2].set_xlabel('Project Window (Days)')
    axes[1, 2].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/numerical_distributions.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Figure 2: Category distributions
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Categorical Variable Analysis', fontsize=16)
    
    # Clothes Category pie chart
    category_counts = df['Clothes Category'].value_counts()
    axes[0, 0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Distribution of Clothes Categories')
    
    # Specialist distribution
    specialist_counts = df['Specialist'].value_counts()
    axes[0, 1].bar(specialist_counts.index, specialist_counts.values, edgecolor='black')
    axes[0, 1].set_title('Distribution of Specialists')
    axes[0, 1].set_xlabel('Specialist Type')
    axes[0, 1].set_ylabel('Count')
    
    # Clothes Type bar chart (top 10)
    top_clothes_types = df['Clothes Type'].value_counts().head(10)
    axes[1, 0].barh(range(len(top_clothes_types)), top_clothes_types.values)
    axes[1, 0].set_yticks(range(len(top_clothes_types)))
    axes[1, 0].set_yticklabels(top_clothes_types.index)
    axes[1, 0].set_title('Top 10 Clothes Types')
    axes[1, 0].set_xlabel('Count')
    
    # Average Days to Complete by Category
    avg_days_by_category = df.groupby('Clothes Category')['Days_to_Complete'].mean()
    axes[1, 1].bar(avg_days_by_category.index, avg_days_by_category.values, edgecolor='black')
    axes[1, 1].set_title('Average Days to Complete by Category')
    axes[1, 1].set_xlabel('Clothes Category')
    axes[1, 1].set_ylabel('Average Days to Complete')
    
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/categorical_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Figure 3: Correlation heatmap
    numeric_cols = ['Clothes Assigned', 'Time Needed (in days)', 'Working Time per Clothes (in hours)', 
                   'Working time per day (in hours)', 'Project Window', 'Productivity_Rate', 'Effective_Hours_Per_Day']
    corr_data = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, square=True)
    plt.title('Correlation Heatmap of Numerical Variables')
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()


def create_scatter_matrix(df):
    """
    Create a scatter matrix of numerical features
    """
    plot_dir = "./plots"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    # Select numerical columns for scatter matrix
    numeric_cols = ['Clothes Assigned', 'Time Needed (in days)', 'Working Time per Clothes (in hours)', 
                   'Working time per day (in hours)', 'Project Window', 'Productivity_Rate', 'Effective_Hours_Per_Day']
    
    # Filter dataframe to only include numeric columns that exist
    available_numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_numeric_cols) > 1:
        # Create scatter matrix
        scatter_fig = sns.pairplot(df[available_numeric_cols], diag_kind='hist', plot_kws={'alpha':0.6})
        scatter_fig.fig.suptitle('Scatter Matrix of Numerical Features', y=1.02)
        plt.savefig(f'{plot_dir}/scatter_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    else:
        print("Insufficient numerical columns for scatter matrix")

def analyze_project_timelines(df):
    """
    Analyze project timelines and scheduling
    """
    print(f"\n{'='*50}")
    print("PROJECT TIMELINE ANALYSIS")
    print(f"{'='*50}")
    
    print(f"Date Range: {df['Project Start'].min()} to {df['Project Deadline'].max()}")
    
    # Timeline analysis
    timeline_summary = df.groupby(['Project Start', 'Project Deadline']).size().reset_index(name='Projects_Count')
    print(f"Number of unique project periods: {len(timeline_summary)}")
    
    # Projects overlapping in time
    df_sorted = df.sort_values('Project Start')
    print(f"Earliest project start: {df_sorted['Project Start'].iloc[0]}")
    print(f"Latest project deadline: {df_sorted['Project Deadline'].iloc[-1]}")
    
    # Analysis of project window vs actual completion time
    print(f"\nProject Window vs Actual Completion Time:")
    print(f"Average Project Window: {df['Project Window'].mean():.2f} days")
    print(f"Average Actual Completion Time: {df['Time Needed (in days)'].mean():.2f} days")
    print(f"Difference (Window - Actual): {df['Project Window'].mean() - df['Time Needed (in days)'].mean():.2f} days")
    
def analyze_clothing_categories(df):
    """
    Analyze different clothing categories and types
    """
    print(f"\n{'='*50}")
    print("CLOTHING CATEGORIES ANALYSIS")
    print(f"{'='*50}")
    
    # Custom vs Uniform analysis
    category_analysis = df.groupby('Clothes Category').agg({
        'Clothes Assigned': ['count', 'mean', 'std'],
        'Time Needed (in days)': ['mean', 'std'],
        'Working Time per Clothes (in hours)': ['mean', 'std'],
        'Working time per day (in hours)': ['mean', 'std']
    }).round(2)
    
    print("Summary by Clothes Category:")
    print(category_analysis)
    
    # Top clothing types by quantity
    top_clothes = df.groupby('Clothes Type').agg({
        'Clothes Assigned': 'sum',
        'Time Needed (in days)': 'mean'
    }).sort_values('Clothes Assigned', ascending=False)
    
    print(f"\nTop 10 Clothing Types by Total Quantity:")
    print(top_clothes.head(10))

def analyze_worker_performance(df):
    """
    Analyze worker/tailor performance
    """
    print(f"\n{'='*50}")
    print("WORKER PERFORMANCE ANALYSIS")
    print(f"{'='*50}")
    
    # Worker analysis
    worker_stats = df.groupby('Name').agg({
        'Clothes Assigned': ['count', 'sum', 'mean'],
        'Time Needed (in days)': 'mean',
        'Working Time per Clothes (in hours)': 'mean',
        'Working time per day (in hours)': 'mean'
    }).round(2)
    
    # Rename columns for clarity
    worker_stats.columns = ['Projects_Count', 'Total_Clothes_Assigned', 'Avg_Clothes_Per_Project',
                           'Avg_Time_Needed_Days', 'Avg_Hours_Per_Clothing', 'Avg_Daily_Working_Hours']
    
    print(f"Total Unique Workers: {len(worker_stats)}")
    print(f"Average Projects per Worker: {worker_stats['Projects_Count'].mean():.2f}")
    
    # Top performers by total clothes assigned
    top_workers = worker_stats.sort_values('Total_Clothes_Assigned', ascending=False).head(10)
    print(f"\nTop 10 Workers by Total Clothes Assigned:")
    print(top_workers[['Projects_Count', 'Total_Clothes_Assigned', 'Avg_Time_Needed_Days']])
    
    # Analysis by specialization
    spec_analysis = df.groupby('Specialist').agg({
        'Clothes Assigned': 'mean',
        'Time Needed (in days)': 'mean',
        'Working Time per Clothes (in hours)': 'mean'
    }).round(2)
    
    print(f"\nPerformance by Specialist Type:")
    print(spec_analysis)

def analyze_productivity_metrics(df):
    """
    Analyze productivity metrics and efficiency
    """
    print(f"\n{'='*50}")
    print("PRODUCTIVITY METRICS ANALYSIS")
    print(f"{'='*50}")
    
    # Productivity metrics
    print(f"Overall Productivity Metrics:")
    print(f"- Average Clothes per Day: {df['Productivity_Rate'].mean():.2f}")
    print(f"- Average Hours per Day: {df['Daily_Working_Hours'].mean():.2f}")
    print(f"- Average Hours per Clothing: {df['Hours_per_Clothing'].mean():.2f}")
    print(f"- Average Effective Hours per Day: {df['Effective_Hours_Per_Day'].mean():.2f}")
    
    # Productivity by category
    productivity_by_category = df.groupby('Clothes Category').agg({
        'Productivity_Rate': 'mean',
        'Effective_Hours_Per_Day': 'mean',
        'Hours_per_Clothing': 'mean'
    }).round(2)
    
    print(f"\nProductivity by Category:")
    print(productivity_by_category)
    
    # Efficiency ratios
    df['Efficiency_Ratio'] = df['Daily_Working_Hours'] / df['Hours_per_Clothing']
    print(f"\nAverage Efficiency Ratio (Daily Hours / Hours per Clothing): {df['Efficiency_Ratio'].mean():.2f}")
    
    # Identify most efficient workers
    worker_efficiency = df.groupby('Name').agg({
        'Efficiency_Ratio': 'mean',
        'Productivity_Rate': 'mean',
        'Clothes Assigned': 'sum'
    }).round(2)
    
    top_efficient_workers = worker_efficiency.sort_values('Efficiency_Ratio', ascending=False).head(10)
    print(f"\nTop 10 Most Efficient Workers (by Efficiency Ratio):")
    print(top_efficient_workers)

if __name__ == "__main__":
    df_analyzed = analyze_geo_data()