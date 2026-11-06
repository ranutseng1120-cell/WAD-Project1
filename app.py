
import streamlit as st
import pandas as pd
import plotly.express as px

# Step 9: Update Page Configuration
st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",  
    page_icon="🎓",                          
    layout="wide"                            
)


# Step 10: Keep CSV Loading from Lab 04
def load_student_data():
    try:
        # Read students.csv and convert it into a Pandas DataFrame.
        data = pd.read_csv("students.csv")

        # Return the loaded DataFrame.
        return data

    except FileNotFoundError:
        # Display an error if students.csv cannot be found.
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )

        # Stop the application because the dataset is required.
        st.stop()

# Step 11: Keep Loading the Student Data
student_df = load_student_data()


# Step 12: Keep the Risk Level Function
def get_risk_level(score, attendance):

    # If either score or attendance is below 60, classify as High Risk.
    if score < 60 or attendance < 60:
        return "High Risk"

    # If either score or attendance is below 75, classify as Medium Risk.
    elif score < 75 or attendance < 75:
        return "Medium Risk"

    # Otherwise, classify the student as Low Risk.
    else:
        return "Low Risk"


# Step 13: Apply Risk Classification to All Students
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],       # Get the student's score.
        row["Attendance"]   # Get the student's attendance.
    ),
    axis=1
)


# Step 14: Keep Session State from Lab 04
if "risk_history" not in st.session_state:

    # Create an empty list to store individual student risk checks.
    # Session state keeps this information while the user interacts with the app.
    st.session_state["risk_history"] = []


# Step 15: Keep Sidebar Navigation

# Create a sidebar for navigating between application pages.
with st.sidebar:

    # Display the sidebar title.
    st.title("EduRisk Menu")

    # Create a radio button menu.
    # The selected option determines which page will be displayed.
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

# Step 16: Update the Home Page

# Display the Home page when the user selects Home.
if selected_page == "Home":

    # Display the main application title.
    st.title("🎓 EduRisk Analytics")

    # Display a subtitle describing the application.
    st.subheader("Interactive Dashboard with Visualization and Filters")

    # Display a welcome message.
    st.write("Welcome to Lab 05.")

    # Explain the improvements included in this lab.
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )

    # Display a success message when the application is running.
    st.success("Lab 05 app is running successfully!")


