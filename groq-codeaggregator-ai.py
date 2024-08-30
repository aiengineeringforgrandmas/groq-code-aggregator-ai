import streamlit as st
import os
import tempfile
import shutil
from git import Repo
from pathlib import Path
import fnmatch
import chardet
from typing import List, Tuple, Dict
import json
import re
import hashlib
from tqdm import tqdm
import time
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Groq API setup
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit UI
st.set_page_config(page_title="AI Digest: Code Aggregator", page_icon="🧠", layout="wide")

st.title("🧠 AI Digest: Code Aggregator")

# --- Groq Configuration ---
st.sidebar.title('Llama 3')
model = st.sidebar.selectbox(
    'Choose a Llama 3 model',
    ['llama3-70b-8192', 'llama3-8b-8192', 'llama3-groq-70b-8192-tool-use-preview', 'llama3-groq-8b-8192-tool-use-preview',
     'llama-3.1-8b-instant', 'llama-3.1-70b-versatile', 'llama3-groq-70b-8192-tool-use-preview']
)

# --- API Key Input ---
if not groq_api_key:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    if not groq_api_key:
        st.warning("Please enter a valid Groq API Key to continue.")
        st.stop()

# --- System Prompt Input ---
default_system_prompt = "You are a helpful and informative AI assistant."
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = default_system_prompt

if not default_system_prompt:
    new_system_prompt = st.sidebar.text_area("Enter System Prompt", value=st.session_state.system_prompt, key="new_system_prompt")
    if st.sidebar.button("Enter Prompt"):
        st.session_state.system_prompt = new_system_prompt
else:
    st.sidebar.text_area("Current System Prompt (set in backend)", value=st.session_state.system_prompt, disabled=True)

# Groq rate limits
RATE_LIMITS = {
    'llama3-70b-8192': {'requests_per_minute': 30, 'tokens_per_minute': 6000},
    'llama3-8b-8192': {'requests_per_minute': 30, 'tokens_per_minute': 30000},
    'llama3-groq-70b-8192-tool-use-preview': {'requests_per_minute': 30, 'tokens_per_minute': 15000},
    'llama3-groq-8b-8192-tool-use-preview': {'requests_per_minute': 30, 'tokens_per_minute': 15000},
    'llama-3.1-8b-instant': {'requests_per_minute': 30, 'tokens_per_minute': 131072},
    'llama-3.1-70b-versatile': {'requests_per_minute': 30, 'tokens_per_minute': 131072},
}

# Rate limiting function
def rate_limit(model):
    limit = RATE_LIMITS[model]['requests_per_minute']
    time.sleep(60 / limit)

# Utility functions

def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def escape_triple_backticks(content: str) -> str:
    return content.replace("```", "\\`\\`\\`")

def estimate_token_count(text: str) -> int:
    return len(text) // 4

