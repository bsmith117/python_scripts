def surfline_buoy_extract(buoy_id_list):
    import datetime
    x1 = datetime.datetime.now()
    date = x1.strftime("%Y") + x1.strftime("%m") + x1.strftime("%d")
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    import time
    from pathlib import Path
    from urllib.request import urlretrieve as download
    from PIL import ImageFont
    from PIL import ImageDraw
    from selenium import webdriver
    from PIL import Image
    from cropImage import cropImage
    url = 'https://www.surfline.com/sign-in/?redirectUrl=https://www.surfline.com/'
    options = Options()
    #options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=options, executable_path="/Applications/chromedriver")
    driver.get(url)
    time.sleep(10)
    # locate email form by_xpath

    username = driver.find_element_by_xpath('//*[@id="email"]')
    # send_keys() to simulate key strokes
    username.send_keys('bsmith117@gmail.com')
    # locate password form by_xpath
    password = driver.find_element_by_xpath('//*[@id="password"]')
    # send_keys() to simulate key strokes
    password.send_keys('pebbles')
    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div/div/div[3]/form/button')
    log_in_button.click()
    #'/html/body/div[1]/div[2]/div[2]/div/div/div[3]/form/button'

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    a = 0
    for buoy_id in buoy_id_list:
        link = 'https://www.surfline.com/surfdata/forecast_buoy_detail_new.cfm?bid=' + str(buoy_id)
        directory = '/Users/Brandon/PycharmProjects/surflie_wave_app/buoy_extract/output/'
        Path(directory).mkdir(exist_ok=True)
        a = a + 1
        windows_before = driver.current_window_handle
        # print("First Window Handle is : %s" % windows_before)
        script = "window.open('{}')".format(link)
        driver.execute_script(script)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(a + 1))
        windows_after = driver.window_handles
        new_window = [x for x in windows_after if x != windows_before][a - 1]
        driver.switch_to_window(new_window)
        print("Page Title after Tab Switching is : %s" % driver.title)
        # print("Second Window Handle is : %s" % new_window)
        driver.refresh()
        time.sleep(3)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        data = []
        buoy_name = driver.title
        print(buoy_name)
        try:
            details = soup.find('div', {'class': 'buoy-info-swells borderRB'})
            leg = len(details.find_all('div')) - 1

            for row in details.find_all('div')[0:leg]:
                tag = row.text.strip()
                data.append(tag)

            image = (soup
                .find('div', {'id': 'tab-buoy-data-1'})
                .find("img")
                .attrs['src']
                )

            extract = True
        except:
            data = ['no data']
            extract = False

        if extract == True:
            directory = '/Users/Brandon/PycharmProjects/surflie_wave_app/buoy_extract/output/'
            Path(directory).mkdir(exist_ok=True)
            extension = image.split('.')[-1]
            download(image, f"{directory}/{str(buoy_id)}_plot.png")
            orig_img_path = directory + str(buoy_id) + '_plot.png'

            left = 15
            top = 0
            right = 600
            bottom = 310

            height = 310
            plot_width = right - left
            cropImage(f"{directory}/{str(buoy_id)}_plot.png", left, top, right, bottom, f"{directory}/{str(buoy_id)}_plot.png")
            # direction plot
            left = 15
            right = 600
            top = 600 - 195
            bottom = 600
            image_name = str(buoy_id) + '_plot.png'
            img_path = directory + image_name
            img_dir_path = directory + str(buoy_id) + '_dir_plot.png'
            crop1 = '/Users/Brandon/PycharmProjects/WaveApp/merge_image/cropped/crop1.png'
            crop2 = '/Users/Brandon/PycharmProjects/WaveApp/merge_image/cropped/crop2.png'

            x1 = 0
            x2 = 36
            x3 = 204
            x4 = 585
            x5 = 0
            x6 = 600
            y5 = 600 - 195
            width = (x4 - x3) + (x2 - x1)
            img1 = cropImage(img_path, x1, 0, x2, 310, crop1)
            img2 = cropImage(img_path, x3, 0, x4, 310, crop2)
            # Read the two images
            image1 = Image.open(crop1)
            image2 = Image.open(crop2)

            # img3 = cropImage(img_dir_path, x1, 0, x2, 195, crop3)
            # img4 = cropImage(img_dir_path, x3, 0, x4, 195, crop4)
            # image3 = Image.open(crop3)
            # image4 = Image.open(crop4)
            new_image = Image.new('RGB', (width, 310), (250, 250, 250))
            new_image.paste(image1, (0, 0))
            new_image.paste(image2, (x2, 0))
            # new_image.paste(image3, (0, 195))
            # new_image.paste(image4, (x2, 195))
            new_image.save(img_path, "png")
            print(data)
            leg = len(data)
            count = 0

            str1 = ''
            for idx in data:
                if count < leg:
                    str2 = str(idx) + '\n'
                    str1 = "".join((str1, str2))
                    count = count + 1
                else:
                    str2 = str(idx)
                    str1 = "".join((str1, str2))
                    count = count + 1

            if leg <= 2:
                ht = 80
            else:
                ht = 120

            img = Image.open(img_path)
            font = ImageFont.truetype('/Users/Brandon/PycharmProjects/WaveApp/arial sv/arial_ce/ArialCEBold.ttf',
                                      18)
            wd = 300
            text_width = 200
            button_img = Image.new('RGBA', (plot_width - 5, height - 90), "white")
            # put text on image
            button_draw = ImageDraw.Draw(button_img)
            button_draw.text((35, 0), str1, font=font, fill=(0, 0, 0, 1))
            # put button on source image in position (0, 0)
            img.paste(button_img, (0, height - 90))
            img.save(img_path)
        elif extract == False:
            image_name = str(buoy_id) + '_plot.png'
            img_path = directory + image_name
            img = Image.open('/Users/Brandon/PycharmProjects/WaveApp/no_data.png')
            img.save(img_path)
    driver.quit()  # remove this line to leave the browser open

surfline_buoy_extract([46232,46047,46219])