# save_application.py - Simple version
import json
import datetime
import os

def save_application(data):
    """
    Save application data to text file
    """
    try:
        # Create filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"job_application_{safe_name}_{timestamp}.txt"
        
        # Write data to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("=" * 50 + "\n")
            file.write("JOB APPLICATION FORM\n")
            file.write("=" * 50 + "\n\n")
            
            file.write(f"📅 Submission Time: {data.get('submissionTime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
            file.write(f"👤 Full Name: {data['name']}\n")
            file.write(f"📍 Address: {data['address']}\n")
            file.write(f"📞 Phone Number: {data['phone']}\n")
            file.write(f"📧 Email Address: {data['email']}\n")
            file.write(f"🎂 Date of Birth: {data['birthdate']}\n")
            file.write(f"📅 Age: {data['age']} years\n")
            
            file.write("\n" + "=" * 50 + "\n")
            file.write("Data saved successfully\n")
            file.write("=" * 50 + "\n")
        
        print(f"✅ File created: {filename}")
        return filename
    
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = {
        'name': 'John Smith',
        'address': '123 Main Street, New York',
        'phone': '0550123456',
        'email': 'john.smith@example.com',
        'birthdate': '1990-05-15',
        'age': '33',
        'submissionTime': '2023-10-15 14:30:00'
    }
    
    # Save data
    saved_file = save_application(sample_data)
    if saved_file:
        print(f"📄 Data saved in: {saved_file}")