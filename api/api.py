import streamlit as st
import requests
from PIL import Image
import io

# Define API endpoint
api_urls = [
    "https://carbotrackapi-qoz5nlx2ga-ew.a.run.app/predict"
]

# Define app title and description
st.markdown("# Welcome to the Carbotrack app! #")
st.markdown('''
Please be aware that our app and our models are still at an early stage and may lack accuracy in food detection.
**DO NOT** use this as medical guidance; always follow recommendations from your doctor.
Please upload or take a picture to test our app and see how much insulin you should take based on the picture of your food.
''')

# File upload section
uploaded_file = st.file_uploader('Photo of your meal', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False, help='Upload your photo')

# Process uploaded file
if uploaded_file is not None:
    col1, col2, col3 = st.columns([1,2,1])  # Create columns for layout
    with col2:  # Display the uploaded image in the middle column
        st.image(uploaded_file, width=340)

    # Button for food detection and insulin recommendation
    col1, col2, col3 = st.columns([1,2,1])  # Create columns for layout
    with col2:  # Put the button in the middle column
        col2_1, col2_2, col2_3 = st.columns([1,4,1])  # Create sub-columns within col2
        with col2_2:  # Put the button in the middle sub-column
            if st.button("Let's try to detect food type and give you an insulin recommendation!", key='predict'):
                if uploaded_file is not None:
                    files = {"image": (uploaded_file.name, buffer, "image/jpeg")}
                    with st.spinner('Trying to detect food type and give you an insulin recommendation!'):
                        response = requests.post(url, files=files)

                    # Handle API response
                    if response.status_code == 200:
                        result = response.json()
                        food_result = result.get('food_result', 'Unknown')
                        carbs_result = result.get('carbs_result', 'Unknown')
                        insulin_result = result.get('insulin_result', 'Unknown')

                        # Display results
                        st.markdown(f"**Food detected:** {food_result} :drooling_face:")  
                        st.markdown(f"**Estimated carbs:** {carbs_result:.2f} g")
                        st.markdown(f"**Recommended insulin dose (not medical advice):** {insulin_result} dose")
                    else:
                        st.write("Food not recognized. Our model is still learning. We apologize!")
                else:
                    st.write("Please upload an image")
