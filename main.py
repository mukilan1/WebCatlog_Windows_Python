import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QVBoxLayout, QToolBar, QAction, QDialog, QListWidget, QListWidgetItem, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.allowed_websites = []  # List of allowed websites with custom tab names
        self.load_allowed_websites() # Load allowed websites from file

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.nav_bar = QToolBar("Navigation")
        self.addToolBar(self.nav_bar)

        back_btn = QPushButton('Back')
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QPushButton('Reload')
        reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())

        self.nav_bar.addWidget(back_btn)
        self.nav_bar.addWidget(next_btn)
        self.nav_bar.addWidget(reload_btn)

        self.catalog_button = QPushButton('Website Catalog')
        self.catalog_button.clicked.connect(self.show_catalog)

        self.manage_button = QPushButton('Manage')
        self.manage_button.clicked.connect(self.show_manage_dialog)

        self.google_account_button = QPushButton('Google Accounts Center')
        self.google_account_button.clicked.connect(self.open_google_accounts_center)

        self.nav_bar.addWidget(self.catalog_button)
        self.nav_bar.addWidget(self.manage_button)
        self.nav_bar.addWidget(self.google_account_button)

        self.update_tabs()  # Add tabs for allowed websites

    def load_allowed_websites(self):
        try:
            with open('allowed_websites.txt', 'r') as file:
                lines = file.read().splitlines()
                updated_websites = []
                for line in lines:
                    parts = line.split('|')
                    if len(parts) == 2:
                        website_url, tab_name = parts[0], parts[1]
                        updated_websites.append((website_url, tab_name))
                self.allowed_websites = updated_websites
        except FileNotFoundError:
            pass



    def save_allowed_websites(self):
        with open('allowed_websites.txt', 'w') as file:
            for website_url, tab_name in self.allowed_websites:
                file.write(f"{website_url}|{tab_name}\n")

    def add_tab(self, url, tab_name):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.tabs.addTab(browser, tab_name)

    def update_tabs(self):
        # Clear all tabs
        while self.tabs.count() > 0:
            self.tabs.removeTab(0)

        # Re-add allowed websites as tabs
        for website_url, tab_name in self.allowed_websites:
            self.add_tab(website_url, tab_name)

    def show_catalog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Website Catalog")
        layout = QVBoxLayout(dialog)

        catalog_list = QListWidget()

        for website, name in self.allowed_websites:
            item = QListWidgetItem(name)
            catalog_list.addItem(item)

        layout.addWidget(catalog_list)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_manage_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Websites")
        dialog_layout = QVBoxLayout(dialog)

        website_list = QListWidget()
        for website, name in self.allowed_websites:
            item = QListWidgetItem(name)
            website_list.addItem(item)

        dialog_layout.addWidget(website_list)

        add_button = QPushButton("Add Website")
        add_button.clicked.connect(self.add_website)

        remove_button = QPushButton("Remove Website")
        remove_button.clicked.connect(self.remove_website)

        dialog_layout.addWidget(add_button)
        dialog_layout.addWidget(remove_button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def add_website(self):
        website_dialog = QDialog(self)
        website_dialog.setWindowTitle("Add Website")
        website_dialog_layout = QVBoxLayout(website_dialog)

        url_input = QLineEdit()
        url_input.setPlaceholderText("Enter website URL")

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter a name (optional)")

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_website_action(url_input.text(), name_input.text()))

        website_dialog_layout.addWidget(url_input)
        website_dialog_layout.addWidget(name_input)
        website_dialog_layout.addWidget(add_button)

        website_dialog.setLayout(website_dialog_layout)
        website_dialog.exec_()

    def add_website_action(self, url, name):
        if url:
            formatted_url = url if url.startswith("http://") or url.startswith("https://") else f"http://{url}"
            # Check if the website URL is not already in the list of allowed websites
            if formatted_url not in [website_url for website_url, _ in self.allowed_websites]:
                self.allowed_websites.append((formatted_url, name if name else formatted_url))
                self.add_tab(formatted_url, name if name else formatted_url)
                self.save_allowed_websites()  # Save updated list of allowed websites
                self.update_tabs() 

    def remove_website(self):
        website_list = self.findChild(QListWidget)
        selected_item = website_list.currentItem()
        if selected_item:
            selected_index = website_list.row(selected_item)
            if selected_index >= 0 and selected_index < len(self.allowed_websites):
                self.allowed_websites.pop(selected_index)
                self.save_allowed_websites()  # Save updated list of allowed websites
                self.update_tabs()  # Update tabs

    def open_google_accounts_center(self):
    # Replace 'YOUR_GOOGLE_ACCOUNTS_CENTER_URL' with the actual URL for Google Accounts Center
        google_accounts_url = "https://www.google.com"

        browser = QWebEngineView()
        browser.setUrl(QUrl(google_accounts_url))

        popup = QDialog(self)
        popup.setWindowTitle("Google Accounts Center")
        popup_layout = QVBoxLayout(popup)
        popup_layout.addWidget(browser)

        popup.exec_()

        # If not open, add it as a new tab
        self.add_tab(google_accounts_url, "Google Accounts Center")

def main():
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
