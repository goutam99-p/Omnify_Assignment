from playwright.sync_api import sync_playwright


def test_orangehrm_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        page.wait_for_selector("input[name='username']")


        page.fill("input[name='username']", "Admin")
        page.fill("input[name='password']", "admin123")


        page.click("button[type='submit']")
        page.wait_for_selector("h6.oxd-topbar-header-breadcrumb-module")


        assert "Dashboard" in page.text_content("h6.oxd-topbar-header-breadcrumb-module")

        print("Login test passed")

        browser.close()


if __name__ == "__main__":
    test_orangehrm_login()
