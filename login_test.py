import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    # ChromeDriver ayarları
    chrome_options = Options()
    # Headless mod kapalı
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Tarayıcı boyutunu ayarla
    driver.set_window_size(1920, 1080)

    yield driver
    driver.quit()


def take_screenshot(driver, test_name):
    # Ekran görüntüsü klasörünü oluştur
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    # Dosya adı oluştur
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")

    # Ekran görüntüsü al
    driver.save_screenshot(screenshot_path)
    print(f"✅ Ekran görüntüsü kaydedildi: {screenshot_path}")


def test_successful_login(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "successful_login")
    message = driver.find_element(By.ID, "message").text
    assert "Giriş Başarılı!" in message, "Başarılı giriş testi başarısız oldu"


def test_failed_login(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "failed_login")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "Hatalı giriş testi başarısız oldu"


def test_empty_username(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "empty_username")
    message = driver.find_element(By.ID, "message").text
    assert "Kullanıcı adı boş olamaz!" in message, "Boş kullanıcı adı testi başarısız oldu"


def test_empty_password(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "empty_password")
    message = driver.find_element(By.ID, "message").text
    assert "Parola boş olamaz!" in message, "Boş parola testi başarısız oldu"


def test_sql_injection(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("' OR '1'='1")
    driver.find_element(By.ID, "password").send_keys("' OR '1'='1")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "sql_injection")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "SQL injection testi başarısız oldu"


def test_long_username(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("a" * 100)
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "long_username")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "Uzun kullanıcı adı testi başarısız oldu"


def test_special_characters(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("@dm!n")
    driver.find_element(By.ID, "password").send_keys("!@#$%")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "special_characters")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "Özel karakter testi başarısız oldu"


def test_case_sensitivity(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("Admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "case_sensitivity")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "Büyük/küçük harf testi başarısız oldu"

def test_xss_in_username(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("<script>alert('XSS')</script>")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "xss_in_username")
    message = driver.find_element(By.ID, "message").text
    assert "<script>" not in message, "XSS açığı tespit edildi (kullanıcı adı)"


def test_xss_in_password(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("<script>alert('XSS')</script>")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "xss_in_password")
    message = driver.find_element(By.ID, "message").text
    assert "<script>" not in message, "XSS açığı tespit edildi (parola)"


def test_javascript_injection(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("'); alert('Hacked'); ('")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "javascript_injection")
    message = driver.find_element(By.ID, "message").text
    assert "Hacked" not in message, "JavaScript injection tespit edildi"


def test_html_injection(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("<b>Hacked</b>")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "html_injection")
    message = driver.find_element(By.ID, "message").text
    assert "<b>" not in message, "HTML injection tespit edildi"


def test_special_characters(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("!@#$%^&*()")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "special_characters")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "Özel karakter testi başarısız oldu"


def test_blank_spaces(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("     ")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "blank_spaces")
    message = driver.find_element(By.ID, "message").text
    assert "Kullanıcı adı boş olamaz!" in message, "Boşluk karakteri testi başarısız oldu"


def test_sql_injection_comment(driver):
    driver.get("http://localhost:3000/index.html")
    driver.find_element(By.ID, "username").send_keys("admin' --")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button").click()
    take_screenshot(driver, "sql_injection_comment")
    message = driver.find_element(By.ID, "message").text
    assert "Hatalı kullanıcı adı veya parola!" in message, "SQL injection (comment) testi başarısız oldu"