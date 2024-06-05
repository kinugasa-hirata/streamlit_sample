import streamlit as st
from pathlib import Path
import pandas as pd

def display_content(content):
  """Displays the file content as a code block."""
  if content:
    st.write("**File Content:**")
    st.code(content, language="text")

def create_dataframe(content):
  """Creates a DataFrame from semicolon-delimited content (optional sorting)."""
  if not content:
    return None

  # Split lines by semicolon, considering empty elements
  lines = [line.strip().split(";") for line in content.splitlines() if line.strip()]

  # Create DataFrame with appropriate column names (adjust if needed)
  df = pd.DataFrame(lines, columns=[f"Column {i+1}" for i in range(len(lines[0]))])

  # Optional sorting (uncomment if needed)
  # df = df.sort_values(by="Column 1")

  return df

def save_to_excel(df, filename):
  """Saves the DataFrame to an Excel file in the working directory."""
  try:
    # Get the script's absolute path (ensures correct saving location)
    script_path = Path(__file__).absolute()
    # Get the parent directory (working directory)
    working_dir = script_path.parent
    save_path = working_dir / filename  # Combine path and filename
    df.to_excel(save_path, index=False)  # Save without index
    st.success(f"DataFrame saved to Excel: {save_path}")
  except Exception as e:
    st.error(f"Error saving to Excel: {e}")

def main():
  """Main function for file upload, processing, and saving."""
  st.title("File Uploader, Processing, and Save to Excel (Working Directory)")

  # File Uploader
  uploaded_file = st.file_uploader(
      label="Drag and Drop your file here or click to browse",
      type=["txt", "csv"]
  )

  content = ""
  if uploaded_file is not None:
    try:
      content = str(uploaded_file.read(), 'utf-8')
      display_content(content)
    except Exception as e:
      st.error(f"Error reading file: {e}")

  # Data Processing and Save
  df = create_dataframe(content)
  if df is not None:
    # Display the DataFrame in the browser window
    st.dataframe(df)

    save_button = st.button("Save Dataframe to Excel")
    if save_button:
      save_filename = st.text_input("Enter filename (.xlsx)", "data.xlsx")
      if save_filename:
        save_to_excel(df, save_filename)

if __name__ == "__main__":
  main()
