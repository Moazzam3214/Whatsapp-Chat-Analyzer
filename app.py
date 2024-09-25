import streamlit as st
from preprocessor import preprocessor, filter_by_date
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.markdown("Analyze your WhatsApp chat data easily.")
uploaded_file = st.sidebar.file_uploader(
    "Upload a WhatsApp chat file (text format)", type="txt")

if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor(data)

        # Add date filter
        st.sidebar.header("Date Filter")
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        start_date = st.sidebar.date_input(
            "Start date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input(
            "End date", max_date, min_value=min_date, max_value=max_date)

        # Convert date inputs to datetime
        start_datetime = datetime.datetime.combine(
            start_date, datetime.time.min)
        end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

        # Filter DataFrame based on date range
        df = filter_by_date(df, start_datetime, end_datetime)

        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.remove("group_notification")
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox(
            "Select user for analysis", user_list)

        if st.sidebar.button("Show Analysis"):
            # Filter out group notifications
            df = df[df['user'] != 'group_notification']

            # Filter the DataFrame for the selected user
            if selected_user != "Overall":
                df = df[df['user'] == selected_user]

            with st.spinner('Analyzing the data...'):
                num_messages, num_words, num_media, num_links = helper.fetch_stats(
                    df)

            st.markdown("### Analysis Summary")
            metrics = {
                "Total Messages": num_messages,
                "Total Words": num_words,
                "Media Shared": num_media,
                "Total Links": num_links
            }
            cols = st.columns(len(metrics))
            for i, (key, value) in enumerate(metrics.items()):
                cols[i].metric(key, value)

            col1, col2 = st.columns(2)
            with col1:
                helper.display_bar_plot("Most Busy Day", helper.fetch_most_busy_day(
                    df), "Day", "Number of Messages", "viridis")

            with col2:
                helper.display_bar_plot("Most Busy Month", helper.fetch_most_busy_month(
                    df), "Month", "Number of Messages", "coolwarm_r")

            if selected_user == "Overall":
                col1, col2 = st.columns(2)
                with col1:
                    x, busy_user_df = helper.fetch_most_busy_user(df)
                    helper.display_bar_plot(
                        "Most Busy User", x, "Users", "Number of Messages", "viridis")

                with col2:
                    st.markdown("### Most Busy User Percentage")
                    st.dataframe(busy_user_df)

            st.markdown("### Word Cloud")
            df_wc = helper.fetch_wordcloud(df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            st.markdown("### Emojis")
            emoji_df = helper.fetch_emojis(df)
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                st.markdown("### Emoji Distribution")
                if not emoji_df.empty:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df['Count'].head(5),
                           labels=emoji_df['Emoji'].head(5), startangle=90, autopct='%1.1f%%')
                    # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.axis('equal')
                    plt.title("Emoji Distribution")
                    st.pyplot(fig)
                else:
                    st.write("No emojis found in the selected data.")

            st.markdown('### Monthly Timeline')
            monthly_timeline_df = helper.fetch_monthly_timeline(df)
            helper.display_line_plot(monthly_timeline_df['time'], monthly_timeline_df['message'],
                                     "Monthly Timeline", "Time", "Number of Messages", "red")

            st.markdown('### Weekly Timeline')
            weekly_timeline_df = helper.fetch_weekly_timeline(df)
            helper.display_line_plot(weekly_timeline_df['year_month_week'], weekly_timeline_df['message'],
                                     "Weekly Timeline", "Time", "Number of Messages", "green")

            st.markdown('### Daily timeline')
            daily_timeline_df = helper.fetch_daily_timeline(df)
            helper.display_line_plot(daily_timeline_df['year_month_day'], daily_timeline_df['message'],
                                     "Daily Timeline", "Time", "Number of Messages", "blue")

            st.markdown('### Hourly Activity of Day')
            hourly_activity_of_day_df = helper.fetch_hourly_activity_of_day(df)
            helper.display_heatmap(
                hourly_activity_of_day_df, "Hourly Activity of Day", "Hour", "Number of Messages")

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("Please upload a .txt file to begin analysis.")
