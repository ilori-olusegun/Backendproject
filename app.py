from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import re

app = Flask(__name__)

@app.route('/get_info', methods=['GET'])
def get_info():
    # Get query parameters
    slack_name = request.args.get('slack_name')
    track = request.args.get('track')

    # Calculate current day of the week and UTC time
    current_day = datetime.utcnow().strftime('%A')
    utc_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Validate UTC time within +/-2 hours
    utc_time_valid = validate_utc_time(utc_time)

    # Construct response JSON
    response = {
        "slack_name": slack_name,
        "current_day": current_day,
        "utc_time": utc_time,
        "track": track,
        "github_file_url": "https://github.com/ilori-olusegun/Backendproject/blob/main/app.py",
        "github_repo_url": "https://github.com/ilori-olusegun/Backendproject",
        "status_code": 200 if utc_time_valid else 400  # Return 400 if UTC time is not valid
    }

    return jsonify(response)

def validate_utc_time(utc_time):
    try:
        current_utc_time = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.utcnow()
        time_difference = abs(now - current_utc_time)
        return time_difference <= timedelta(hours=2)
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(debug=True)
