import os
import glob

directory = r"c:\Users\User\Desktop\ttj\frontend\src"
for ext in ["**/*.ts", "**/*.tsx"]:
    for filepath in glob.glob(os.path.join(directory, ext), recursive=True):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if "http://localhost:8000" in content:
                content = content.replace("http://localhost:8000", "")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            
print("Done")
