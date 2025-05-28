import random
from playwright.sync_api import sync_playwright, Locator

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
    page.wait_for_selector('//input[@name="username"]').type("Admin")
    page.wait_for_selector('//input[@name="password"]').type("admin123")
    page.click("button:has-text(' Login ')")
    page.wait_for_timeout(3000)

    page.hover('//a[@href="/web/index.php/pim/viewPimModule"]')
    page.click('//a[@href="/web/index.php/pim/viewPimModule"]')
    page.click("button:has-text(' Add ')")
    page.wait_for_timeout(3000)

    fields = page.locator('//input[contains(@class , "oxd-input--active")]')
    fields.nth(1).fill("Mary")
    fields.nth(1).fill("Jane")
    fields.nth(2).fill("Watson")
    random_emp_id1 = str(random.randint(10000, 99999))
    fields.nth(3).fill(random_emp_id1)
    page.click("button:has-text(' Save ')")
    page.wait_for_timeout(3000)

    page.wait_for_selector('//a[text()="Add Employee"]').click()
    fields.nth(1).fill("John")
    fields.nth(1).fill("Frank")
    fields.nth(2).fill("Kennedy")
    random_emp_id2 = str(random.randint(10000, 99999))
    fields.nth(3).fill(random_emp_id2)
    page.click("button:has-text(' Save ')")
    page.wait_for_timeout(3000)

    page.wait_for_selector('//a[text()="Add Employee"]').click()
    page.wait_for_timeout(3000)
    fields.nth(1).fill("Jack")
    fields.nth(1).fill("Black")
    fields.nth(2).fill("Torrance")
    random_emp_id3 = str(random.randint(10000, 99999))
    fields.nth(3).fill(random_emp_id3)
    page.click("button:has-text(' Save ')")
    page.wait_for_timeout(3000)

    page.wait_for_selector('//a[text()="Employee List"]').click()
    page.wait_for_timeout(3000)

    target_names = ["mary jane watson","john frank kennedy","jack black torrance"]
    found_names = set()
    current_page = 1

    while True:
        print(f"\n Checking page {current_page}")

        rows = page.locator("div.orangehrm-container .oxd-table-row")
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            cells = row.locator(".oxd-table-cell").all_inner_texts()
            if len(cells) >= 4:
                first_middle = cells[2].strip()
                last = cells[3].strip()
                full_name = f"{first_middle} {last}".strip().lower()

                if full_name in target_names and full_name not in found_names:
                    row.scroll_into_view_if_needed()
                    print(f" Name Verified: {first_middle} {last}")
                    found_names.add(full_name)

        next_page = str(current_page + 1)
        next_btn = page.locator(f'button.oxd-pagination-page-item--page:has-text("{next_page}")')

        if next_btn.count() == 0:
            print(" No more pages.")
            break

        next_btn.click()
        page.wait_for_timeout(1500)  # give the page time to load
        current_page += 1
