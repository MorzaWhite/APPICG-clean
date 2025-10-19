
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the order creation page
    page.goto("http://127.0.0.1:8000/orden/nueva/")

    # Add a "SET" item
    page.click("button[data-bs-target='#addItemModal']")
    page.wait_for_selector("#step-1", state="visible")
    page.select_option("#tipo_certificado_modal", "GC_COMPLETA")
    page.click("#step-1 button.next-step")

    page.wait_for_selector("#step-2", state="visible")
    page.select_option("#que_es_modal", "JOYA")
    page.click("#step-2 button.next-step")

    page.wait_for_selector("#step-3", state="visible")
    page.select_option("#tipo_joya_modal", "SET")
    page.click("#step-3 button.next-step")

    page.wait_for_selector("#step-4", state="visible")
    page.fill("#componentes_set_modal", "Anillo, Aretes")
    page.click("#step-4 button.next-step")

    page.wait_for_selector("#step-5", state="visible")
    page.select_option("#gema_principal_modal", "Zafiro")
    page.click("#step-5 button.next-step")

    page.wait_for_selector("#step-6", state="visible")
    page.fill("#cantidad_gemas_modal", "3")
    page.click("#step-6 button.next-step")

    page.wait_for_selector("#step-7", state="visible")
    page.click("#add-item-to-order")

    # Wait for the UI to update and take a screenshot
    page.wait_for_timeout(2000)
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
