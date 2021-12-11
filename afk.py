import os, pyautogui, threading, time, random

class autoMate:
	running = True
	def main(self):
		t = threading.Thread(target = lambda: os.system("brave-browser https://www.google.com/robots.txt < /dev/null"))
		t.start()
		time.sleep(5)
		pyautogui.moveTo(500, 500, duration=0.5)


		n = 0
		while self.running:
			if pyautogui.screenshot().getpixel((1316, 89)) == (218, 68, 83):
				time.sleep(float(random.randrange(10, 50))/17.0)
				pyautogui.moveTo(1316, 89, duration=float(random.randrange(10, 150))/160.0)
				time.sleep(0.1)
				pyautogui.click()
				pyautogui.moveTo(500, 500, duration=0.5)
				time.sleep(0.9)
			pyautogui.moveRel(random.randrange(-175, 175), random.randrange(-175, 175), duration=float(random.randrange(30, 150))/160.0)
			time.sleep(float(random.randrange(10, 50))/10.0)



			if pyautogui.position()[-1] <= 170 or pyautogui.position()[-1] >= 725:
				pyautogui.moveTo(500, 500, duration=0.5)

			if random.randrange(0, 100)%10 == 0 :
				pyautogui.scroll(random.randrange(-30, 30))

			if random.randrange(0, 10)%3 == 0:
				pyautogui.click()