from playwright.sync_api import sync_playwright, expect
import re
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the create order page
    page.goto("http://localhost:8000/orden/nueva/")

    # Click the "Add Item" button and take a screenshot
    page.locator('button[data-bs-target="#addItemModal"]').click()
    expect(page.locator('#addItemModal')).to_be_visible()
    page.screenshot(path="jules-scratch/verification/modal_initial_state.png")

    # Step 1: Certificate Type
    page.select_option('#tipo_certificado_modal', 'GC_SENCILLA')
    page.locator('.step-card.active .next-step').click()
    expect(page.locator('#step-2.active')).to_be_visible()

    # Step 2: What is it?
    page.select_option('#que_es_modal', 'JOYA')
    page.locator('.step-card.active .next-step').click()
    expect(page.locator('#step-3.active')).to_be_visible()

    # Step 3: Type of Jewel
    page.select_option('#tipo_joya_modal', 'ANILLO')
    page.locator('.step-card.active .next-step').click()
    expect(page.locator('#step-4.active')).to_be_visible()

    # Step 4: Main Gemstone (Select2)
    page.locator('#step-4.active .select2-container').click()
    page.locator('.select2-results__option', has_text='Diamante').click()
    page.locator('.step-card.active .next-step').click()
    expect(page.locator('#step-5.active')).to_be_visible()

    # Step 5: Quantity
    page.fill('#cantidad_gemas_modal', '1')
    page.locator('.step-card.active .next-step').click()
    expect(page.locator('#step-6.active')).to_be_visible()

    # Step 6: Details
    page.select_option('#metal_modal', 'ORO')
    page.locator('#step-6.active .select2-container').click()
    page.locator('.select2-results__option', has_text='Redonda').click()
    page.fill('#peso_gema_modal', '1.0')
    page.locator('#add-item-to-order').click()

    # Reopen the modal and take another screenshot
    expect(page.locator('#addItemModal')).not_to_be_visible()
    page.locator('button[data-bs-target="#addItemModal"]').click()
    expect(page.locator('#addItemModal')).to_be_visible()
    page.screenshot(path="jules-scratch/verification/modal_reset_state.png")
    page.locator('#addItemModal .btn-close').click()

    # Create the order with a unique number
    order_number = f"VERIF-{int(time.time())}"
    page.fill('input[name="numero_orden_facturacion"]', order_number)
    page.locator('button[type="submit"]').click()
    expect(page).to_have_url(re.compile(r"/orden/creada/"))

    # Go to the order detail page
    orden_id = page.url.split('/')[-2]
    page.goto(f"http://localhost:8000/orden/{orden_id}/")

    # Take a screenshot to verify the manual date modal is gone
    page.screenshot(path="jules-scratch/verification/no_manual_date.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
