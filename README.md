# Application-Kannon-47

## Overview

**Application-Kannon-47** is a graphical user interface (GUI) tool designed to help users track job applications, maintain chat logs, and interact with an AI assistant. It leverages a SQLite database for data storage and uses Python's `tkinter` library for creating the interface.

This tool is built to manage job applications, interact with OpenAI's GPT-based assistant, and track application statuses. The application includes functionalities like logging chat conversations, searching and filtering job offers, and displaying detailed offer views. It supports multi-user operations and allows users to keep track of their application journey efficiently.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Job Application Management:** Add, edit, search, filter, and delete job applications with different statuses (Open, Applied, Rejected, Accepted).
- **Chat Integration:** Uses OpenAI's GPT to assist users with job-related queries and logs chat interactions.
- **User-Friendly GUI:** Built using `tkinter` for easy navigation and a responsive user interface.
- **SQLite Database:** Uses SQLite for efficient data storage and retrieval.
- **Multi-user Support:** Tracks applications for multiple users and associates each job offer with a user profile.
- **Data Persistence:** Keeps a record of job applications and chat logs in the local SQLite database.

## Technologies Used

- **Python**: Core programming language.
- **SQLite**: Database to store user data and job applications.
- **tkinter**: GUI framework to create the graphical interface.
- **OpenAI API**: For chat-based AI assistant functionality.
- **dotenv**: To manage environment variables.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/Application-Kannon-47.git
   cd Application-Kannon-47
   ```

2. **Set Up a Virtual Environment:**
   It's a good practice to use a virtual environment to manage your dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Install the required Python packages using the following command:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   Create and initialize your SQLite database. Ensure your database schema is correctly set up before running the application. You may need to create the necessary tables as described in the code comments.

5. **Configure Environment Variables:**
   If your application requires any environment variables (like API keys), create a `.env` file in the project root and add the necessary variables in the format:
   ```plaintext
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   OPENAI_API_KEY=your_openai_api_key
   ```

6. **Run the Application:**
   You can start the application by running:
   ```bash
   python main.py
   ```

## Usage

Once the application is running, you can:

- Track job applications, including position, company, status, and any related offers.
- Search for specific applications based on filters such as position, company, and status.
- View, edit, or delete entries related to your job applications.

## Features

- **User Authentication:** Secure login to manage your applications.
- **Application Tracking:** Keep track of multiple job applications with detailed status updates.
- **Search Functionality:** Filter applications based on criteria.
- **Chat Assistant:** Integrated ChatGPT assistant for guidance and tips.
- **Scrollable Results:** Easily navigate through search results with scrollable windows.

## Contributing

If you would like to contribute to the Application-Kannon-47 project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
