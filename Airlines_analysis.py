import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import matplotlib.cm as cm
from gtts import gTTS
from io import BytesIO

import warnings
warnings.filterwarnings('ignore')
conn = sqlite3.connect("travel.sqlite")
cursor = conn.cursor()


cursor.execute("""select name from sqlite_master where type ='table';""")
print('List of tables present in the database')
table_list = [table[0] for table in cursor.fetchall()]
print(table_list)

tables = pd.read_sql("""SELECT *
                        FROM sqlite_master
                        WHERE type='table';""", conn)

def tables(table_name, conn):
    # iterating over each available table in the list
    for table in table_name:
        # storing the table into a dataframe by reading them using the read_sql_query
        df = pd.read_sql_query(f"""select * from {table}""", conn)
        # introducing a global variable

        globals()[table] = df
    return dict

table_names = ['aircrafts_data','boarding_passes','bookings','flights','seats','ticket_flights','tickets']
tables(table_names, conn)

# print(aircrafts_data)
airports_data = pd.read_sql_query("select * from airports_data", conn)
airports_data['airport_name'] = airports_data['airport_name'].apply(lambda x: json.loads(x)['en'])
airports_data['city'] = airports_data['city'].apply(lambda x: json.loads(x)['en'])
# airports_data


aircrafts_data = pd.read_sql_query("select * from aircrafts_data", conn)
aircrafts_data['model'] = aircrafts_data['model'].apply(lambda x: eval(x)["en"])
# aircrafts_data


