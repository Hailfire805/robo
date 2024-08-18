from RPA.PDF import PDF
from RPA.Tables import Tables
from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP

pdf = PDF()


@task
def main():
    browser.configure(
    )
    open_site()
    click_ok_button()
    get_orders()
    orders = Tables().read_table_from_csv(path="orders.csv", header=True)
    fill_data(orders)


def open_site():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def click_ok_button():
    page = browser.page()
    page.click("button:text('OK')")


def fill_data(orders):
    page = browser.page()
    for row in orders:

        order_number = row['Order number']
        print(order_number)
        Head = row['Head']
        print(Head)
        Body = row['Body']
        print(Body)
        Legs = row['Legs']
        print(Legs)
        enter_data(row)
        page.click("#order")
        collect_results(row)
        screenshot_robot(order_number)
        start_over()
        click_ok_button()


def collect_results(data):
    page = browser.page()
    order_number = data["Order number"]
    page.screenshot(path=f"output/{order_number}_order_summary.png")


def start_over():
    page = browser.page()
    try:

        page.click("#order-another")
    except:
        page.click("#order")
        start_over()


def get_orders():
    http = HTTP()
    return http.download(
        url="https://robotsparebinindustries.com/orders.csv", overwrite=True)


def enter_data(data):
    page = browser.page()
    page.select_option("#head", data['Head'])
    page.click(f"#id-body-{data['Body']}")
    page.fill(
        '//html/body/div/div/div[1]/div/div[1]/form/div[3]/input', data['Legs'])
    page.fill("#address", data["Address"])


def create_receipt(order_number):

    path = f"output/{order_number}"
    return path


def screenshot_robot(order_number):
    list_of_files = [
        f"output/{order_number}_order_summary.png"
    ]
    pdf.add_files_to_pdf(
        files=list_of_files,
        target_document=f"output/{order_number}.pdf"
    )
