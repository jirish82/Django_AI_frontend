import os
import fnmatch

def should_include_file(filename):
    # List of file patterns to include
    include_patterns = [
        '*.py',
        '*.html',
        '*.js',
        '*.css',
        'requirements.txt',
        'manage.py',
    ]
    
    # List of file patterns to exclude
    exclude_patterns = [
        '*.pyc',
        '*.pyo',
        '__pycache__',
        '*.git*',
        '*.sqlite3',
        '*.log',
    ]
    
    # Check if the file should be included
    for pattern in include_patterns:
        if fnmatch.fnmatch(filename, pattern):
            for exclude in exclude_patterns:
                if fnmatch.fnmatch(filename, exclude):
                    return False
            return True
    return False

def generate_project_file(app_name, output_file):
    app_dir = os.path.join(os.getcwd(), app_name)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                if should_include_file(file):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, start=os.getcwd())
                    
                    outfile.write(f"File: {relative_path}\n")
                    outfile.write("=" * (len(relative_path) + 6) + "\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                    except UnicodeDecodeError:
                        outfile.write("(Binary file, content not shown)")
                    
                    outfile.write("\n\n")

if __name__ == "__main__":
    app_name = "ai_conversation"
    output_file = "ai_conversation_project_files.txt"
    
    generate_project_file(app_name, output_file)
    print(f"Project files have been compiled into {output_file}")