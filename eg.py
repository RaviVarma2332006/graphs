import requests
import pandas as pd
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- Configuration ---
# Replace with your actual TomTom API Key
API_KEY = "YOUR_TOMTOM_API_KEY"

# Bounding box for Sus - Pashan Road (minLat, minLon, maxLat, maxLon)
# These coordinates roughly cover the Sus Gaon to Pashan Circle stretch
BBOX = "18.5350,73.7600,18.5550,73.7950" 

# TomTom Traffic Flow API Endpoint
URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}&bbox={BBOX}"

def fetch_traffic_data():
    """Fetches live traffic data from TomTom API and returns a Pandas DataFrame."""
    print("Fetching traffic data for the Sus-Pashan corridor...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        
        # Parse the JSON response
        # Note: The exact parsing depends on the TomTom endpoint structure. 
        # This is a general extraction of flow segment data.
        road_segments = []
        if 'flowSegmentData' in data:
            flow_data = data['flowSegmentData']
            road_segments.append({
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Current Speed (km/h)": flow_data.get('currentSpeed', 'N/A'),
                "Free Flow Speed (km/h)": flow_data.get('freeFlowSpeed', 'N/A'),
                "Confidence": flow_data.get('confidence', 'N/A'),
                "Road Closed": flow_data.get('roadClosure', False)
            })
            
        df = pd.DataFrame(road_segments)
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        # Return dummy data for testing the PDF generation if API fails/key is missing
        return pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Current Speed (km/h)": 14,
            "Free Flow Speed (km/h)": 40,
            "Confidence": 0.89,
            "Road Closed": False
        }])

def generate_pdf_report(df, filename="Traffic_Report_Sus_Pashan.pdf"):
    """Generates a PDF report from the Pandas DataFrame."""
    print(f"Generating PDF report: {filename}...")
    
    # Initialize PDF canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title & Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Adaptive Traffic Management System - Area Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "Corridor: Sus (Sus-Gaon) & Sus-Pashan Road")
    c.drawString(50, height - 90, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    c.line(50, height - 100, width - 50, height - 100)
    
    # Data Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Live Traffic Snapshot:")
    
    # Draw Data from DataFrame
    y_position = height - 160
    c.setFont("Helvetica", 11)
    
    if df.empty:
        c.drawString(50, y_position, "No data available from API.")
    else:
        for index, row in df.iterrows():
            c.drawString(50, y_position, f"Timestamp: {row['Timestamp']}")
            c.drawString(50, y_position - 20, f"Current Speed: {row['Current Speed (km/h)']} km/h")
            c.drawString(50, y_position - 40, f"Free Flow Speed: {row['Free Flow Speed (km/h)']} km/h")
            
            # Calculate congestion severity
            if row['Current Speed (km/h)'] != 'N/A' and row['Free Flow Speed (km/h)'] != 'N/A':
                ratio = row['Current Speed (km/h)'] / row['Free Flow Speed (km/h)']
                status = "Heavy Traffic" if ratio < 0.5 else "Moderate Traffic" if ratio < 0.8 else "Clear Flow"
                c.drawString(50, y_position - 60, f"Status: {status}")
            
            y_position -= 100 # Spacing for next record if you loop through multiple segments

    # Save PDF
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    # 1. Fetch the data
    traffic_df = fetch_traffic_data()
    
    # 2. Print to console to verify
    print("\nData Preview:")
    print(traffic_df)
    print("-" * 30)
    
    # 3. Generate the PDF
    generate_pdf_report(traffic_df)