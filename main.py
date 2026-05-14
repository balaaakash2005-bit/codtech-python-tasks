<<<<<<< HEAD
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

print("\n" + "🌍 "*15)
print("WEATHER DASHBOARD")
print("🌍 "*15)

print("\n✅ You can search ANY city in the WORLD!")
print("   (India: Chennai, Mumbai, Delhi | Worldwide: London, Paris, Tokyo, Sydney, etc.)\n")

CITY = input("📍 Enter city name: ").strip()

if not CITY:
    print("❌ City name cannot be empty!")
    exit()

print(f"\n🔄 Fetching weather data for {CITY}...\n")


def get_weather_data(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("✅ Weather data received successfully!\n")
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Message: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Network error: {e}")
        return None


def extract_weather(data):
    if data is None:
        return None
    
    weather = {
        'city': data['name'],
        'country': data['sys'].get('country', ''),
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'clouds': data['clouds']['all'],
        'description': data['weather'][0]['description']
    }
    
    return weather


def display_weather(weather):
    print("="*55)
    print(f"🌍 {weather['city']}, {weather['country']}")
    print("="*55)
    print(f"🌡️  Temperature: {weather['temp']}°C")
    print(f"🤔 Feels Like: {weather['feels_like']}°C")
    print(f"📊 Min/Max: {weather['temp_min']}°C / {weather['temp_max']}°C")
    print(f"💧 Humidity: {weather['humidity']}%")
    print(f"🌪️  Wind Speed: {weather['wind_speed']} m/s")
    print(f"☁️  Cloud Cover: {weather['clouds']}%")
    print(f"🎚️ Pressure: {weather['pressure']} hPa")
    print(f"🌤️  Condition: {weather['description'].upper()}")
    print("="*55 + "\n")


def chart_temperature(weather):
    fig, ax = plt.subplots(figsize=(11, 6))
    
    temps = [weather['temp_min'], weather['temp'], weather['temp_max']]
    labels = ['Min Temp', 'Current', 'Max Temp']
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    bars = ax.bar(labels, temps, color=colors, alpha=0.85, edgecolor='black', linewidth=2.5)
    
    ax.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=13)
    ax.set_title(f'🌡️ Temperature Levels - {weather["city"]}', fontweight='bold', fontsize=15)
    ax.set_ylim(0, max(temps) + 12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar, temp in zip(bars, temps):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{temp}°C', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('temperature_chart.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved: temperature_chart.png")
    plt.close()


def chart_humidity(weather):
    fig, ax = plt.subplots(figsize=(9, 7))
    
    humidity = weather['humidity']
    values = [humidity, 100 - humidity]
    labels = [f'Humid\n{humidity}%', f'Dry\n{100-humidity}%']
    colors = ['#3498db', '#ecf0f1']
    explode = (0.05, 0)
    
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', 
           startangle=90, explode=explode, textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    ax.set_title(f'💧 Humidity Level - {weather["city"]}', fontweight='bold', fontsize=15, pad=20)
    
    plt.tight_layout()
    plt.savefig('humidity_chart.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved: humidity_chart.png")
    plt.close()


def chart_metrics(weather):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'🌤️ Weather Metrics - {weather["city"]}', fontweight='bold', fontsize=15, y=1.00)
    
    ax1 = axes[0]
    wind = weather['wind_speed']
    ax1.barh(['Wind Speed'], [wind], color='#2ecc71', alpha=0.85, edgecolor='black', linewidth=2.5, height=0.5)
    ax1.set_xlabel('Speed (m/s)', fontweight='bold', fontsize=12)
    ax1.set_title('🌪️ Wind Speed', fontweight='bold', fontsize=13)
    ax1.set_xlim(0, max(wind + 5, 15))
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.text(wind/2, 0, f'{wind} m/s', ha='center', va='center', 
            fontweight='bold', color='white', fontsize=13)
    
    ax2 = axes[1]
    cloud = weather['clouds']
    ax2.barh(['Cloud Cover'], [cloud], color='#95a5a6', alpha=0.85, edgecolor='black', linewidth=2.5, height=0.5)
    ax2.set_xlabel('Percentage (%)', fontweight='bold', fontsize=12)
    ax2.set_xlim(0, 100)
    ax2.set_title('☁️ Cloud Cover', fontweight='bold', fontsize=13)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.text(cloud/2, 0, f'{cloud}%', ha='center', va='center', 
            fontweight='bold', color='white', fontsize=13)
    
    plt.tight_layout()
    plt.savefig('metrics_chart.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved: metrics_chart.png")
    plt.close()


def chart_summary(weather):
    data = {
        'Parameter': [
            'Temperature',
            'Feels Like',
            'Min Temp',
            'Max Temp',
            'Humidity',
            'Pressure',
            'Wind Speed',
            'Cloud Cover',
            'Condition'
        ],
        'Value': [
            f"{weather['temp']}°C",
            f"{weather['feels_like']}°C",
            f"{weather['temp_min']}°C",
            f"{weather['temp_max']}°C",
            f"{weather['humidity']}%",
            f"{weather['pressure']} hPa",
            f"{weather['wind_speed']} m/s",
            f"{weather['clouds']}%",
            weather['description'].upper()
        ]
    }
    
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=df.values.tolist(), colLabels=list(df.columns),
                    cellLoc='center', loc='center',
                    colWidths=[0.35, 0.35])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)
    
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white', fontsize=12)
    
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
            else:
                table[(i, j)].set_facecolor('#ffffff')
            table[(i, j)].set_text_props(fontsize=11)
    
    plt.title(f'📋 Weather Summary - {weather["city"]}', 
             fontweight='bold', fontsize=15, pad=25)
    
    plt.tight_layout()
    plt.savefig('summary_table.png', dpi=300, bbox_inches='tight')
    print("✅ Chart saved: summary_table.png")
    plt.close()