# Step 17: Replace the Old Dashboard Page
# Step 18: Add Dashboard Title and Instruction
elif selected_page == "Dashboard":

    # Display the dashboard title.
    st.title("Interactive Student Performance Dashboard")

    # Explain how users can interact with the dashboard.
    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )

    # Step 19: Add Dashboard Filters Section
    st.subheader("Dashboard Filters")


    # ------------------------------------------
    # 9.1 CREATE THREE FILTER COLUMNS
    # ------------------------------------------

    # Divide the dashboard into three equal columns.
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    # Step 20: Add Course Filter

    with filter_col1:

        course_options = ["All"] + sorted(student_df["Course"].unique())
        # Create a dropdown menu for selecting a course.
        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )

    # Step 21: Add Risk Level Filter
    with filter_col2:

        # Get all unique risk levels and sort them.
        # Add All to allow users to display every risk level.
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())

        # Create a dropdown menu for selecting a risk level.
        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )

    # Step 22: Add Attendance Slider
    with filter_col3:

        # Create a slider from 0 to 100.
        # The default minimum attendance is 0%.
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )


    # Step 23: Create `filtered_df`
    filtered_df = student_df.copy()

    # If the user selects a specific course, keep only that course.
    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    # If the user selects a specific risk level, keep only that risk level.
    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    # Keep students whose attendance is greater than
    # or equal to the selected minimum attendance.
    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]

   # Step 24: Handle Empty Filter Results
    if filtered_df.empty:

        # Inform the user that no records match the selected filters.
        st.warning("No students match the selected filters. Please adjust the filters.")


    # ------------------------------------------
    # 9.3 CALCULATE DASHBOARD METRICS
    # ------------------------------------------

   # Step 25: Add Filtered Metrics
    st.subheader("Filtered Dashboard Metrics")

    # Count the number of students remaining after filtering.
    filtered_total_students = len(filtered_df)

    # Check whether the filtered dataset contains students.
    if filtered_total_students > 0:

        # Calculate the average score of filtered students.
        filtered_average_score = filtered_df["Score"].mean()

        # Calculate the average attendance of filtered students.
        filtered_average_attendance = filtered_df["Attendance"].mean()

        # Count how many filtered students are classified as High Risk.
        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]

    else:
        # Use zero values when no students match the filters.
        # This prevents errors when calculating metrics.
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0


    # Step 26: Display Filtered Metric Cards
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    # Display the total number of filtered students.
    with metric_col1:
        st.metric("Students", filtered_total_students)

    # Display the average student score.
    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))

    # Display the average attendance percentage.
    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    # Display the number of High Risk students.
    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)


    # ------------------------------------------
    # 9.4 COURSE SUMMARY USING GROUPBY()
    # ------------------------------------------

    # Step 27: Add Course Summary Table
    st.subheader("Course Summary")

    # Only calculate the summary if filtered data is available.
    if filtered_total_students > 0:

        # Group students according to their course.
        # agg() calculates multiple statistical summaries.
        course_summary = filtered_df.groupby("Course").agg(

            # Count the number of students in each course.
            Students=("Student Name", "count"),

            # Calculate the average score for each course.
            Average_Score=("Score", "mean"),

            # Calculate the average attendance for each course.
            Average_Attendance=("Attendance", "mean"),

            # Calculate the average study hours for each course.
            Average_Study_Hours=("Study Hours", "mean")

        ).reset_index()  # Convert Course from index back into a column.

        # Display the grouped course summary as a table.
        st.dataframe(course_summary)

    else:
        # Display a message when no course summary can be calculated.
        st.info("No course summary available for the selected filters.")

    # Step 28: Add Risk Level Summary Table
    st.subheader("Risk Level Summary")

    if filtered_total_students > 0:

        # Count the number of students in each risk category.
        # value_counts() counts occurrences of each unique value.
        # reset_index() converts the result into a DataFrame.
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()

        # Rename the columns for easier understanding.
        risk_summary.columns = ["Risk Level", "Students"]

        # Display the risk summary table.
        st.dataframe(risk_summary)

    else:
        # Display a message when no risk summary is available.
        st.info("No risk summary available for the selected filters.")


   # Step 29: Add Streamlit Charts Section
    st.subheader("Streamlit Charts")

    # Divide the section into two columns for side-by-side charts.
    chart_col1, chart_col2 = st.columns(2)

    # Step 30: Add Student Score Chart
    with chart_col1:

        # Display the chart title.
        st.write("Student Scores")

        if filtered_total_students > 0:

            # Set Student Name as the index.
            # Select only the Score column for visualization.
            score_chart = filtered_df.set_index("Student Name")["Score"]

            # Create a bar chart using Streamlit.
            st.bar_chart(score_chart)

        else:
            # Display a message if no data is available.
            st.info("No score chart available.")
            
    # Step 31: Add Course Count Chart
    with chart_col2:

        # Display the chart title.
        st.write("Students by Course")

        if filtered_total_students > 0:

            # Count the number of students in each course.
            course_count = filtered_df["Course"].value_counts()

            # Create a bar chart using Streamlit.
            st.bar_chart(course_count)

        else:
            # Display a message if no data is available.
            st.info("No course count chart available.")


    # Step 32: Add Plotly Charts Section
    st.subheader("Interactive Plotly Charts")

    # Divide the section into two columns.
    plotly_col1, plotly_col2 = st.columns(2)

    # Step 33: Add Plotly Risk Distribution Chart
    with plotly_col1:

        # Display the chart description.
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:

            # Count students in each risk category.
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]
            fig_risk = px.bar(

                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        else:
            st.info("No risk distribution chart available.")
    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )
            st.plotly_chart(fig_score, use_container_width=True)

        else:
            st.info("No score chart available.")
    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(filtered_df)

    else:
        st.info("No student records to display.")

    # Step 36: Add Ethical Visualization Reminder
    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )

# Step 37: Keep the Student Data Page from Lab 04
elif selected_page == "Student Data":

    st.title("Student Data")
    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )
    st.subheader("Data Inspection")
    st.write("Rows and Columns:", student_df.shape)
    st.write("Column Names:")
    st.write(student_df.columns.tolist())
    st.write("First 5 Rows:")
    st.dataframe(student_df.head())
    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

elif selected_page == "Risk Checker":

    st.title("Single Student Risk Checker")
    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )
    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )


    # Step 38: Keep the Risk Checker Page from Lab 04
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")
        
    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")

        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )
            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

            st.session_state["risk_history"].append(result)

            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")

            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")

            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

    st.subheader("Recent Risk Checks")
    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )
        st.dataframe(history_df)
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")

    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

# Step 39: Update the About Page
else:

    st.title("About")
    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")
    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )
    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )
