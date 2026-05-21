import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Set page config
st.set_page_config(
    page_title="Cricket Match Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏏 Cricket Match Analysis Dashboard")
st.markdown("Analyze cricket match patterns, team performance, and match outcomes through interactive visualizations.")
st.markdown("---")

# Load your data
@st.cache_data
def load_data():
    # Replace with your actual dataset path
    df = pd.read_excel('FinalMatches.xlsx', sheet_name='Matches')
    run_bins = [0, 100, 150, 200, 250, 300]
    bin_labels = ['Low', 'Medium', 'High', 'Very High', 'Extreme']
    df['run_category'] = pd.cut(df['target_runs'], bins=run_bins, labels=bin_labels)

    unique_teams = df['result'].unique()
    print("Unique Teams:", unique_teams.tolist())

    # Initialize label encoders
    le = LabelEncoder()
    le_run_category = LabelEncoder()
    le_target_overs = LabelEncoder()
    le_result = LabelEncoder()
    le_city = LabelEncoder()
    le_match_type = LabelEncoder()
    le_home = LabelEncoder()
    le_away = LabelEncoder()
    le_toss_winner = LabelEncoder()
    le_toss_decision = LabelEncoder()
    le_winner = LabelEncoder()
    le_home_won_toss = LabelEncoder()

    # Fit and transform with individual encoders
    df['run_category_encoded'] = le_run_category.fit_transform(df['run_category'])
    df['target_overs_encoded'] = le_target_overs.fit_transform(df['target_overs'])
    df['result_encoded'] = le_result.fit_transform(df['result'])
    df['city_encoded'] = le_city.fit_transform(df['city'])
    df['match_type_encoded'] = le_match_type.fit_transform(df['match_type'])
    df['Home_encoded'] = le_home.fit_transform(df['Home'])
    df['Away_encoded'] = le_away.fit_transform(df['Away'])
    df['toss_winner_encoded'] = le_toss_winner.fit_transform(df['toss_winner'])
    df['toss_decision_encoded'] = le_toss_decision.fit_transform(df['toss_decision'])
    df['winner_encoded'] = le_winner.fit_transform(df['winner'])

    df['home_won_toss'] = df['Home_encoded'] == df['toss_winner_encoded']
    df['home_won_toss_encoded'] = le_home_won_toss.fit_transform(df['home_won_toss'])

    df = df.drop(columns=['target_runs', 'target_overs', 'result', 'city', 'match_type', 'Home', 'Away', 'toss_winner', 'toss_decision', 'winner', 'run_category', 'home_won_toss'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Run category filter
run_categories = st.sidebar.multiselect(
    "Select Run Categories:",
    options=sorted(df['run_category_encoded'].unique()),
    default=sorted(df['run_category_encoded'].unique())
)

# Match result filter
match_results = st.sidebar.multiselect(
    "Select Match Results:",
    options=sorted(df['result_encoded'].unique()),
    default=sorted(df['result_encoded'].unique())
)

# Toss decision filter
toss_decisions = st.sidebar.multiselect(
    "Select Toss Decisions:",
    options=sorted(df['toss_decision_encoded'].unique()),
    default=sorted(df['toss_decision_encoded'].unique())
)

# Match type filter
match_types = st.sidebar.multiselect(
    "Select Match Types:",
    options=sorted(df['match_type_encoded'].unique()),
    default=sorted(df['match_type_encoded'].unique())
)

# Apply filters
filtered_df = df[
    (df['run_category_encoded'].isin(run_categories)) &
    (df['result_encoded'].isin(match_results)) &
    (df['toss_decision_encoded'].isin(toss_decisions)) &
    (df['match_type_encoded'].isin(match_types))
]

# Key Metrics Row
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_matches = len(filtered_df)
    st.metric("Total Matches", total_matches)

with col2:
    unique_cities = filtered_df['city_encoded'].nunique()
    st.metric("Unique Cities", unique_cities)

with col3:
    home_toss_wins = filtered_df['home_won_toss_encoded'].sum()
    home_toss_win_rate = (home_toss_wins / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    st.metric("Home Toss Wins", f"{home_toss_wins} ({home_toss_win_rate:.1f}%)")

with col4:
    avg_target_overs = filtered_df['target_overs_encoded'].mean()
    st.metric("Avg Target Overs", f"{avg_target_overs:.1f}")

st.markdown("---")

# First Row of Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Run Category Distribution")
    run_dist = filtered_df['run_category_encoded'].value_counts().sort_index()
    fig1 = px.bar(
        x=run_dist.index, 
        y=run_dist.values,
        labels={'x': 'Run Category', 'y': 'Number of Matches'},
        color=run_dist.values,
        color_continuous_scale='viridis'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🥧 Toss Decision Distribution")
    toss_counts = filtered_df['toss_decision_encoded'].value_counts()
    fig2 = px.pie(
        values=toss_counts.values,
        names=['Field First', 'Bat First'] if len(toss_counts) == 2 else toss_counts.index,
        color=toss_counts.values,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig2, use_container_width=True)

# Second Row of Charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Run Category vs Target Overs")
    fig3 = px.scatter(
        filtered_df,
        x='run_category_encoded',
        y='target_overs_encoded',
        color='result_encoded',
        size='winner_encoded',
        hover_data=['city_encoded', 'match_type_encoded'],
        title="Relationship between Run Categories and Target Overs",
        labels={
            'run_category_encoded': 'Run Category',
            'target_overs_encoded': 'Target Overs',
            'result_encoded': 'Match Result'
        }
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📊 Match Result Analysis")
    result_dist = filtered_df['result_encoded'].value_counts()
    fig4 = px.bar(
        x=result_dist.index,
        y=result_dist.values,
        labels={'x': 'Match Result', 'y': 'Count'},
        color=result_dist.values,
        color_continuous_scale='plasma'
    )
    st.plotly_chart(fig4, use_container_width=True)

# Third Row of Charts
col5, col6 = st.columns(2)

with col5:
    st.subheader("🏙️ City Distribution")
    city_dist = filtered_df['city_encoded'].value_counts().head(10)
    fig5 = px.pie(
        values=city_dist.values,
        names=city_dist.index,
        title="Top 10 Cities (Encoded Values)"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("📋 Match Type Distribution")
    match_type_dist = filtered_df['match_type_encoded'].value_counts()
    fig6 = px.bar(
        x=match_type_dist.index,
        y=match_type_dist.values,
        labels={'x': 'Match Type', 'y': 'Count'},
        color=match_type_dist.values,
        color_continuous_scale='rainbow'
    )
    st.plotly_chart(fig6, use_container_width=True)

# Fourth Row - Advanced Visualizations
st.subheader("🔍 Advanced Analysis")
col7, col8 = st.columns(2)

with col7:
    st.subheader("🎲 Toss Decision Impact on Winning")
    toss_win_analysis = pd.crosstab(
        filtered_df['toss_decision_encoded'], 
        filtered_df['winner_encoded']
    )
    fig7 = px.imshow(
        toss_win_analysis,
        title="Toss Decision vs Winner Heatmap",
        labels=dict(x="Winner", y="Toss Decision", color="Count"),
        aspect="auto"
    )
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.subheader("📈 Target Overs Distribution")
    fig8 = px.histogram(
        filtered_df,
        x='target_overs_encoded',
        nbins=20,
        title="Distribution of Target Overs",
        labels={'target_overs_encoded': 'Target Overs'},
        color_discrete_sequence=['#00CC96']
    )
    st.plotly_chart(fig8, use_container_width=True)

# Word Cloud Visualization
st.subheader("☁️ City Popularity Word Cloud")
try:
    from collections import Counter
    city_freq = dict(Counter(filtered_df['city_encoded']))
    
    # Create word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis'
    ).generate_from_frequencies(city_freq)
    
    # Display word cloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('City Distribution Word Cloud (Based on Encoded Values)')
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Word cloud could not be generated: {e}")

# Insights Section
st.markdown("---")
st.header("💡 Key Insights & Summary")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.subheader("🏆 Winning Patterns")
    if not filtered_df.empty:
        most_common_winner = filtered_df['winner_encoded'].mode()[0]
        win_rate_home_toss = (filtered_df['home_won_toss_encoded'].sum() / len(filtered_df)) * 100
        most_common_result = filtered_df['result_encoded'].mode()[0]
        
        st.info(f"**Most Common Winner Code:** {most_common_winner}")
        st.info(f"**Home Team Wins Toss:** {win_rate_home_toss:.1f}% of matches")
        st.info(f"**Most Common Result:** {most_common_result}")
    else:
        st.warning("No data available for insights with current filters")

with insight_col2:
    st.subheader("🎯 Match Characteristics")
    if not filtered_df.empty:
        avg_runs = filtered_df['run_category_encoded'].mean()
        avg_overs = filtered_df['target_overs_encoded'].mean()
        unique_teams = max(filtered_df['Home_encoded'].nunique(), filtered_df['Away_encoded'].nunique())
        
        st.success(f"**Average Run Category:** {avg_runs:.1f}")
        st.success(f"**Average Target Overs:** {avg_overs:.1f}")
        st.success(f"**Unique Teams:** {unique_teams}")
    else:
        st.warning("No data available for insights with current filters")

# Raw Data Section
st.markdown("---")
st.header("📋 Raw Data")

with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button for filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_cricket_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Cricket Match Analysis Dashboard • Built with Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)