if __name__ == "__main__":
    
    if not API_KEY:
        print("❌ ERROR: API_KEY not found!")
        print("Please create .env file with API_KEY=your_key")
        exit()
    
    weather_data = get_weather_data(CITY)
    
    if weather_data is None:
        print(f"❌ Failed to fetch weather data for '{CITY}'!")
        print("Please check:")
        print("  1. City name spelling")
        print("  2. Internet connection")
        print("  3. API key validity")
        exit()
    
    weather = extract_weather(weather_data)
    
    if weather is None:
        print("❌ Failed to extract weather info!")
        exit()
    
    display_weather(weather)
    
    print("🎨 Creating visualizations...\n")
    chart_temperature(weather)
    chart_humidity(weather)
    chart_metrics(weather)
    chart_summary(weather)
    
    print("\n" + "✅ "*20)
    print("ALL CHARTS CREATED SUCCESSFULLY!")
    print("✅ "*20)
    print("\n📊 Generated files:")
    print("   1. temperature_chart.png")
    print("   2. humidity_chart.png")
    print("   3. metrics_chart.png")
    print("   4. summary_table.png")
    print("\n🎯 Task 1 COMPLETE!\n")
=======
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# -----------------------------
# READ CSV FILE
# -----------------------------

data = pd.read_csv("students.csv")

# -----------------------------
# CALCULATIONS
# -----------------------------

data["Total"] = (
    data["Python"] +
    data["Java"] +
    data["DBMS"]
)

data["Average"] = round(
    data["Total"] / 3,
    2
)

# -----------------------------
# GRADE SYSTEM
# -----------------------------

grades = []

for avg in data["Average"]:

    if avg >= 90:
        grades.append("A")

    elif avg >= 80:
        grades.append("B")

    elif avg >= 70:
        grades.append("C")

    else:
        grades.append("D")

data["Grade"] = grades

# -----------------------------
# PASS / FAIL
# -----------------------------

status_list = []

for avg in data["Average"]:

    if avg >= 40:
        status_list.append("PASS")

    else:
        status_list.append("FAIL")

data["Status"] = status_list

# -----------------------------
# RANK SYSTEM
# -----------------------------

data["Rank"] = data["Total"].rank(
    ascending=False,
    method="dense"
).astype(int)

data = data.sort_values(by="Rank")

# -----------------------------
# STATISTICS
# -----------------------------

total_students = len(data)

passed_students = (
    data["Status"] == "PASS"
).sum()

failed_students = (
    data["Status"] == "FAIL"
).sum()

