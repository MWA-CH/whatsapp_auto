# CAN: Import the necessary libraries
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from deta import Deta


# CAN: Define the Streamlit web app


def main():
    # CAN: Set the page title and description
    st.title("WhatsApp Message Sender")
    st.subheader("Send WhatsApp messages with images and text")

    # CAN: Add file upload options for Excel sheet and image
    st.sidebar.title("Upload Options")
    excel_file = st.sidebar.file_uploader(
        "Upload Excel File", type=["xls", "xlsx"])
    image_files = st.sidebar.file_uploader(
        "Upload Image (Optional)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # CAN: Add input field for text message
    text_message = st.text_area("Enter the text message to send")

    # CAN: Add a button to trigger the message sending process
    if st.button("Send Messages"):
        # CAN: Validate that the user has provided the Excel sheet
        if excel_file is not None:
            # CAN: Read the Excel sheet into a pandas DataFrame
            df = pd.read_excel(excel_file)

            # CAN: Display the DataFrame on the web page (optional, for user verification)
            st.dataframe(df)

            # CAN: Get the phone numbers from the Excel sheet
            phone_numbers = df["Phone Number"].tolist()
            target = "_8nE1Y"
            message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            # CAN: Set up the Selenium WebDriver for Chrome
            driver = webdriver.Chrome()
            driver.get("https://web.whatsapp.com")
            st.info("Please scan the QR code on WhatsApp Web to continue...")

            # CAN: Wait for the user to scan the QR code and log in
            while "WhatsApp" not in driver.title:
                time.sleep(1)

            # CAN: Iterate through each phone number and send the WhatsApp message
            for phone_number in phone_numbers:
                try:
                    # CAN: Open a new chat with the phone number
                    driver.get(
                        f"https://web.whatsapp.com/send?phone={phone_number}")
                    # CAN: Wait until the chat is opened successfully
                    WebDriverWait(driver, 80).until(EC.presence_of_element_located(
                        (By.XPATH, message_box_path)))

                    # CAN: Check if the chat is opened successfully
                    chat_title = driver.find_element(
                        By.XPATH, f"//div[@class='{target}']")
                    if chat_title:
                        # CAN: Check if any images are uploaded
                        if image_files:
                            # CAN: Iterate through each uploaded image and send them one by one
                            # pic_names = []
                            for image_file in image_files:
                                # CAN: Upload the image if provided
                                # print(image_file.name)
                                attachment_icon = driver.find_element(
                                    By.XPATH, "//div[@title='Attach']")
                                attachment_icon.click()
                                time.sleep(5)

                                # image_input = driver.find_element(
                                #     By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
                                # file = image_file.read()
                                # image_result = open(image_file.name, 'wb')
                                # image_result.write(file)
                                # pic_names.append(image_file.name)
                                # image_result.close()

                                image_input = driver.find_element(
                                    By.XPATH, "//input[@type='file']")

                                # bytes_data = image_file.getvalue()
                                # image_input.send_keys(st.image(bytes_data))

                                image_input.send_keys(
                                    '/Users/MWA/Desktop/PythonScripts/whatsapp_auto/screenshot.png')

                                time.sleep(10)

                                message_box = driver.find_element(
                                    By.XPATH, "//p[@class='selectable-text copyable-text iq0m558w g0rxnol2']")

                                message_box.send_keys(text_message)

                                # CAN: Send the message
                                send_button = driver.find_element(
                                    By.XPATH, "//span[@data-icon='send']")
                                send_button.click()

                                time.sleep(15)

                                # CAN: Enter the text message
                                # message_box = driver.find_element(
                                #     By.XPATH, message_box_path)
                                # message_box.send_keys(text_message, Keys.ENTER)

                                # # CAN: Send the message
                                # send_button = driver.find_element(By.XPATH,
                                #                                   "//span[@data-icon='send']")
                                # send_button.click()

                                # CAN: Wait for a few seconds before proceeding to the next number
                                # time.sleep(15)
                        else:
                            message_box = driver.find_element(
                                By.XPATH, message_box_path)
                            message_box.send_keys(text_message, Keys.ENTER)

                            # # CAN: Send the message
                            # send_button = driver.find_element(By.XPATH,
                            #                                   "//span[@data-icon='send']")
                            # send_button.click()

                            # CAN: Wait for a few seconds before proceeding to the next number
                            time.sleep(15)
                except Exception as e:
                    # CAN: Display any errors or exceptions on the web page
                    st.error(
                        f"Error sending message to {phone_number}: {str(e)}")

            # CAN: Close the browser after sending messages to all numbers
            driver.quit()

            # CAN: Display a success message after sending messages
            st.success("WhatsApp messages sent successfully to all numbers!")

        else:
            st.warning("Please upload the Excel file before sending messages.")


# CAN: Run the Streamlit web app
if __name__ == "__main__":
    main()