def is_text_file(file_path: str) -> bool:
    try:
        with open(file_path, 'rb') as file:
            return not bool(file.read(1024).translate(None, bytes({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {7,8,9,10,12,13,27})))
    except:
        return False

def get_file_type(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()
    file_types = {
        'Image': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'},
        'SVG Image': {'.svg'},
        'WebAssembly': {'.wasm'},
        'PDF': {'.pdf'},
        'Word Document': {'.doc', '.docx'},
        'Excel Spreadsheet': {'.xls', '.xlsx'},
        'PowerPoint Presentation': {'.ppt', '.pptx'},
        'Compressed Archive': {'.zip', '.rar', '.7z'},
        'Executable': {'.exe'},
        'Dynamic-link Library': {'.dll'},
        'Shared Object': {'.so'},
        'Dynamic Library': {'.dylib'}
    }
    for file_type, extensions in file_types.items():
        if extension in extensions:
            return file_type
    return 'Binary'

def should_treat_as_binary(file_path: str) -> bool:
    return file_path.lower().endswith('.svg') or get_file_type(file_path) != 'Binary'

def detect_language(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.rs': 'Rust',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.m': 'Objective-C',
        '.sh': 'Shell',
        '.pl': 'Perl',
        '.lua': 'Lua',
        '.r': 'R',
        '.vb': 'Visual Basic',
        '.cs': 'C#',
        '.f': 'Fortran',
        '.sql': 'SQL',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.toml': 'TOML',
    }
    return language_map.get(extension, 'Unknown')

def count_lines_and_comments(content: str, language: str) -> Tuple[int, int]:
    lines = content.splitlines()
    total_lines = len(lines)
    comment_lines = 0
    comment_patterns = {
        'Python': r'^\s*#',
        'JavaScript': r'^\s*(//|/\*)',
        'Java': r'^\s*(//|/\*)',
        'C++': r'^\s*(//|/\*)',
        'C': r'^\s*(//|/\*)',
        'Ruby': r'^\s*#',
        'PHP': r'^\s*(//|#|/\*)',
    }
    pattern = comment_patterns.get(language)
    if pattern:
        comment_lines = sum(1 for line in lines if re.match(pattern, line))
    return total_lines, comment_lines

# Constants

WHITESPACE_DEPENDENT_EXTENSIONS = {
    '.py', '.yaml', '.yml', '.jade', '.haml', '.slim',
    '.coffee', '.pug', '.styl'
}

DEFAULT_IGNORES = [
    'node_modules', 'package-lock.json', 'npm-debug.log',
    'yarn.lock', 'yarn-error.log', 'pnpm-lock.yaml',
    'bun.lockb', 'deno.lock', 'vendor', 'composer.lock',
    '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.Python',
    'pip-log.txt', 'pip-delete-this-directory.txt',
    '.venv', 'venv', 'ENV', 'env', 'Gemfile.lock',
    '.bundle', 'target', '*.class', '.gradle', 'build',
    'pom.xml.tag', 'pom.xml.releaseBackup', 'pom.xml.versionsBackup',
    'pom.xml.next', 'bin', 'obj', '*.suo', '*.user',
    'go.sum', 'Cargo.lock', 'target', '.git', '.svn',
    '.hg', '.DS_Store', 'Thumbs.db', '.env', '.env.local',
    '.env.development.local', '.env.test.local', '.env.production.local',
    '*.env', '*.env.*', '.svelte-kit', '.next', '.nuxt',
    '.vuepress', '.cache', 'dist', 'tmp', 'codebase.md',
    '.turbo'
]

# Main functionality

def clone_repo(repo_url: str, target_dir: str) -> None:
    try:
        Repo.clone_from(repo_url, target_dir)
    except Exception as e:
        if "Auth" in str(e):
            raise Exception("Authentication error. The repository might be private or you may not have access.")
        elif "not found" in str(e):
            raise Exception("Repository not found. Please check the URL and try again.")
        else:
            raise Exception(f"An error occurred while cloning the repository: {str(e)}")

def read_ignore_file(input_dir: str, filename: str) -> List[str]:
    try:
        with open(os.path.join(input_dir, filename), 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

@st.cache_data
def aggregate_files(
    input_dir: str,
    use_default_ignores: bool,
    remove_whitespace_flag: bool,
    ignore_file: str,
    custom_ignore_patterns: List[str],
    output_format: str
) -> Tuple[str, int, int, int, int, List[str], Dict]:
    user_ignore_patterns = read_ignore_file(input_dir, ignore_file)
    ignored_patterns = set(DEFAULT_IGNORES + user_ignore_patterns + custom_ignore_patterns if use_default_ignores else user_ignore_patterns + custom_ignore_patterns)

    output = ""
    jsonl_output = []
    included_count = 0
    ignored_count = 0
    binary_and_svg_file_count = 0
    total_files = 0
    included_files = []
    file_tree = {"name": "root", "type": "directory", "children": []}
    code_analysis = {}

    for root, dirs, files in os.walk(input_dir):
        current_dir = file_tree
        for part in Path(root).relative_to(input_dir).parts:
            if not any(child['name'] == part for child in current_dir['children']):
                new_dir = {"name": part, "type": "directory", "children": []}
                current_dir['children'].append(new_dir)
            current_dir = next(child for child in current_dir['children'] if child['name'] == part)

        for file in tqdm(files, desc="Processing files", unit="file"):
            total_files += 1
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, input_dir)

            if any(fnmatch.fnmatch(relative_path, pattern) for pattern in ignored_patterns):
                ignored_count += 1
                continue

            current_dir['children'].append({"name": file, "type": "file"})

            if is_text_file(full_path) and not should_treat_as_binary(full_path):
                with open(full_path, 'rb') as f:
                    raw_content = f.read()
                    encoding = chardet.detect(raw_content)['encoding']
                content = raw_content.decode(encoding or 'utf-8', errors='ignore')
                
                content = escape_triple_backticks(content)
                
                if remove_whitespace_flag and Path(file).suffix not in WHITESPACE_DEPENDENT_EXTENSIONS:
                    content = remove_whitespace(content)
                
                language = detect_language(full_path)
                total_lines, comment_lines = count_lines_and_comments(content, language)
                
                if output_format == 'markdown':
                    output += f"# {relative_path}\n\n"
                    output += f"```{Path(file).suffix[1:]}\n"
                    output += content
                    output += "\n```\n\n"
                elif output_format == 'jsonl':
                    jsonl_output.append({
                        "path": relative_path,
                        "content": content,
                        "language": language,
                        "total_lines": total_lines,
                        "comment_lines": comment_lines
                    })

                included_count += 1
                included_files.append(relative_path)
                
                code_analysis[relative_path] = {
                    "language": language,
                    "total_lines": total_lines,
                    "comment_lines": comment_lines,
                    "comment_ratio": comment_lines / total_lines if total_lines > 0 else 0
                }
            else:
                file_type = get_file_type(full_path)
                if output_format == 'markdown':
                    output += f"# {relative_path}\n\n"
                    if file_type == 'SVG Image':
                        output += f"This is a file of the type: {file_type}\n\n"
                    else:
                        output += f"This is a binary file of the type: {file_type}\n\n"
                elif output_format == 'jsonl':
                    jsonl_output.append({
                        "path": relative_path,
                        "file_type": file_type,
                        "is_binary": True
                    })

                binary_and_svg_file_count += 1
                included_count += 1
                included_files.append(relative_path)

    if output_format == 'jsonl':
        output = "\n".join(json.dumps(item) for item in jsonl_output)

    return output, included_count, ignored_count, binary_and_svg_file_count, total_files, included_files, file_tree, code_analysis

# Groq AI Insights
def generate_ai_insights(uploaded_file, question: str) -> str:
    """Generates AI insights using the Groq API."""
    if uploaded_file is not None:
        code_summary = uploaded_file.getvalue().decode("utf-8")

        client = Groq(api_key=groq_api_key)
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": st.session_state.system_prompt},
                {"role": "user", "content": f"```\n{code_summary}\n```\nAnswer the user's question about the code above: \n{question}"}
            ],
            stream=True,
        )

        ai_insights = ""
        for chunk in chat_completion:
            if chunk.choices[0].delta.content is not None:
                ai_insights += chunk.choices[0].delta.content
                # You can update the UI with each chunk here if needed
                # For example: st.write(chunk.choices[0].delta.content, end='')

        return ai_insights.strip()
    else:
        return "Please upload a codebase file first."