class_average = round(
    data["Average"].mean(),
    2
)

# -----------------------------
# TOPPER
# -----------------------------

topper = data.iloc[0]

# -----------------------------
# CREATE PDF
# -----------------------------

pdf = FPDF()

pdf.add_page()

# -----------------------------
# TITLE
# -----------------------------

pdf.set_font("Arial", "B", 20)

pdf.set_text_color(0, 51, 102)

pdf.cell(
    200,
    10,
    "STUDENT REPORT",
    ln=True,
    align="C"
)

pdf.ln(5)

# DATE

pdf.set_font("Arial", "", 11)

current_time = datetime.now().strftime(
    "%d-%m-%Y %I:%M %p"
)

pdf.cell(
    200,
    10,
    f"Generated On: {current_time}",
    ln=True
)

pdf.ln(8)

# -----------------------------
# TABLE HEADER
# -----------------------------

pdf.set_fill_color(0, 102, 204)

pdf.set_text_color(255, 255, 255)

pdf.set_font("Arial", "B", 10)

pdf.cell(30, 10, "Name", 1, 0, "C", True)
pdf.cell(20, 10, "Py", 1, 0, "C", True)
pdf.cell(20, 10, "Java", 1, 0, "C", True)
pdf.cell(20, 10, "DBMS", 1, 0, "C", True)
pdf.cell(22, 10, "Total", 1, 0, "C", True)
pdf.cell(22, 10, "Avg", 1, 0, "C", True)
pdf.cell(18, 10, "Grade", 1, 0, "C", True)
pdf.cell(25, 10, "Status", 1, 0, "C", True)
pdf.cell(15, 10, "Rank", 1, 1, "C", True)

# -----------------------------
# TABLE DATA
# -----------------------------

pdf.set_font("Arial", "", 10)

pdf.set_text_color(0, 0, 0)

for index, row in data.iterrows():

    pdf.cell(30, 10, str(row["Name"]), 1)
    pdf.cell(20, 10, str(row["Python"]), 1)
    pdf.cell(20, 10, str(row["Java"]), 1)
    pdf.cell(20, 10, str(row["DBMS"]), 1)
    pdf.cell(22, 10, str(row["Total"]), 1)
    pdf.cell(22, 10, str(row["Average"]), 1)
    pdf.cell(18, 10, str(row["Grade"]), 1)
    pdf.cell(25, 10, str(row["Status"]), 1)
    pdf.cell(15, 10, str(row["Rank"]), 1)

    pdf.ln()

# -----------------------------
# TOPPER SECTION
# -----------------------------

pdf.ln(10)

pdf.set_font("Arial", "B", 14)

pdf.set_text_color(0, 51, 102)

pdf.cell(
    200,
    10,
    "TOPPER DETAILS",
    ln=True
)

pdf.set_font("Arial", "", 12)

pdf.set_text_color(0, 0, 0)

pdf.cell(
    200,
    10,
    f"Topper Name : {topper['Name']}",
    ln=True
)

pdf.cell(
    200,
    10,
    f"Total Marks : {topper['Total']}",
    ln=True
)

pdf.cell(
    200,
    10,
    f"Grade : {topper['Grade']}",
    ln=True
)

# -----------------------------
# STATISTICS
# -----------------------------

pdf.ln(8)

pdf.set_font("Arial", "B", 14)

pdf.set_text_color(0, 51, 102)

pdf.cell(
    200,
    10,
    "CLASS STATISTICS",
    ln=True
)

pdf.set_font("Arial", "", 12)

pdf.set_text_color(0, 0, 0)

pdf.cell(
    200,
    10,
    f"Total Students : {total_students}",
    ln=True
)

pdf.cell(
    200,
    10,
    f"Passed Students : {passed_students}",
    ln=True
)

pdf.cell(
    200,
    10,
    f"Failed Students : {failed_students}",
    ln=True
)

pdf.cell(
    200,
    10,
    f"Class Average : {class_average}",
    ln=True
)

# -----------------------------
# SAVE PDF
# -----------------------------

pdf.output("report.pdf")

print("Professional PDF Generated Successfully!")
>>>>>>> c22d016 (Task 2 completed)
