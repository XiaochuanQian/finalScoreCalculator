import streamlit as st
from datetime import datetime

# Function to calculate the required final exam score
def calculate_final_exam_score(current_score, desired_score, final_weight):
    """
    Calculate the score needed on the final exam to achieve the desired overall grade.
    """
    # Convert weights to proportions
    final_weight /= 100

    # Calculate the score needed
    needed_score = (desired_score - (current_score * (1 - final_weight))) / final_weight

    return needed_score

# Function for love calculator
def love_calculator(name1, name2):
    """Calculate a compatibility score based on two names."""
    combined_names = name1 + name2
    total = 0
    for char in combined_names.upper():
        if char.isalpha():
            total += ord(char) - ord('A') + 1
    love_score = total % 101
    return love_score

# Function to check if the current date is Valentine's Day or Qixi Festival
def is_special_day():
    today = datetime.now()
    # Valentine's Day: February 14
    if today.month == 2 and today.day == 14:
        return True
    # Qixi Festival (approximation): August 7
    if today.month == 8 and today.day == 7:
        return True
    return False

# Streamlit app layout
st.set_page_config(page_title="Multi-Feature App", page_icon="💡")

# Sidebar navigation
st.sidebar.title("Navigation")

# Determine available pages
available_pages = ["Final Exam Score Calculator"]
if is_special_day():
    available_pages.append("Love Calculator")

page = st.sidebar.radio("Select a feature:", available_pages)

if page == "Final Exam Score Calculator":
    # Final Exam Score Calculator Page
    st.title('Final Exam Score Calculator')

    # Tabbed interface for input methods
    tab1, tab2 = st.tabs(["Use Sliders", "Type Values"])

    # Default values
    current_score = 92.5
    desired_score = 90.0
    final_weight = 40.0

    with tab1:  # Slider input method
        st.write("Use sliders to set the values:")
        current_score = st.slider('Current Overall Score (%)', 0.0, 100.0, current_score, 0.01)
        desired_score = st.slider('Desired Overall Score (%)', 0.0, 100.0, desired_score, 0.01)
        final_weight = st.slider('Final Exam Weight (%)', 0.0, 100.0, final_weight, 0.5)

    with tab2:  # Text input method
        st.write("Type the values directly:")
        current_score_input = st.text_input("Enter Current Overall Score (%)", str(current_score))
        desired_score_input = st.text_input("Enter Desired Overall Score (%)", str(desired_score))
        final_weight_input = st.text_input("Enter Final Exam Weight (%)", str(final_weight))

        # Convert and validate inputs
        try:
            current_score = float(current_score_input)
            desired_score = float(desired_score_input)
            final_weight = float(final_weight_input)
        except ValueError:
            st.error("Please enter valid numeric values.")

    # Compute the required score when button is pressed
    if st.button('Calculate Required Final Score'):
        if current_score is not None and desired_score is not None and final_weight is not None:
            if 0 <= current_score <= 100 and 0 <= desired_score <= 100 and 0 <= final_weight <= 100:
                needed_score = calculate_final_exam_score(current_score, desired_score, final_weight)

                if 0 <= needed_score <= 100:
                    st.write(
                        f"You need to score **{needed_score:.2f}%** on the final exam to achieve your desired overall score.")
                elif needed_score < 0:
                    st.write("Congratulations! You have already achieved your desired score.")
                else:
                    st.write("It is not possible to achieve your desired score with the given final exam weight.")
            else:
                st.error("Please ensure all inputs are between 0 and 100.")
        else:
            st.error("Missing or invalid inputs. Please check your values.")

elif page == "Love Calculator":
    # Love Calculator Page
    st.title('Love Calculator')

    # Input fields for names
    name1 = st.text_input("Enter the first name:", "Alice")
    name2 = st.text_input("Enter the second name:", "Bob")

    # Calculate compatibility score
    if st.button('Calculate Love Score'):
        if name1 and name2:
            score = love_calculator(name1, name2)
            st.write(f"The love score between **{name1}** and **{name2}** is: **{score}%**")
        else:
            st.error("Please enter both names.")
