from DrissionPage import ChromiumPage 
from RecaptchaSolver import RecaptchaSolver
import time

 
driver = ChromiumPage()
recaptchaSolver = RecaptchaSolver(driver)

driver.get("https://www.google.com/recaptcha/api2/demo")

t0 = time.time()
recaptchaSolver.solveCaptcha()
print(f"逃过验证码花费: {time.time()-t0:.2f} seconds")

driver.ele("#recaptcha-demo-submit").click()

driver.close()
