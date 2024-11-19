import pandas as pd
import streamlit as st
import plotly.express as px

# Set up Streamlit page configuration
st.set_page_config(
    page_title="NFL Player Performance",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets URL
gsheetid = "1HITWGxY2Bu5QHdj7z7FeoBBIftVde7Wa4KoO8dMpzdc"
sheetid = "291705184"
url = f"https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetid}&format"
st.write(url)

# Load data from Google Sheets
data = pd.read_csv(url)

# Custom CSS for styling the title, subtitle, and menu
st.markdown("""
    <style>
    /* Title and subtitle styles */
    .title {
        color: #1E90FF;  /* Dodger Blue */
        font-size: 48px;
        font-weight: 700;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    .subtitle {
        color: #4682B4;  /* Steel Blue */
        font-size: 24px;
        font-weight: 400;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and subtitle with custom styling
st.markdown("<h1 class='title'>NFL Player Performance Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Visualize key performance metrics for NFL players by season</h2>", unsafe_allow_html=True)

# Menu items
menu = st.sidebar.radio("Navigation", ["Home", "EDA", "Insights", "Prediction"])

if menu == "Home":
    st.write("### Welcome to the NFL Player Performance Analysis App!")
    st.write("""
    This interactive application provides a comprehensive view of NFL player statistics, allowing you to dive deep into various performance metrics across seasons.
    Whether you're an NFL enthusiast, fantasy football player, or data analyst, this app is designed to give you insights into player performance trends, key metrics, and fantasy points analysis.

    Use the menu on the left to get started—explore player stats, analyze trends, and make data-driven predictions for future seasons.
    """)

elif menu == "EDA":
    # Sidebar menu for selecting the type of yard data
    metric = st.sidebar.selectbox(
        "Select a metric to visualize:",
        ("Passing Yards", "Receiving Yards", "Rushing Yards", "Total Yards")
    )

    # Mapping selection to column name
    metric_column = {
        "Passing Yards": "passing_yards",
        "Receiving Yards": "receiving_yards",
        "Rushing Yards": "rushing_yards",
        "Total Yards": "total_yards"
    }[metric]

    # Scatter plot for the selected metric
    st.write(f"Scatter Plot of {metric} by Season")
    search_query = st.text_input("Search for a player:")

    # Filter data based on the search query
    if search_query:
        filtered_data = data[data["player_name"].str.contains(search_query, case=False)]
    else:
        filtered_data = data

    filtered_data = filtered_data[filtered_data[metric_column] > 0]
    fig = px.scatter(
        filtered_data,
        x="season",
        y=metric_column,
        color="player_name",
        hover_name="player_name",
        title=f"{metric} Over Seasons"
    )
    st.plotly_chart(fig)

    # Top 10 players in the selected metric
    top_10_players = data.groupby("player_name")[metric_column].sum().nlargest(10)
    st.write(f"Top 10 Players in {metric} (All-Time)")
    pie_fig = px.pie(
        names=top_10_players.index,
        values=top_10_players.values,
        title=f"Top 10 Players by {metric} (All-Time)"
    )
    st.plotly_chart(pie_fig)

elif menu == "Insights":
    st.write("### Insights Page")
    st.write("This page provides insights and analysis of player performance data.")

    # Search bar for specific player insights
    player_search = st.text_input("Search for a player to view Fantasy Points and Yards per Game:")

    # Filter data based on player search query
    if player_search:
        player_data = data[data["player_name"].str.contains(player_search, case=False)]

        if not player_data.empty:
            # Line chart for Fantasy Points (PPR) for the searched player
            st.write(f"#### Fantasy Points (PPR) for {player_search} by Season")
            line_chart = px.line(
                player_data,
                x="season",
                y="fantasy_points_ppr",
                title=f"{player_search} - Fantasy Points (PPR) by Season",
                labels={"fantasy_points_ppr": "Fantasy Points (PPR)", "season": "Season"}
            )
            st.plotly_chart(line_chart)

        else:
            st.write("No data found for the specified player. Please check the spelling or try another player.")
    else:
        st.write("Use the search bar above to look up a player's fantasy points and yards per game by season.")

    # Line chart for all players' Fantasy Points (PPR)
    st.write("#### Overall Fantasy Points (PPR) Over Seasons")
    fantasy_points_data = data.groupby("season")["fantasy_points_ppr"].sum().reset_index()
    line_chart_all = px.line(
        fantasy_points_data,
        x="season",
        y="fantasy_points_ppr",
        title="Total Fantasy Points (PPR) by Season",
        labels={"fantasy_points_ppr": "Fantasy Points (PPR)", "season": "Season"}
    )
    st.plotly_chart(line_chart_all)

elif menu == "Prediction":
    st.write("### Prediction Page")
    st.write("This page will offer predictive analysis based on historical data.")
