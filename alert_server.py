"""
Alert Server Module
Runs a local web server that displays alerts via Browser Source
"""

import logging
import threading
import queue
import time
from typing import Optional, Dict, Any
from flask import Flask, render_template_string, Response, jsonify, send_from_directory
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertServer:
    """Web server for browser source alerts"""

    def __init__(self, port: int = 8000):
        """
        Initialize alert server

        Args:
            port: Port to run server on (default: 8000)
        """
        self.port = port
        self.app = Flask(__name__)
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for development
        self.alert_queue = queue.Queue()
        self.is_running = False
        self.server_thread: Optional[threading.Thread] = None

        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def index():
            """Main overlay page"""
            return render_template_string(self._get_overlay_html())

        @self.app.route('/stream')
        def stream():
            """Server-Sent Events stream for real-time alerts"""
            def event_stream():
                while True:
                    try:
                        # Wait for alert with timeout
                        alert = self.alert_queue.get(timeout=30)
                        yield f"data: {alert}\n\n"
                    except queue.Empty:
                        # Send keepalive
                        yield f": keepalive\n\n"
                    except Exception as e:
                        logger.error(f"Error in event stream: {e}")
                        break

            return Response(event_stream(), mimetype='text/event-stream')

        @self.app.route('/alerts/<path:filename>')
        def serve_alert(filename):
            """Serve alert files (images/videos)"""
            alerts_dir = Path(__file__).parent / 'alerts'
            return send_from_directory(alerts_dir, filename)

        @self.app.route('/api/alert', methods=['POST'])
        def trigger_alert():
            """API endpoint to trigger an alert"""
            from flask import request
            data = request.get_json()
            self.trigger_alert(
                alert_type=data.get('type', 'follow'),
                username=data.get('username', 'Anonymous'),
                message=data.get('message', ''),
                media_file=data.get('media_file'),
                duration=data.get('duration', 3.0)
            )
            return jsonify({'status': 'ok'})

        @self.app.route('/api/status')
        def status():
            """Server status endpoint"""
            return jsonify({
                'status': 'running',
                'port': self.port,
                'url': f'http://localhost:{self.port}'
            })

    def _get_overlay_html(self) -> str:
        """Get the HTML for the alert overlay"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TikForever Alerts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            width: 1920px;
            height: 1080px;
            overflow: hidden;
            background: transparent;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .alert-container {
            position: fixed;
            top: 100px;
            right: 50px;
            width: 500px;
            z-index: 1000;
        }

        .alert {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            opacity: 0;
            transform: translateX(600px);
            animation: slideIn 0.5s ease-out forwards;
            position: relative;
            overflow: hidden;
        }

        .alert.hide {
            animation: slideOut 0.5s ease-in forwards;
        }

        @keyframes slideIn {
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes slideOut {
            to {
                opacity: 0;
                transform: translateX(600px);
            }
        }

        .alert-type {
            font-size: 18px;
            font-weight: bold;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .alert-username {
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .alert-message {
            font-size: 20px;
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: 15px;
        }

        .alert-media {
            width: 100%;
            max-height: 300px;
            object-fit: contain;
            border-radius: 10px;
            margin-top: 15px;
        }

        .alert-icon {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 40px;
            opacity: 0.3;
        }

        /* Different alert type colors */
        .alert.follow {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .alert.gift {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        .alert.share {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }

        .alert.like {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }

        .alert.comment {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        }

        /* Sparkle effect */
        .sparkle {
            position: absolute;
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            animation: sparkle 1s ease-in-out infinite;
        }

        @keyframes sparkle {
            0%, 100% {
                opacity: 0;
                transform: scale(0);
            }
            50% {
                opacity: 1;
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <div class="alert-container" id="alertContainer"></div>

    <script>
        const alertContainer = document.getElementById('alertContainer');
        const eventSource = new EventSource('/stream');

        eventSource.onmessage = function(event) {
            if (event.data) {
                try {
                    const alertData = JSON.parse(event.data);
                    showAlert(alertData);
                } catch (e) {
                    console.error('Error parsing alert data:', e);
                }
            }
        };

        eventSource.onerror = function(error) {
            console.error('EventSource error:', error);
        };

        function showAlert(data) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert ${data.type}`;

            let mediaHtml = '';
            if (data.media_file) {
                const ext = data.media_file.split('.').pop().toLowerCase();
                if (['mp4', 'webm', 'ogg'].includes(ext)) {
                    mediaHtml = `<video class="alert-media" autoplay muted>
                        <source src="/alerts/${data.media_file}" type="video/${ext}">
                    </video>`;
                } else {
                    mediaHtml = `<img class="alert-media" src="/alerts/${data.media_file}" alt="Alert">`;
                }
            }

            const iconMap = {
                'follow': '👤',
                'gift': '🎁',
                'share': '📤',
                'like': '❤️',
                'comment': '💬'
            };

            alertDiv.innerHTML = `
                <div class="alert-icon">${iconMap[data.type] || '⭐'}</div>
                <div class="alert-type">${data.type}</div>
                <div class="alert-username">${data.username}</div>
                ${data.message ? `<div class="alert-message">${data.message}</div>` : ''}
                ${mediaHtml}
            `;

            // Add sparkles
            for (let i = 0; i < 5; i++) {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.style.left = `${Math.random() * 100}%`;
                sparkle.style.top = `${Math.random() * 100}%`;
                sparkle.style.animationDelay = `${Math.random() * 0.5}s`;
                alertDiv.appendChild(sparkle);
            }

            alertContainer.appendChild(alertDiv);

            // Auto-remove after duration
            const duration = (data.duration || 3) * 1000;
            setTimeout(() => {
                alertDiv.classList.add('hide');
                setTimeout(() => {
                    alertContainer.removeChild(alertDiv);
                }, 500); // Wait for animation
            }, duration);
        }

        // Test function (for debugging)
        function testAlert() {
            showAlert({
                type: 'follow',
                username: 'TestUser123',
                message: 'Thanks for following!',
                duration: 3
            });
        }
    </script>
</body>
</html>
        '''

    def start(self):
        """Start the alert server"""
        if self.is_running:
            logger.warning("Alert server is already running")
            return

        self.is_running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        logger.info(f"Alert server started on http://localhost:{self.port}")

    def _run_server(self):
        """Run the Flask server"""
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        except Exception as e:
            logger.error(f"Error running alert server: {e}")
            self.is_running = False

    def stop(self):
        """Stop the alert server"""
        self.is_running = False
        logger.info("Alert server stopped")

    def trigger_alert(self, alert_type: str, username: str = 'Anonymous',
                      message: str = '', media_file: Optional[str] = None,
                      duration: float = 3.0):
        """
        Trigger an alert

        Args:
            alert_type: Type of alert (follow, gift, share, like, comment)
            username: Username to display
            message: Optional message to display
            media_file: Optional media file (relative to alerts folder)
            duration: How long to show the alert (seconds)
        """
        import json

        alert_data = {
            'type': alert_type,
            'username': username,
            'message': message,
            'media_file': media_file,
            'duration': duration,
            'timestamp': time.time()
        }

        try:
            self.alert_queue.put(json.dumps(alert_data))
            logger.info(f"Alert triggered: {alert_type} for {username}")
        except Exception as e:
            logger.error(f"Error triggering alert: {e}")

    def get_url(self) -> str:
        """Get the URL for the browser source"""
        return f"http://localhost:{self.port}"


if __name__ == '__main__':
    # Test the server
    server = AlertServer()
    server.start()

    print(f"Alert server running at: {server.get_url()}")
    print("Add this URL as a Browser Source in TikTok Live Studio!")
    print("\nPress Ctrl+C to stop...")

    try:
        # Test alert after 3 seconds
        time.sleep(3)
        server.trigger_alert('follow', 'TestUser123', 'Thanks for following!', duration=5)

        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