repo_url = st.text_input("Enter GitHub repository URL:")

custom_ignore = st.text_area("Custom ignore patterns (one per line):", height=100)
custom_ignore_patterns = [pattern.strip() for pattern in custom_ignore.split('\n') if pattern.strip()]

output_format = st.radio("Select output format:", ("markdown", "jsonl"))

# Use session state to store the codebase summary
if 'codebase_summary' not in st.session_state:
    st.session_state.codebase_summary = None

if st.button("📊 Generate Codebase"):
    if repo_url:
        try:
            with st.spinner("Cloning repository and generating codebase..."):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    clone_repo(repo_url, tmp_dir)
                    
                    output, included_count, ignored_count, binary_count, total_files, included_files, file_tree, code_analysis = aggregate_files(
                        tmp_dir,
                        use_default_ignores=True,
                        remove_whitespace_flag=True,
                        ignore_file=".aidigestignore",
                        custom_ignore_patterns=custom_ignore_patterns,
                        output_format=output_format
                    )
                    
                    # Save the output to the data folder
                    data_folder = Path("data")
                    data_folder.mkdir(exist_ok=True)
                    output_file = data_folder / f"codebase.{output_format}"
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(output)
                    
                    st.success(f"✅ Codebase generated and saved to {output_file}")
                    
                    # Display statistics
                    st.write("📈 Repository Statistics:")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total files", total_files)
                    col2.metric("Files included", included_count)
                    col3.metric("Files ignored", ignored_count)
                    col4.metric("Binary and SVG files", binary_count)
                    
                    # Token count estimation
                    token_count = estimate_token_count(output)
                    st.metric("Estimated token count", token_count)
                    
                    # Display file tree
                    st.write("📁 Repository Structure:")
                    st.json(file_tree)
                    
                    # Display code analysis
                    st.write("📊 Code Analysis:")
                    analysis_df = pd.DataFrame.from_dict(code_analysis, orient='index')
                    st.dataframe(analysis_df)

                    # Store the codebase summary in session state
                    st.session_state.codebase_summary = output
                    st.session_state.codebase_file_path = output_file

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check the repository URL and try again.")
    else:
        st.warning("⚠️ Please enter a GitHub repository URL.")

# Groq AI Input
st.subheader("🤖 Ask Groq a Coding Related Question:")
uploaded_file = st.file_uploader("Upload Codebase File", type=["txt", "md"])
question = st.text_area("Enter your question:")
if st.button("Ask Groq"):
    if question:
        with st.spinner("Groq is thinking..."):
            ai_insights = generate_ai_insights(uploaded_file, question)
            st.write(ai_insights)
    else:
        st.warning("Please enter a question.")

# User Guide
st.sidebar.title("📚 User Guide")
st.sidebar.markdown("""
1. Enter the GitHub repository URL in the text box.
2. (Optional) Add custom ignore patterns, one per line.
3. Select the desired output format (markdown or jsonl).
4. Click the "Generate Codebase" button to start the process.
5. Review the generated statistics, file tree, and code analysis.
6. **Upload a document file using the file uploader.**
7. **Ask your questions about the codebase in the Groq input box.**

**Note:** For private repositories, make sure you have the necessary permissions.

**Tip:** Use custom ignore patterns to exclude specific files or directories from the analysis.
""")

# Cache Management
if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared successfully!")
