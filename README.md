# BlueSky Social Python Bot

## Overview
A customizable template for creating AI-powered social media bots using LlamaIndex, Bluesky, and Ollama with RAG functionality.

## Project Structure
- **ollamaBlueSky.py**: Contains core bot logic with RAG setup, file directory reading, and persistent storage.
- **BlueSkyBot.py**: Handles original API interactions, task scheduling, and posting features.

This project demonstrates my ability to build robust Python applications that interact with APIs, process data, and automate tasks. The **BlueSky Social Python Bot** automates the posting of text and image content to the BlueSky Social platform using the `Atproto` client, complete with logging and scheduling capabilities.

## 🛠 Features
- **Text Posting:** Fetch and post textual data from a specified API endpoint.
- **Image Posting:** Fetch and post images with metadata such as descriptions and alternative text for accessibility.
- **Task Scheduling:** Automate tasks to run at periodic intervals using the `schedule` library.
- **Error Handling:** Comprehensive logging and error handling for robust performance.
- **Secure Configuration:** Credentials and API URLs are handled securely using environment variables.
- **Ollama RAG Integration:** Implements retrieval augmented generation using LlamaIndex with dynamic prompt creation, file directory reading, and persistent storage.

---

## 🚀 Technologies Used
- **Python**: Core programming language.
- **`atproto`**: For interacting with the BlueSky Social API.
- **`requests`**: To handle HTTP requests and fetch data.
- **`schedule`**: For periodic task scheduling.
- **`logging`**: For activity and error tracking.
- **`tempfile`**: For efficient temporary file management.

---

## 📚 Learning Objectives
This project highlights my proficiency in:
- API integration and interaction using Python.
- Scheduling and automating tasks.
- Writing maintainable and reusable code.
- Error handling and robust application design.
- Secure handling of sensitive information (e.g., API credentials).

---

## 📦 Setup Instructions

### Prerequisites
- Python 3.8 or later installed on your machine.
- Basic knowledge of Python and command-line tools.
- APIs to fetch text and images (set up your own or use public ones).

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MeanFishy00/BlueSky-Social-Python-Bot.git
   cd BlueSky-Social-Python-Bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Configure your credentials and API endpoints:
   ```bash
   export API_USERNAME="your_username"
   export API_PASSWORD="your_password"
   export TEXT_API_URL="https://example.com/api/text"
   export IMAGE_API_URL="https://example.com/api/image"
   ```

   Alternatively, you can use a `.env` file or a configuration manager like `python-decouple`.

4. **Run the Script**:
   ```bash
   python script_name.py
   ```

---

## 🛠 How It Works
1. **Text Posting**: 
   - Fetches data from the `TEXT_API_URL` endpoint.
   - Posts the `text` field from the API response.
2. **Image Posting**:
   - Fetches image content from the `IMAGE_API_URL` endpoint.
   - Saves the image locally using `tempfile`.
   - Posts the image with metadata (description and alt text).
3. **Task Scheduler**:
   - Runs `textPost` every 1 minute and `imagePost` every 2 hours by default.
   - Continuously checks for pending tasks and executes them.

---

## 📋 Code Overview
### File Structure
```
.
├── script_name.py          # Main script
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
```

### Key Functions
- **`textPost`**: Handles text posting tasks.
- **`imagePost`**: Handles image posting tasks.
- **`fetch_data`**: Fetches JSON data from a given API endpoint.
- **`run_scheduler`**: Configures and runs the task scheduler.

---

## 🔧 Customization
### Modifying Schedule
To change the schedule, update the `schedule.every` calls in `run_scheduler`:
```python
schedule.every(5).minutes.do(textPost)  # Run textPost every 5 minutes
schedule.every(1).hours.do(imagePost)  # Run imagePost every 1 hour
```

### Adding New Features
Extend the script to include:
- Posting other types of media or data.
- Advanced retry mechanisms using libraries like `tenacity`.

---

## 🧪 Testing
For testing, consider using `pytest` or `unittest`:
- Mock the API responses using `responses` or `unittest.mock`.
- Verify error handling and logging.
- Validate the scheduling functionality.

---

## 🌟 Why This Project?
This project showcases my ability to:
- Build end-to-end Python applications that integrate with APIs.
- Automate and schedule tasks effectively.
- Write secure, maintainable, and production-ready code.
- Solve real-world problems with Python.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📫 Contact
Feel free to connect with me for questions or collaboration:
- **GitHub**: [MeanFishy00](https://github.com/MeanFishy00)
- **Email**: Isaiah.greenwood01@gmail.com
- **LinkedIn**: [Isaiahgwood](https://www.linkedin.com/in/isaiahgwood)
- **Portfolio**: [Repositories](https://github.com/MeanFishy00?tab=repositories)
