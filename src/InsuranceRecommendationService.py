from flask import Flask, request
from selenium import webdriver

app = Flask(__name__)

def show_insurance(vehicle_number):
    path_to_chromedriver = "C:\\chromedriver_win32\\chromedriver.exe" # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    url = 'https://www.policybazaar.com/motor-insurance/car-insurance/'
    browser.get(url)

    browser.find_element_by_xpath('//*[@id=\"carRegistrationNumber\"]').send_keys(vehicle_number) # xpath of the text box to send text
    browser.find_element_by_xpath('//*[@id=\"btnSubmit\"]').click() # xpath of the enter or submit button to click
    done = False
    while done == False:
        try:
            browser.find_element_by_xpath('//*[@id=\"rightSection\"]/div/div/div[1]/div[2]/div/button[2]').click() # Here I'm trying to bypass the
                                                                                                                  # prompts that pop-up in the middle
            done = True
        except:
            1 # bcoz this block should not be empty
    return browser.current_url

@app.route('/insurance')
def hello_world():
    vehicle_no = request.args.get('vehicleNo')
    url = show_insurance(vehicle_no)
    return url


if __name__ == "__main__":
    app.run(host="0.0.0.0")