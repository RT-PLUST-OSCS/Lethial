from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime
import os
import webbrowser
from threading import Timer
import socket

class ApplicationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve HTML page
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('job_application.html', 'r', encoding='utf-8') as file:
                    html_content = file.read()
                self.wfile.write(html_content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        # Serve other files (CSS, JS if separate)
        elif self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/submit':
            # Read sent data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Convert data from JSON
                form_data = json.loads(post_data.decode('utf-8'))
                
                # Create filename based on name and time
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = "".join(c for c in form_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"application_{safe_name}_{timestamp}.txt"
                
                # Write data to text file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("=" * 50 + "\n")
                    file.write("JOB APPLICATION - CONFIDENTIAL\n")
                    file.write("=" * 50 + "\n\n")
                    
                    file.write(f"Application Submitted: {form_data['submissionTime']}\n")
                    file.write(f"Full Name: {form_data['name']}\n")
                    file.write(f"Address: {form_data['address']}\n")
                    file.write(f"Phone Number: {form_data['phone']}\n")
                    file.write(f"Email Address: {form_data['email']}\n")
                    file.write(f"Date of Birth: {form_data['birthdate']}\n")
                    file.write(f"Age: {form_data['age']} years\n")
                    
                    file.write("\n" + "=" * 50 + "\n")
                    file.write("Application Status: RECEIVED\n")
                    file.write(f"Reference ID: APP-{timestamp}\n")
                    file.write("=" * 50 + "\n")
                
                # Prepare friendly response
                response_data = {
                    'status': 'success',
                    'message': 'Application submitted successfully! Your information has been received.',
                    'reference_id': f'APP-{timestamp}',
                    'timestamp': datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
                
                # Print friendly console message
                print("\n" + "✨" * 30)
                print("NEW APPLICATION RECEIVED!")
                print("✨" * 30)
                print(f"Applicant: {form_data['name']}")
                print(f"Contact: {form_data['email']} | {form_data['phone']}")
                print(f"Application saved: {filename}")
                print(f"Reference ID: APP-{timestamp}")
                print("✨" * 30 + "\n")
                
            except Exception as e:
                print(f"Error saving application: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {
                    'status': 'error', 
                    'message': 'We encountered an issue saving your application. Please try again.'
                }
                self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom log format to make console output cleaner
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {args[0]}")

def find_available_port(start_port=5000, end_port=5010):
    """Find an available port"""
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def open_browser():
    """Open browser after server starts"""
    webbrowser.open(f'http://localhost:{PORT}')

def print_welcome_message():
    """Print a friendly welcome message"""
    print("\n" + "🌟" * 40)
    print("🌟         CAREER APPLICATION SYSTEM         🌟")
    print("🌟" * 40)
    print("\nWelcome! The application form is now ready.")
    print("We're here to help candidates start their career journey!")
    print("\n" + "─" * 50)

def main():
    global PORT
    
    # Find available port
    PORT = find_available_port()
    if PORT is None:
        print("⚠️  No available port found! Please check your network.")
        return
    
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ApplicationHandler)
    
    # Print welcome message
    print_welcome_message()
    print(f"\n✅ Server is running on: http://localhost:{PORT}")
    print("📝 Application form is opening in your browser...")
    print("💾 Applications will be saved automatically")
    print("🛑 Press Ctrl+C when you're done\n")
    
    # Open browser automatically after 1.5 seconds
    Timer(1.5, open_browser).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using the Career Application System!")
        print("Have a great day! 🎯")
        httpd.server_close()

if __name__ == '__main__':
    # Check if HTML file exists
    if not os.path.exists('job_application.html'):
        print("⚠️  Application form not found!")
        print("Please make sure 'job_application.html' is in the same folder.")
        print("Creating a sample file...")
        
        # Create a simple HTML file if not found
        with open('job_application.html', 'w', encoding='utf-8') as f:
            f.write("<html><body><h1>Application Form</h1><p>Please download the complete HTML file.</p></body></html>")
    
    main()