import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def load_and_prepare_data(filepath):
    """
    Load marketing campaign data and variable descriptions.
    
    Args:
        filepath (str): Path to the marketing campaign CSV file
    
    Returns:
        pd.DataFrame: Processed marketing campaign data
    """
    # Load the data
    df = pd.read_csv(filepath)
    
    # Basic data type conversions and cleaning
    numeric_columns = [
        'Campaign_Budget', 'Ad_Click_Rate', 'Conversion_Rate', 
        'Social_Media_Followers', 'Email_Open_Rate', 'Customer_Retention_Rate'
    ]
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def generate_comprehensive_analysis(df):
    """
    Generate a comprehensive analysis of marketing campaign data.
    
    Args:
        df (pd.DataFrame): Marketing campaign data
    
    Returns:
        dict: Comprehensive analysis results
    """
    analysis = {}
    
    # 1. Overall Campaign Performance Metrics
    analysis['overall_performance'] = {
        'total_budget': df['Campaign_Budget'].sum(),
        'average_budget': df['Campaign_Budget'].mean(),
        'average_click_rate': df['Ad_Click_Rate'].mean(),
        'average_conversion_rate': df['Conversion_Rate'].mean(),
        'average_retention_rate': df['Customer_Retention_Rate'].mean()
    }
    
    # 2. Performance by Platform
    analysis['platform_performance'] = df.groupby('Platform').agg({
        'Campaign_Budget': ['mean', 'sum'],
        'Ad_Click_Rate': 'mean',
        'Conversion_Rate': 'mean',
        'Customer_Retention_Rate': 'mean'
    }).reset_index()
    
    # 3. Performance by Campaign Type
    analysis['campaign_type_performance'] = df.groupby('Campaign_Type').agg({
        'Campaign_Budget': ['mean', 'sum'],
        'Ad_Click_Rate': 'mean',
        'Conversion_Rate': 'mean',
        'Customer_Retention_Rate': 'mean'
    }).reset_index()
    
    # 4. Performance by Target Audience
    analysis['audience_performance'] = df.groupby('Target_Audience').agg({
        'Campaign_Budget': ['mean', 'sum'],
        'Ad_Click_Rate': 'mean',
        'Conversion_Rate': 'mean',
        'Customer_Retention_Rate': 'mean',
        'Social_Media_Followers': 'mean'
    }).reset_index()
    
    # 5. Correlation Analysis
    analysis['correlation_matrix'] = df[['Campaign_Budget', 'Ad_Click_Rate', 
                                         'Conversion_Rate', 'Social_Media_Followers', 
                                         'Email_Open_Rate', 'Customer_Retention_Rate']].corr()
    
    return analysis

def visualize_results(df, analysis):
    """
    Create visualizations of marketing campaign data.
    
    Args:
        df (pd.DataFrame): Marketing campaign data
        analysis (dict): Comprehensive analysis results
    """
    # 1. Budget Distribution by Campaign Type
    plt.figure(figsize=(12, 6))
    df.boxplot(column='Campaign_Budget', by='Campaign_Type')
    plt.title('Campaign Budget Distribution by Campaign Type')
    plt.suptitle('')  # Remove automatic suptitle
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('budget_distribution.png')
    plt.close()
    
    # 2. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(analysis['correlation_matrix'], cmap='coolwarm', aspect='auto')
    plt.colorbar()
    plt.title('Correlation Matrix of Marketing Metrics')
    plt.xticks(range(len(analysis['correlation_matrix'].columns)), 
               analysis['correlation_matrix'].columns, rotation=45)
    plt.yticks(range(len(analysis['correlation_matrix'].columns)), 
               analysis['correlation_matrix'].columns)
    
    # Add correlation values to the heatmap
    for i in range(len(analysis['correlation_matrix'].columns)):
        for j in range(len(analysis['correlation_matrix'].columns)):
            plt.text(j, i, f'{analysis["correlation_matrix"].iloc[i, j]:.2f}', 
                     ha='center', va='center', color='black')
    
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()
    
    # 3. Conversion Rate by Platform
    plt.figure(figsize=(10, 6))
    platform_conversion = df.groupby('Platform')['Conversion_Rate'].mean().sort_values(ascending=False)
    platform_conversion.plot(kind='bar')
    plt.title('Average Conversion Rate by Platform')
    plt.xlabel('Platform')
    plt.ylabel('Conversion Rate (%)')
    plt.tight_layout()
    plt.savefig('conversion_rate_by_platform.png')
    plt.close()

def main(filepath='marketing_data.csv'):
    """
    Main function to run the marketing campaign data analysis.
    
    Args:
        filepath (str, optional): Path to the marketing campaign CSV file
    """
    print("Marketing Campaign Data Analysis")
    print("================================")

    try:
        # Load data
        df = load_and_prepare_data(filepath)
        
        # Generate comprehensive analysis
        analysis = generate_comprehensive_analysis(df)
        
        # Print overall performance
        print("\nOverall Campaign Performance:")
        for metric, value in analysis['overall_performance'].items():
            print(f"{metric.replace('_', ' ').title()}: {value:.2f}")
        
        print("\n--- Platform Performance ---")
        print(analysis['platform_performance'].to_string(index=False))
        
        print("\n--- Campaign Type Performance ---")
        print(analysis['campaign_type_performance'].to_string(index=False))
        
        print("\n--- Target Audience Performance ---")
        print(analysis['audience_performance'].to_string(index=False))
        
        # Create visualizations
        visualize_results(df, analysis)
        print("\nVisualizations have been saved in the current directory.")
        
        # Pause to keep window open
        print("\nPress Ctrl+C to exit the program...")
        while True:
            pass
    
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Please ensure the file is in the correct directory.")
        print("\nPress any key to exit...")
        input()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("\nPress any key to exit...")
        input()

# Modify the script's behavior when run directly
if __name__ == "__main__":
    main()
    sys.exit(0)