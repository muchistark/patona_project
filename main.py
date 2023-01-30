from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import csv
from selenium.common.exceptions import NoSuchElementException
import requests


def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def web_scrape():

    driver = webdriver.Firefox()
    options = Options()
    options.add_argument("--headless")

    driver.get("https://dermnetnz.org/image-library")

    elements = find_multiple_element(
        driver, ".imageList__group a.imageList__group__item[href]"
    )
    if elements:

        fields = ["Decease_name", "Decease_name", "Decease_image_source"]
        rows = []

        file_name = "decease_log.csv"
        folder_name = "decease_images"

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        element_exist = False
        for element_index, element in enumerate(elements, start=1):

            decease_name = find_element(element, ".imageList__group__item__copy")
            decease_image = find_element(
                element, ".imageList__group__item__image img[src]"
            )

            if decease_name and decease_image:
                element_exist = True

                decease_name = decease_name.get_attribute("innerText").replace(
                    "images", ""
                )
                decease_link = element.get_attribute("href")
                decease_image = decease_image.get_attribute("src")
                image_name = (
                    f"{folder_name}/{decease_name.split(' ')[0]}_{element_index}.jpg"
                )

                response = requests.get(decease_image)
                with open(image_name, "wb") as image_cont:
                    image_cont.write(response.content)

                temp_row = [decease_name, decease_link, f"{image_name}"]
                rows.append(temp_row)

        if not element_exist:
            print("elements not found")
            return "FAIL"

        with open(file_name, "w") as csv_file:

            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(fields)
            csv_writer.writerows(rows)

    else:
        print("Main Element not Found")
        return "FAIL"

    driver.quit()

    return "PASS"


def find_element(element, selector):
    try:
        return_element = element.find_element(by="css selector", value=selector)
        return return_element
    except NoSuchElementException:
        return None


def find_multiple_element(element, selector):
    try:
        return_element = element.find_elements(by="css selector", value=selector)
        return return_element
    except NoSuchElementException:
        return None


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    result = web_scrape()
    if result == "PASS":
        print("Job Completed")
    else:
        print("job failed")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
