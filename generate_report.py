import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def generate_monthly_report(month=None, year=None):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
        
    # Read the Excel file
    df = pd.read_excel("pact_tracker.xlsx")
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter for the specified month
    monthly_data = df[
        (df['date'].dt.month == month) & 
        (df['date'].dt.year == year)
    ]
    
    # Generate statistics
    total_days = len(monthly_data)
    successful_days = len(monthly_data[monthly_data['status'] == 'yes'])
    success_rate = (successful_days / total_days) * 100 if total_days > 0 else 0
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Success rate pie chart
    plt.subplot(2, 1, 1)
    plt.pie([successful_days, total_days - successful_days], 
            labels=['Success', 'Missed'],
            autopct='%1.1f%%')
    plt.title(f'Pact Success Rate for {datetime.strptime(str(month), "%m").strftime("%B")} {year}')
    
    # Daily status timeline
    plt.subplot(2, 1, 2)
    status_numeric = (monthly_data['status'] == 'yes').astype(int)
    plt.plot(monthly_data['date'], status_numeric, marker='o')
    plt.title('Daily Pact Status')
    plt.ylabel('Status (1=Success, 0=Missed)')
    plt.xticks(rotation=45)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(f'monthly_report_{year}_{month}.png')
    
    # Generate text report
    report = f"""
    Monthly Pact Report for {datetime.strptime(str(month), "%m").strftime("%B")} {year}
    =======================================
    
    Total Days Tracked: {total_days}
    Successful Days: {successful_days}
    Success Rate: {success_rate:.1f}%
    
    Key Thoughts from the Month:
    """
    
    # Add some key thoughts (last 5 successful days)
    successful_entries = monthly_data[monthly_data['status'] == 'yes'].tail(5)
    for _, entry in successful_entries.iterrows():
        report += f"\n- {entry['date'].strftime('%Y-%m-%d')}: {entry['thoughts']}"
    
    # Save the report
    with open(f'monthly_report_{year}_{month}.txt', 'w') as f:
        f.write(report)
    
    print("Report generated successfully!")

if __name__ == "__main__":
    # You can specify month and year, or leave them blank for current month
    generate_monthly_report() 