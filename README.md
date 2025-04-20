# Throughput Watcher

A monitoring tool that watches livestream quality and sends alerts when issues are detected. This project uses Selenium for web automation and Twilio for sending SMS notifications when stream quality dips below acceptable thresholds.

## 📋 Features

- Automated monitoring of livestream quality metrics
- SMS notifications via Twilio when issues are detected
- Headless browser operation for server environments
- GitHub Actions integration for scheduled monitoring
- Custom exit codes to properly handle stream end detection

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Chrome browser
- Twilio account for SMS notifications

### Setup

1. Clone the repository:
```bash
git clone https://github.com/lucianlavric/throughput-watcher.git
cd throughput-watcher
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with required environment variables (see Environment Variables section below).

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_PHONE=your_twilio_phone_number
TWILIO_TO_PHONE=recipient_phone_number
USER_EMAIL=your_login_email
USER_PASSWORD=your_login_password
GITHUB_TOKEN=your_github_token  # Only needed for GitHub Actions workflows
```

## 🚀 Usage

### Running Locally

Run the monitoring script manually:

```bash
python login.py
```

### GitHub Actions Integration

The project includes GitHub Actions workflows that can run the script on a schedule or trigger it manually. These are defined in `.github/workflows/` directory.

To use GitHub Actions:
1. Fork this repository
2. Add your environment variables as GitHub Secrets in your forked repository
3. Enable GitHub Actions in your repository settings
4. The workflows will run according to the schedule defined in the workflow files

## 📊 How It Works

1. The script logs into the target website using the provided credentials
2. It monitors key metrics on the livestream page
3. When quality dips below thresholds or other issues are detected, an SMS alert is sent
4. The script runs continuously until the stream ends or an error occurs

## 🔧 Customization

You can modify thresholds and monitoring parameters by editing the `login.py` file.

## 🔒 Security Notes

- Never commit sensitive data (passwords, API keys) directly to the repository
- Always use environment variables for all sensitive data
- Regularly rotate your API tokens and credentials

## 📝 License

This project is available as open source under the terms of the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
