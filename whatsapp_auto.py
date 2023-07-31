# Import the necessary libraries
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os


# Define the Streamlit web app
def main():
    # Set the page title and description
    st.title("WhatsApp Message Sender By Artisan Innovattion Technologies")
    st.subheader("Send WhatsApp messages with images and text")

    # Add file upload options for Excel sheet and image
    st.sidebar.title("Upload Options")
    excel_file = st.sidebar.file_uploader(
        "Upload Excel File", type=["xls", "xlsx"])
    image_files = st.sidebar.file_uploader(
        "Upload Image (Optional)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # Hide footer made with streamlit
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Save images in folder
    if image_files:
        pic_names = []
        for image_f in image_files:
            file = image_f.read()
            image_result = open(image_f.name, 'wb')
            image_result.write(file)
            pic_names.append(image_f.name)
            image_result.close()

    # Add input field for text message
    text_message = st.text_area("Enter the text message to send")

    # Add a button to trigger the message sending process
    if st.button("Send Messages"):
        # Validate that the user has provided the Excel sheet
        if excel_file is not None:
            # Read the Excel sheet into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # Display the DataFrame on the web page (optional, for user verification)
            st.dataframe(df)

            # Get the phone numbers from the Excel sheet
            phone_numbers = df["Phone Number"].tolist()
            target = "_8nE1Y"
            message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'

            # Set up the Selenium WebDriver for Chrome
            driver = webdriver.Chrome()
            driver.get("https://web.whatsapp.com")
            st.info("Please scan the QR code on WhatsApp Web to continue...")

            # Wait for the user to scan the QR code and log in
            while "WhatsApp" not in driver.title:
                time.sleep(1)
            # Iterate through each phone number and send the WhatsApp message
            for phone_number in phone_numbers:
                i = 0
                try:
                    # Open a new chat with the phone number
                    driver.get(
                        f"https://web.whatsapp.com/send?phone={phone_number}")
                    # Wait until the chat is opened successfully
                    WebDriverWait(driver, 80).until(EC.presence_of_element_located(
                        (By.XPATH, message_box_path)))
                    # Check if the chat is opened successfully
                    chat_title = driver.find_element(
                        By.XPATH, f"//div[@class='{target}']")
                    if chat_title:
                        # Check if any images are uploaded
                        if image_files:
                            # Iterate through each uploaded image and send them one by one
                            for image_file in image_files:
                                # Upload the image if provided
                                attachment_icon = driver.find_element(
                                    By.XPATH, "//div[@title='Attach']")
                                attachment_icon.click()
                                time.sleep(10)
                                image_input = driver.find_element(
                                    By.XPATH, "//input[@type='file']")
                                name = pic_names[i]
                                path = os.path.abspath(
                                    "/Users/MWA/Desktop/PythonScripts/whatsapp_auto/" + name)
                                i = i + 1
                                image_input.send_keys(path)
                                time.sleep(10)
                                message_box = driver.find_element(
                                    By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w g0rxnol2']")
                                message_box.send_keys(text_message)
                                # Send the message
                                send_button = driver.find_element(
                                    By.XPATH, "//span[@data-icon='send']")
                                send_button.click()
                                time.sleep(10)
                        else:
                            message_box = driver.find_element(
                                By.XPATH, message_box_path)
                            message_box.send_keys(text_message, Keys.ENTER)
                            time.sleep(10)
                except Exception as e:
                    # Display any errors or exceptions on the web page
                    st.error(
                        f"Error sending message to {phone_number}: {str(e)}")

            # Close the browser after sending messages to all numbers
            driver.quit()

            # Display a success message after sending messages
            st.success("WhatsApp messages sent successfully to all numbers!")

        else:
            st.warning("Please upload the Excel file before sending messages.")


# Run the Streamlit web app
if __name__ == "__main__":
    main()
