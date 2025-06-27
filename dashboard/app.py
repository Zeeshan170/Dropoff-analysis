import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Student Lead Funnel Analysis")

# Upload CSV
uploaded_file = st.file_uploader("Upload your funnel data in csv format", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df_sorted = df.sort_values(by=['Lead ID', 'Timestamp'])
    lead_final_stage = df_sorted.groupby('Lead ID').last().reset_index()

    # Define stage order
    stage_order = ['New Lead', 'Contacted', 'Demo Given', 'Follow-up in Progress', 'Registered']
    stage_progression = df.drop_duplicates(['Lead ID', 'Stage'])['Stage'].value_counts().reindex(stage_order)
    stage_dropoffs = stage_progression.shift(1) - stage_progression
    stage_dropoffs_percentage = (stage_dropoffs / stage_progression.shift(1) * 100).round(2)

    st.subheader("Stage-wise Drop-off Metrics")
    drop_df = pd.DataFrame({
        'Stage': stage_order,
        'Leads at Stage': stage_progression.values,
        'Drop-off Count': stage_dropoffs.values,
        'Drop-off Rate (%)': stage_dropoffs_percentage.values
    }).dropna()
    st.dataframe(drop_df)

    # Bar chart: Drop-off Count
    st.subheader("Drop-off Count by Stage")
    fig1, ax1 = plt.subplots()
    sns.barplot(x='Drop-off Count', y='Stage', data=drop_df, ax=ax1, palette='Reds_r')
    st.pyplot(fig1)

    # Bar chart: Drop-off Rate
    st.subheader("Drop-off Rate (%) by Stage")
    fig2, ax2 = plt.subplots()
    sns.barplot(x='Drop-off Rate (%)', y='Stage', data=drop_df, ax=ax2, palette='Blues_r')
    st.pyplot(fig2)

    # Pie chart: Stage distribution
    st.subheader("Stage Distribution Pie Chart")
    fig3, ax3 = plt.subplots()
    ax3.pie(stage_progression, labels=stage_order, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax3.axis('equal')
    st.pyplot(fig3)

    # Segment metrics function
    def compute_drop_metrics(group_col):
        segment_df = lead_final_stage.groupby(group_col)['Stage'].value_counts(normalize=True).unstack().fillna(0) * 100
        segment_df['Drop Rate (%)'] = segment_df.get('Dropped / Inactive', 0)
        segment_df['Conversion Rate (%)'] = segment_df.get('Registered', 0)
        return segment_df[['Drop Rate (%)', 'Conversion Rate (%)']].round(2)

    # Advisor-wise
    st.subheader("Advisor-wise Drop & Conversion Rates")
    advisor_metrics = compute_drop_metrics('Advisor')
    st.dataframe(advisor_metrics)
    fig4, ax4 = plt.subplots()
    advisor_metrics[['Drop Rate (%)', 'Conversion Rate (%)']].plot(kind='bar', ax=ax4, colormap='coolwarm', figsize=(10,5))
    plt.title('Advisor-wise Drop vs Conversion Rate')
    st.pyplot(fig4)

    # Source-wise
    st.subheader("Source-wise Drop & Conversion Rates")
    source_metrics = compute_drop_metrics('Source')
    st.dataframe(source_metrics)
    fig5, ax5 = plt.subplots()
    source_metrics[['Drop Rate (%)', 'Conversion Rate (%)']].plot(kind='bar', ax=ax5, colormap='coolwarm', figsize=(10,5))
    plt.title('Source-wise Drop vs Conversion Rate')
    st.pyplot(fig5)

    # Program-wise
    st.subheader("Program-wise Drop & Conversion Rates")
    program_metrics = compute_drop_metrics('Program')
    st.dataframe(program_metrics)
    fig6, ax6 = plt.subplots()
    program_metrics[['Drop Rate (%)', 'Conversion Rate (%)']].plot(kind='bar', ax=ax6, colormap='coolwarm', figsize=(10,5))
    plt.title('Program-wise Drop vs Conversion Rate')
    st.pyplot(fig6)

    # Insights
    st.markdown("""
    ## 🔍 Key Insights & Recommendations
    
    **1. Funnel Performance:**
    - Major drop-offs occur between 'Contacted' → 'Demo Given' and 'Follow-up' → 'Registered'.

    **2. Advisor-wise:**
    - Clear variance in performance. Leverage top advisors' practices.

    **3. Source-wise:**
    - Referrals and campaigns convert better than website or cold traffic.

    **4. Program-wise:**
    - Data Science and MBA perform better than others; highlight their value.

    **Recommendations:**
    - Automate follow-ups post-demo
    - Improve advisor onboarding and training
    - Focus marketing on high-performing sources
    """)