def main():
    def problem_statement():
        st.title("Airlines Data Analysis for profit Maximization")
        st.caption("Developed by Sudeep | GitHub: [Sudeepkr101](https://github.com/Sudeepkr101)")
            # Set seaborn style
        st.image("logo.jpeg", width=700)
        st.subheader("Key Obstacles")
        st. write("1. Stricter environmental regulations: The airlines industry is facing increasing pressure to reduce its carbon footprint, leading to the implementation of more stringent environmental laws. These regulations not only raise operating costs but also restrict the potential for expansion.")

        st. write("2. Higher flight taxes: Governments worldwide are imposing heavier taxes on aircraft as a means to address environmental concerns and generate revenue. This increase in flight taxes has raised the overall cost of flying, subsequently reducing demand.")

        st. write("3. Tight labor market resulting in increased labor costs: The aviation sector is experiencing a scarcity of skilled workers, leading to higher labor costs and an increase in turnover rates.")

    # Function to generate audio from text
    def generate_audio(text):
        tts = gTTS(text=text, lang='en')
        audio_bytes_io = BytesIO()
        tts.write_to_fp(audio_bytes_io)
        return audio_bytes_io
    

    

    def obs_1():
        
        sns.set_style('whitegrid')

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='model', y='range', data=aircrafts_data, palette='crest', color='purple', ax=ax)
        for container in ax.containers:
            ax.bar_label(container)
        # Customize plot
        st.subheader('Airplane Models with Their Ranges')
        plt.title('Airplane Models with Their Ranges')
        plt.xticks(rotation=45)

        # Display plot using st.pyplot()
        st.pyplot(fig)

        st.subheader("Planes having more than 120 seats")
        df = pd.read_sql_query("""select aircraft_code, count(*) as num_seats from seats
                            group by aircraft_code having num_seats >120""", conn)

        df.to_csv('aircraft_seats.csv')
        # Set seaborn style
        sns.set_style('whitegrid')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='aircraft_code', y='num_seats', data=df, palette='crest', ax=ax)
        for container in ax.containers:
            ax.bar_label(container)

        # Customize plot
        plt.title('Aircraft Codes vs Number of Seats')
        plt.xticks(rotation=45)

        # Display plot using st.pyplot()
        st.pyplot(fig)

        crafts = pd.read_sql("""
                        SELECT a.aircraft_code, a.model->'en' AS model_name, s.num_seats
                        FROM aircrafts_data a
                        JOIN (
                            SELECT aircraft_code, COUNT(*) AS num_seats
                            FROM seats
                            GROUP BY aircraft_code
                        ) s
                        ON a.aircraft_code = s.aircraft_code
                        WHERE a.aircraft_code IN ( 320, 321, 733, 763, 773)
                        """, conn)

        crafts
        # Observation text
        observation_text = """
        Here we successfully derived the names of airplanes using their codes
        So it seems like " Boeing 777-300 " is having maximum number of seats (402)."""

        # Button text
        st.subheader("Observation 1")
        button_text = "Listen Conclusion 1"

        # Button to play/pause audio
        button_clicked = st.button(button_text)

        # Play audio if button is clicked
        if button_clicked:
            audio_bytes_io = generate_audio(observation_text)
            st.audio(audio_bytes_io, format='audio/mp3', start_time=0)

        # Optionally, you can display the text in the app as well
        # st.text(observation_text)

    def obs_2():
        st.subheader("Number of tickets booked and total amount earned changed with the time")

        crafts = pd.read_sql("""SELECT aircraft_code, model
                            FROM aircrafts_data
                            where aircraft_code IN (319, 320, 321, 733, 763, 773);""", conn)
        tickets = pd.read_sql_query("""select * from tickets inner join bookings
                        on tickets.book_ref = bookings.book_ref""", conn)

        tickets['book_date'] = pd.to_datetime(tickets['book_date'])
        tickets['date'] = tickets['book_date'].dt.date
        tickets_count = tickets.groupby('date')[['date']].count()

        # Plotting
        plt.figure(figsize=(18, 6))
        plt.fill_between(tickets_count.index, tickets_count['date'], color=plt.colormaps['crest'](0.5), alpha=0.3)
        plt.plot(tickets_count.index, tickets_count['date'], color=plt.colormaps['crest'](0.5), linewidth=2, marker='o', markersize=8)
        plt.title('Number of Tickets Booked on Each Date', fontsize=30)
        plt.xlabel('Date', fontsize=20)
        plt.ylabel('Number of Tickets', fontsize=20)
        plt.grid('b')

        # Display plot using st.pyplot()
        st.pyplot(plt)


        # Load bookings data
        bookings = pd.read_sql_query("select * from bookings", conn)

        # Convert 'book_date' to datetime and extract date
        bookings['book_date'] = pd.to_datetime(bookings['book_date'])
        bookings['date'] = bookings['book_date'].dt.date

        # Group by date and calculate total amount earned
        booking_amount = bookings.groupby('date')[['total_amount']].sum()

        # Plotting
        plt.figure(figsize=(18, 6))
        plt.fill_between(booking_amount.index, booking_amount['total_amount'], color=plt.colormaps['crest'](0.5), alpha=0.3)
        plt.title('Total Amount Earned on Each Date', fontsize=30)
        plt.xlabel('Date', fontsize=20)
        plt.ylabel('Total Amount Earned', fontsize=20)
        plt.grid('b')

        # Display plot using st.pyplot()
        st.pyplot(plt)

        st.subheader("Observation 2")

        observation_text_2 = "Utilized a line chart visualization to analyze the trend of ticket bookings and revenue earned. The number of tickets booked showed a gradual increase from June 22nd to July 7th. From July 8th until August, ticket bookings remained relatively stable with a noticeable peak in bookings on a single day. The revenue earned by the company is closely correlated with the number of tickets booked."
        # Button text
        button_text_2 = "Listen Conclusion 2"

        # Button to play/pause audio
        button_clicked_2 = st.button(button_text_2)

        # Play audio if button is clicked
        if button_clicked_2:
            audio_bytes_io_2 = generate_audio(observation_text_2)
            st.audio(audio_bytes_io_2, format='audio/mp3', start_time=0)


    def obs_3():
        # Display class-wise average flight prices
        st.subheader("Fare Distribution for the Flights")
        df = pd.read_csv('fare_avg_amount.csv')
        sns.set_style('whitegrid')
        fig, axes = plt.subplots(figsize=(12, 8))
        ax = sns.barplot(x='aircraft_code', y='avg(amount)', hue='fare_conditions', data=df, palette='crest')
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Class wise Average Flight Prices')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        crafts_3 = pd.read_sql("""SELECT aircraft_code, model->'en'
                            FROM aircrafts_data
                            where aircraft_code IN (319, 321, 733, 763, 773, 'CN1', 'CR2', 'SU9');
        """, conn)
        crafts_3
        

        st.subheader("Observation 3")
        observation_text_3 = """
        Here we successfully derived the names of airplanes using their codes
        So it seems like " Airbus A319-100 " is having maximum average number of Business class seats.
        Also " Airbus A319-100 " is having maximum average number of Economy seats.
        And " Boeing 777-300 " is having maximum number of Comfort seats.
    """
        button_text_3 = "Listen Conclusion 3"

        # Button to play/pause audio
        button_clicked_3 = st.button(button_text_3)

        # Play audio if button is clicked
        if button_clicked_3:
            audio_bytes_io_3 = generate_audio(observation_text_3)
            st.audio(audio_bytes_io_3, format='audio/mp3', start_time=0)

    def obs_4():
        occupancy_rate = pd.read_sql_query("""select a.aircraft_code,avg(a.seats_count) as booked_seats, b.num_seats, avg(a.seats_count)/b.num_seats as occupancy_rate from
                    (select aircraft_code,flights.flight_id,count(*) as seats_count from boarding_passes
                        inner join flights
                        on boarding_passes.flight_id = flights.flight_id
                        group by aircraft_code,flights.flight_id) as a
                        inner join
                        (select aircraft_code,count(*) as num_seats from seats
                        group by aircraft_code) as b
                        on a.aircraft_code = b.aircraft_code group by a.aircraft_code""", conn
                    )
        
        # Display correlation between booked seats and occupancy rate
        sns.set_style('whitegrid')
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(x="booked_seats", y="occupancy_rate", data=occupancy_rate, ax=ax)
        plt.title('Correlation between Booked Seats and Occupancy Rate')
        plt.xlabel('Booked Seats')
        plt.ylabel('Occupancy Rate')
        st.pyplot(fig)

        observation_text_4 = "as the number of booked seats increases, the occupancy rate also tends to increase. This implies that flights with more booked seats are likely to have a higher proportion of occupied seats, indicating efficient seat utilization."
        st.subheader("Observation 4")
        button_text_4 = "Listen Conclusion 4"

        # Button to play/pause audio
        button_clicked_4 = st.button(button_text_4)

        # Play audio if button is clicked
        if button_clicked_4:
            audio_bytes_io_4 = generate_audio(observation_text_4)
            st.audio(audio_bytes_io_4, format='audio/mp3', start_time=0)

    def obs_5():
        occupancy_rate = pd.read_sql_query("""select a.aircraft_code,avg(a.seats_count) as booked_seats, b.num_seats, avg(a.seats_count)/b.num_seats as occupancy_rate from
                    (select aircraft_code,flights.flight_id,count(*) as seats_count from boarding_passes
                        inner join flights
                        on boarding_passes.flight_id = flights.flight_id
                        group by aircraft_code,flights.flight_id) as a
                        inner join
                        (select aircraft_code,count(*) as num_seats from seats
                        group by aircraft_code) as b
                        on a.aircraft_code = b.aircraft_code group by a.aircraft_code""", conn
                    )
        total_revenue = pd.read_sql_query("""select aircraft_code,sum(amount) as total_revenue from ticket_flights
                            join flights on ticket_flights.flight_id = flights.flight_id
                            group by aircraft_code""", conn)
        # Display occupancy rate and total revenue tables
        st.subheader('Occupancy Rate and Total Revenue')
        st.write("Occupancy Rate for each aircraft")
        # st.dataframe(occupancy_rate)

        occupancy_rate['booked_percentage'] = (occupancy_rate['booked_seats'] / occupancy_rate['num_seats']) * 100
        plt.figure(figsize=(10, 6))
        sns.barplot(x='aircraft_code', y='booked_percentage', data=occupancy_rate, palette='crest')
        plt.title('Percentage of Booked Seats for Each Aircraft')
        plt.xlabel('Aircraft Code')
        plt.ylabel('Percentage of Booked Seats')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Display plot using st.pyplot()
        st.pyplot(plt.gcf())

    
        st.write("Total Revenue Generated by Each Aircraft:")
        # st.dataframe(total_revenue)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='aircraft_code', y='total_revenue', data=total_revenue, palette='crest')
        plt.title('Revenue Generated by Each Aircraft')
        plt.xlabel('Aircraft Code')
        plt.ylabel('Total Revenue')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Adjust layout and display plot
        plt.tight_layout()
        st.pyplot(plt.gcf())  # Display the combined plot


        st.subheader("Calculating how much the total annual turnover would increase by giving all aircraft a 10% higher occupancy rate.")
        # Additional calculations and display
        occupancy_rate['inc occupancy rate'] = occupancy_rate['occupancy_rate'] + occupancy_rate['occupancy_rate'] * 0.1
        occupancy_rate['inc Total Annual Turnover'] = (total_revenue['total_revenue'] / occupancy_rate['occupancy_rate']) * occupancy_rate['inc occupancy rate']
        # st.write(occupancy_rate)
        current_total_turnover = total_revenue['total_revenue'].sum()
        # Calculate the total annual turnover with a 10% higher occupancy rate for each aircraft
        occupancy_rate['inc_occupancy_rate'] = occupancy_rate['occupancy_rate'] * 1.1
        total_revenue['inc_total_revenue'] = (total_revenue['total_revenue'] / occupancy_rate['occupancy_rate']) * occupancy_rate['inc_occupancy_rate']
        new_total_turnover = total_revenue['inc_total_revenue'].sum()

        # Calculate the increase in total annual turnover
        increase_in_turnover = new_total_turnover - current_total_turnover

        # Calculate the current total annual turnover

        # Initialize lists to store data for plotting
        aircraft_codes = []
        current_turnovers = []
        potential_turnovers = []

        # Calculate the total annual turnover for each aircraft
        for index, row in total_revenue.iterrows():
            aircraft_code = row['aircraft_code']
            current_turnover = row['total_revenue']
            potential_turnover = row['inc_total_revenue']
            
            aircraft_codes.append(aircraft_code)
            current_turnovers.append(current_turnover)
            potential_turnovers.append(potential_turnover)

        # Create plot
        plt.figure(figsize=(12, 8))

        # Plot current turnover for each aircraft
        plt.plot(aircraft_codes, current_turnovers, marker='o', linestyle='-', color='orange', label='Current Turnover')

        # Plot potential turnover with 10% increase for each aircraft
        plt.plot(aircraft_codes, potential_turnovers, marker='o', linestyle='-', color='green', label='Potential Turnover (10% Increase)')

        plt.xlabel('Aircraft Code')
        plt.ylabel('Total Annual Turnover')
        plt.title('Comparison of Current and Potential Total Annual Turnover with 10% Increase by Aircraft')
        plt.xticks(rotation=45)
        plt.legend()
        

        # Display plot
        st.pyplot(plt.gcf())
      
        # Display the results in Streamlit
        st.title("Potential Increase in Total Annual Turnover")
        st.write("Current Total Annual Turnover:" ,current_total_turnover)
        st.write("Potential Total Annual Turnover with 10% Increase in Occupancy Rate:", new_total_turnover)
        st.write("Increase in Total Annual Turnover:" ,increase_in_turnover)

    def final():    
        # Create sidebar with links to different pages
        st.sidebar.title("Analysis of Factors")
        selected_page = st.sidebar.radio("", ["Problem Statement","Model Ranges", "Revenue Earned", "Flight Prices","Booked Seats and Occupancy Rate", "Profit Maximized"])

        # # Display content based on selected page
        if selected_page == "Problem Statement":
            problem_statement()
        elif selected_page == "Model Ranges":
            obs_1()
        elif selected_page == "Revenue Earned":
            obs_2()
        elif selected_page == "Flight Prices":
            obs_3()
        elif selected_page == "Booked Seats and Occupancy Rate":
            obs_4()
        else:
            obs_5()
    
    final()
if __name__ == "__main__":
    main()



# Conclusion

# In conclusion, airlines can maximize profitability by analyzing revenue data and making informed decisions. Factors such as total revenue, average revenue per ticket, and average occupancy per aircraft play a crucial role in this analysis. By identifying areas for improvement, adjusting pricing strategies, and optimizing routes, airlines can increase their profitability. However, it's important for airlines to consider consumer happiness and safety while striving for profit. Balancing these factors is key to long-term success in the competitive airline industry. Adopting a data-driven approach to revenue analysis and optimization can lead to sustainable growth and success.
