import pytest
import uuid


def test_token_acls_options_rendering1(driver, user):
    driver.get(f"/become_user/{user.id}")
    driver.get("/profile")
    driver.wait_for_xpath('//input[@name="acls[0]"]')
    driver.wait_for_xpath('//input[@name="acls[1]"]')
    driver.wait_for_xpath('//input[@name="acls[2]"]')
    driver.wait_for_xpath_to_disappear('//input[@name="acls[3]"]')


def test_token_acls_options_rendering2(driver, super_admin_user):
    driver.get(f"/become_user/{super_admin_user.id}")
    driver.get("/profile")
    for i in range(5):
        driver.wait_for_xpath(f'//input[@name="acls[{i}]"]')


@pytest.mark.xfail(strict=False)
def test_add_and_see_realname_in_user_profile(driver, user):
    driver.get(f"/become_user/{user.id}")
    driver.get("/profile")
    first_name_entry = driver.wait_for_xpath('//input[@name="firstName"]')
    first_name = str(uuid.uuid4())
    first_name_entry.send_keys(first_name)
    last_name_entry = driver.wait_for_xpath('//input[@name="lastName"]')
    last_name = str(uuid.uuid4())
    last_name_entry.send_keys(last_name)

    driver.scroll_to_element_and_click(
        driver.find_element_by_xpath('//*[@id="updateProfileButton"]')
    )

    # now that we added the name, let's see if it's displayed correctly
    name_display = driver.wait_for_xpath(
        '//*[@id="userRealname"][contains(@style, "visibility: visible")]'
    ).text
    assert name_display == f"{first_name} {last_name}"


def test_add_data_to_user_profile(driver, user):
    driver.get(f"/become_user/{user.id}")
    driver.get("/profile")
    first_name_entry = driver.wait_for_xpath('//input[@name="firstName"]')
    driver.scroll_to_element_and_click(first_name_entry)
    first_name = str(uuid.uuid4())
    first_name_entry.send_keys(first_name)
    last_name_entry = driver.wait_for_xpath('//input[@name="lastName"]')
    driver.scroll_to_element_and_click(last_name_entry)
    last_name = str(uuid.uuid4())
    last_name_entry.send_keys(last_name)

    email_entry = driver.wait_for_xpath('//input[@name="email"]')
    driver.scroll_to_element_and_click(email_entry)
    email = f"{str(uuid.uuid4())[:5]}@hotmail.com"
    email_entry.clear()
    email_entry.send_keys(email)

    phone_entry = driver.wait_for_xpath('//input[@name="phone"]')
    phone = "+12128675309"
    driver.scroll_to_element_and_click(phone_entry)
    phone_entry.send_keys(phone)

    driver.scroll_to_element_and_click(
        driver.find_element_by_xpath('//*[@id="updateProfileButton"]')
    )


def test_insufficient_name_entry_in_profile(driver, user):
    driver.get(f"/become_user/{user.id}")
    driver.get("/profile")
    first_name_entry = driver.wait_for_xpath('//input[@name="firstName"]')
    first_name = ""
    driver.scroll_to_element_and_click(first_name_entry)
    first_name_entry.send_keys(first_name)
    last_name_entry = driver.wait_for_xpath('//input[@name="lastName"]')
    last_name = str(uuid.uuid4())
    driver.scroll_to_element_and_click(last_name_entry)
    last_name_entry.send_keys(last_name)

    update_profile_button = driver.find_element_by_xpath(
        '//*[@id="updateProfileButton"]'
    )
    driver.scroll_to_element_and_click(update_profile_button)

    helper = driver.wait_for_xpath('//p[@id="firstName_id-helper-text"]')
    assert helper.text == "Required"


@pytest.mark.flaky(reruns=2)
def test_profile_dropdown(driver, user):
    test_add_data_to_user_profile(driver, user)

    # click on profile dropdown
    avatar_element = driver.wait_for_xpath("//span[contains(@data-testid, 'avatar')]")
    driver.scroll_to_element_and_click(avatar_element)

    # check dropdown contents
    driver.wait_for_xpath("//p[contains(@data-testid, 'firstLastName')]")
    driver.wait_for_xpath("//p[contains(@data-testid, 'username')]")
    driver.wait_for_xpath("//a[contains(@data-testid, 'signOutButton')]")
