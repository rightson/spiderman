#!/usr/bin/env python
import sys
import os
import json
import argparse
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ocr import png2Integer


class Spiderman:
    def __init__(self, flow, wait_timeout=10, ocr_tmp_path='tmp_ocr.png'):
        self.WAIT_TIMEOUT = wait_timeout
        self.OCR_TMP_PATH = ocr_tmp_path
        self.flow = self.load_flow(flow)
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome = webdriver.Chrome(service=service, options=options)

    def load_flow(self, path):
        if not os.path.exists(path):
            print('Flow file not found: %s' % path)
            sys.exit(-1)
        with open(path, 'r', encoding='utf-8') as fp:
            result = json.loads(fp.read())
            if not 'steps' in result:
                print('Invalid flow format in %s' % path)
                sys.exit(-1)
            return result

    def run(self, halt):
        try:
            for step in self.flow['steps']:
                if step['action'] == 'get':
                    self.get(step['url'])
                elif step['action'] == 'select':
                    self.select(step['xpath'], step['text'])
                elif step['action'] == 'click':
                    self.click(step['xpath'])
                elif step['action'] == 'window':
                    self.window(step['index'])
                elif step['action'] == 'ocr':
                    self.ocr(step['img_xpath'],
                             step['regen_xpath'],
                             step['input_xpath'])
                elif step['action'] == 'send_keys':
                    self.send_keys(step['xpath'], step['key'])
                elif step['action'] == 'pause':
                    input('[pause] Press Enter to continue... ')
                else:
                    print('Unknown action %s' % step['action'])
            if halt:
                input('[halt] Press Enter to continue... ')
        except KeyboardInterrupt:
            self.__del__()

    def __del__(self):
        sys.stdout.write('[close] closing chrome... ')
        sys.stdout.flush()
        self.chrome.close()
        print('done')

    def get(self, url):
        print('[get] url=%s' % url)
        self.chrome.get(url)

    def select(self, xpath, text):
        print('[select] xpath=%s, text=%s' % (xpath, text))
        while True:
            try:
                return Select(self.element(xpath)).select_by_visible_text(text)
            except:
                time.sleep(0.5)

    def click(self, xpath):
        print('[click] xpath=%s' % xpath)
        self.element(xpath).click()

    def window(self, index):
        try:
            handle = self.chrome.window_handles[index]
            return self.chrome.switch_to.window(handle)
        except Exception as e:
            print('Error: unable to switch to window %s due to %s' %
                  (index, str(e)))

    def ocr(self, img_xpath, regen_xpath, input_xpath):
        while True:
            try:
                img_element = self.element(img_xpath)
                with open(self.OCR_TMP_PATH, 'wb') as file:
                    file.write(img_element.screenshot_as_png)
                code = png2Integer(self.OCR_TMP_PATH)
                if not code:
                    time.sleep(0.5)
                    self.click(regen_xpath)
                    continue
                print('[ocr xpath=%s, code=%s' % (img_xpath, code))
                self.send_keys(input_xpath, code)
                return os.unlink(self.OCR_TMP_PATH)
            except:
                time.sleep(0.5)
                continue

    def send_keys(self, xpath, key):
        print('[send_keys] xpath=%s, key=%s' % (xpath, key))
        self.element(xpath).send_keys(key)

    def element(self, xpath):
        return WebDriverWait(self.chrome, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )


if __name__ == '__main__':
    name = 'Spiderman'
    version = 'Version 1.0.0'
    parser = argparse.ArgumentParser(description='%s (%s)' % (name, version))
    parser.add_argument('steps', type=str, help='Steps file (JSON)')
    parser.add_argument('--halt', action='store_true',
                        help='Halt chrome after steps completed')
    args = parser.parse_args()

    if not args.steps:
        parser.print_help()
        sys.exit(-1)

    peter = Spiderman(args.steps)
    peter.run(halt=args.halt)
