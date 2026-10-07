"""End-to-end UI tests with Playwright (Python)."""
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def page(base_url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(base_url)
        yield pg
        b.close()

def add(page: Page, title: str):
    page.fill("#title", title)
    page.click("#add")

def test_page_title(page):
    expect(page).to_have_title("Task Tracker")

def test_add_task_appears_in_list(page):
    add(page, "UI task one")
    expect(page.locator("#list li .title", has_text="UI task one")).to_be_visible()

def test_empty_title_shows_error(page):
    add(page, "")
    expect(page.locator("#error")).to_have_text("title is required")

def test_mark_done_strikes_through(page):
    add(page, "Finish me")
    row = page.locator("#list li", has_text="Finish me")
    row.locator(".done").click()
    expect(row.locator(".title")).to_have_css("text-decoration-line", "line-through")

def test_delete_removes_task(page):
    add(page, "Delete me")
    row = page.locator("#list li", has_text="Delete me")
    row.locator(".del").click()
    expect(page.locator("#list li", has_text="Delete me")).to_have_count(0)

def test_html_in_title_is_escaped(page):
    add(page, "<b>bold</b>")
    expect(page.locator("#list li .title", has_text="<b>bold</b>")).to_be_visible()
    assert page.locator("#list li b").count() == 0
