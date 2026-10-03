import streamlit as st
import pandas as pd
import altair as alt

#step 7: Update the page configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 02",
    page_icon="🎓",
    layout="wide"
)

#step 8: Update student data
student_df = pd.DataFrame({
    "Student Name": ["Dara", "Sophea", "Vuthy", "Malis", "Rithy", "Sreyneang", "Chan", "Bopha"],
    "Course": ["Python", "Statistics", "Python", "Database", "Web App", "Database", "Python", "Statistics"],
    "Score": [85, 68, 45, 92, 58, 91, 72, 62],
    "Attendance": [90, 75, 50, 95, 60, 94, 80, 88],
    "Study Hours": [12, 8, 3, 15, 5, 14, 9, 7]
})

#step 9:Add a risk level function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

#step 10: Add the risk level column to the DataFrame
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

#step 11: update sidebar navigation
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )
    
#step 12: Update the home page content
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Student Risk Monitoring Dashboard")
    st.write("Welcome to lab 02.")
    st.write("In this lab, you will use Streamlit widgets to explore student performance data.")
    st.success("Lab 02 is working successfully!")
    
    # Create button click me
    if st.button("Click Me"):
        st.success("Welcome")
    
#step 13: Create the Dashboard page content
elif selected_page == "Dashboard":
    st.title("Interactive Dashboard")
    st.write("Use the filters below to explore student performance data.")

elif selected_page == "Student Data":
    st.title("Student Data")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", total_students)
        st.metric("Average Score", round(average_score, 2))

    with col2:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")
        st.metric("Low Score Students", low_score_students)

    st.dataframe(student_df)

else:
    st.title("About")
    st.write("This app is part of Lab 01.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    

#step 14: Add course filter
if selected_page == "Dashboard":
    selected_course = st.selectbox(
    "Select Course",
    ["All"] + list(student_df["Course"].unique())
)

#step 15: Add Risk Level filter
if selected_page == "Dashboard":
    selected_risk = st.selectbox(
    "Select Risk Level",
    ["All", "Low Risk", "Medium Risk", "High Risk"]
)

#step 16: Add Minimum attendance filter
if selected_page == "Dashboard":
    min_attendance = st.slider(
        "Minimum Attendance",
        0,
        100,
        0
    )
#Step 17: Add minimum score slider

    min_score = st.slider(
        "Minimum Score",
        0,
        100,
        0
    )

#step 18: Add Filtering logic 
if selected_page == "Dashboard":
    filtered_df = student_df.copy()
    
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]
        
    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]
        
    filtered_df = filtered_df[filtered_df["Attendance"] >= min_attendance]
    filtered_df = filtered_df[filtered_df["Score"] >= min_score]

    filtered_df = filtered_df[filtered_df["Attendance"] >= min_attendance]
    
    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score]

#Step 19: Add Dashboard Metrics
if selected_page == "Dashboard":
    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    
    else:
        average_score = 0
        average_attendance = 0
    
    high_risk_students = filtered_df[filtered_df["Risk Level"] == "High Risk"].shape[0]

    st.subheader("Dashboard Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

#step 20: Add Show or Hide dataset checkbox
if selected_page == "Dashboard":
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        st.dataframe(filtered_df)
    else:
        st.info("Filtered dataset is hidden.")
    #step 21: Add download button for filtered data
    if show_data:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
        
#Step 22: Add Student score chart
if selected_page == "Dashboard":
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")
            

#step 23: Add Risk level count chart
if selected_page == "Dashboard":
    with chart_col2:
        st.write("Risk Level Count")

        # Step 23: Add Risk level count chart
if selected_page == "Dashboard":
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_count = (
                filtered_df["Risk Level"]
                .value_counts()
                .reset_index()
            )

            risk_count.columns = ["Risk Level", "Count"]

            risk_chart = alt.Chart(risk_count).mark_bar().encode(
                x=alt.X(
                    "Risk Level:N",
                    title="Risk Level"
                ),
                y=alt.Y(
                    "Count:Q",
                    title="Number of Students"
                ),
                color=alt.Color(
                    "Risk Level:N",
                    scale=alt.Scale(
                        domain=["High Risk", "Medium Risk", "Low Risk"],
                        range=["red", "yellow", "green"]
                    ),
                    legend=None
                )
            )

            st.altair_chart(
                risk_chart,
                use_container_width=True
            )

        else:
            st.warning("No data available for risk chart.")

#step 24: Update the student data page
if selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)
    
#step 25: Create the risk checker page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")
            
#step 26: Update the about page
if selected_page == "About":
    st.title("About")
    st.write("This app is part of Lab 02.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Streamlit Interactive Dashboard")
    st.info("Ethics Reminder: Risk prediction should support students, not punish them.")