
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the create order page
            page.goto("http://127.0.0.1:8000/orden/nueva/")

            # Open the "Add Item" modal
            page.get_by_role("button", name="Añadir Ítem").click()

            # Wait for the modal to be visible
            expect(page.locator("#addItemModal")).to_be_visible()

            # Step 1: Select certificate type
            page.locator("#tipo_certificado_modal").select_option("GC_COMPLETA")
            page.get_by_role("button", name="Siguiente").click()

            # Step 2: Select "What is it?"
            page.locator("#que_es_modal").select_option("JOYA")
            page.get_by_role("button", name="Siguiente").click()

            # Step 3: Select jewel type
            page.locator("#tipo_joya_modal").select_option("ANILLO")
            page.get_by_role("button", name="Siguiente").click()

            # Step 5: Select main gemstone
            page.locator("#gema_principal_modal").select_option("Esmeralda")
            page.get_by_role("button", name="Siguiente").click()

            # Step 6: Enter quantity
            page.locator("#cantidad_gemas_modal").fill("1")
            page.get_by_role("button", name="Siguiente").click()

            # Step 7: Enter final details
            page.locator("#metal_modal").select_option("ORO")
            page.locator("#forma_gema_modal").select_option("Redonda")
            page.locator("#peso_gema_modal").fill("1.5")

            # Click the "Add Item to Order" button
            page.get_by_role("button", name="Añadir Ítem a la Orden").click()

            # Wait for the success toast to appear and the modal to close
            expect(page.locator("#success-toast")).to_be_visible()
            expect(page.locator("#addItemModal")).not_to_be_visible()

            # Verify the item summary is displayed
            expect(page.locator("#items-summary-container .card")).to_have_count(1)

            # Verify the suggested date has been updated
            expect(page.locator("#fecha-sugerida-texto")).not_to_contain_text("Calculando...")

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")

            print("Verification script completed successfully.")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
