# 🤖 CodeAggregatorAI - Quickstart Guide 🚀

## Table of Contents 📑
- [1. Introduction](#1-introduction)
- [2. Setup and Installation](#2-setup-and-installation)
    - [2.1 Installing Miniconda](#21-installing-miniconda)
        - [2.1.1 Windows Installation](#211-windows-installation)
        - [2.1.2 MacOS Installation](#212-macos-installation)
    - [2.2 Creating a Conda Environment](#22-creating-a-conda-environment)
    - [2.3 Getting Your Groq API Key](#23-getting-your-groq-api-key)
- [3. User Interface Overview](#3-user-interface-overview)
- [4. Features ✨](#4-features)
    - [4.1 Generate Codebase ✍️](#41-generate-codebase)
    - [4.2 Ask Groq ❓](#42-ask-groq)
    - [4.3 Help Section ❓](#43-help-section)
- [5. Settings and Configuration ⚙️](#5-settings-and-configuration)
- [6. Advanced Features 🚀](#6-advanced-features) (Future Development)
    - [6.1 Enhanced Code Analysis 🧠](#61-enhanced-code-analysis)
    - [6.2 Integration with Code Editors 💻](#62-integration-with-code-editors)
    - [6.3 Collaborative Features 🤝](#63-collaborative-features)
    - [6.4 Custom Model Fine-Tuning ⚙️](#64-custom-model-fine-tuning)
- [7. Troubleshooting 🧰](#7-troubleshooting)
- [8. Best Practices 👍](#8-best-practices)
- [9. FAQ 🤔](#9-faq)
- [10. Version History 🕰️](#10-version-history)

## 1. Introduction <a name="1-introduction"></a>

CodeAggregatorAI is a powerful application designed to aggregate an entire GitHub repository into a single, organized Markdown file, making it easy to feed to AI systems for tasks like code summarization, question answering, refactoring and code generation.  🧠

Key Features:
- Aggregates all files from a GitHub repository, including code, documentation, and configuration files.
- Ignores common build artifacts and unnecessary files to focus on relevant code.
- Outputs a single Markdown file with a clear structure for easy AI processing.
- Provides options for whitespace removal and custom ignore patterns.
- Allows users to ask questions about the codebase using Groq's Llama 3 AI models.

## 2. Setup and Installation <a name="2-setup-and-installation"></a>

To run the CodeAggregatorAI application, you'll need to set up your environment and install the necessary dependencies. 🏗️

### 2.1 Installing Miniconda <a name="21-installing-miniconda"></a>

Miniconda is a minimal installer for Conda, which we'll use to manage our Python environments. 🐍

#### 2.1.1 Windows Installation <a name="211-windows-installation"></a>

1. Visit the Miniconda download page: https://docs.conda.io/en/latest/miniconda.html
2. Download the appropriate installer for your Windows system architecture (32-bit or 64-bit).
3. Run the downloaded installer.
4. Follow the installation wizard, using the default options unless you have specific preferences.
5. **Important:** During installation, make sure to check the box that says "Add Miniconda3 to my PATH environment variable".
6. After installation, open a new Command Prompt and verify by running:

```bash
conda --version
```

#### 2.1.2 MacOS Installation <a name="212-macos-installation"></a>

1. Visit the Miniconda download page: https://docs.conda.io/en/latest/miniconda.html
2. Download the MacOS installer (choose the appropriate version for your system architecture).
3. Open Terminal and navigate to the directory where you downloaded the installer.
4. Run the following command to make the installer executable:

```bash
chmod +x Miniconda3-latest-MacOSX-x86_64.sh
```

5. Run the installer:

```bash
./Miniconda3-latest-MacOSX-x86_64.sh
```

6. Follow the prompts to complete the installation.
7. Close and reopen Terminal to apply the changes.

### 2.2 Creating a Conda Environment <a name="22-creating-a-conda-environment"></a>

1. Open your terminal (Command Prompt for Windows, Terminal for macOS).
2. Create a new Conda environment named `codeaggregator-env` with Python 3.12 (or your preferred version):

```bash
conda create --name codeaggregator-env python=3.12
```

3. Activate the new environment:

```bash
conda activate codeaggregator-env
```

4.  **To deactivate the environment later:**

```bash
conda deactivate
```

### 2.3 Getting Your Groq API Key <a name="23-getting-your-groq-api-key"></a>

Groq API Key: This special key allows you to tap into Groq's powerful AI models. 

1. Get your free key at: https://groq.com/developers.
2. Sign up for a free account or log in if you already have one.
3. You'll find your API key in your account settings.

**How to use the Groq API Key:** Enter this special key in the left side of the Streamlit frontend UI in order to use the app.

### Prerequisites:
- Python 3.11 or higher 🐍
- pip (Python package manager) 📦

### Installation Steps:

1. Clone the repository or download the source code. 📥

2. Install required packages:
   ```
   pip install streamlit groq python-dotenv pandas PyPDF2 streamlit-extras streamlit-option-menu streamlit-lottie requests
   ```

3. Set up environment variables:
   Create a `.env` file in the project root directory and add the following:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

4. Run the application:
   ```
   streamlit run groq-codeaggregator-ai.py 
   ```

## 3. User Interface Overview <a name="3-user-interface-overview"></a>

The application features a clean and intuitive user interface divided into several sections:

- Header: Displays the application title and logo 📝
- Main Content Area: Contains input fields and output for codebase generation and AI insights. 🖼️
- Sidebar: Contains settings and configuration options, including Groq model selection and API key input. ⚙️

## 4. Features ✨ <a name="4-features"></a>

### 4.1 Generate Codebase ✍️ <a name="41-generate-codebase"></a>

This feature allows users to aggregate their entire GitHub repository into a single, organized Markdown file. 

**How to use:**

1. Enter the URL of your GitHub repository in the text input field. 
2. (Optional) Add custom ignore patterns in the text area, one pattern per line. This allows you to exclude specific files or directories from being included in the generated codebase.
3. Select the desired output format (markdown or jsonl) using the radio buttons.
4. Click the "📊 Generate Codebase" button.
5. The application will clone the repository, analyze its contents, and generate the codebase file.
6. You'll see statistics about the repository, including the total number of files, files included, files ignored, and the number of binary and SVG files.
7. A file tree representing the repository's structure will be displayed in JSON format.
8. A code analysis table will show information about each included code file, such as its language, total lines of code, comment lines, and comment ratio.
9. The generated codebase file will be saved to the "data" folder and a success message will be displayed.

**Features:**

- Aggregates all files in the specified directory and subdirectories
- Ignores common build artifacts and configuration files
- Outputs a single Markdown file containing the whole codebase
- Provides options for whitespace removal and custom ignore patterns

**NOTE!** For best results, re-upload the Markdown file before starting a new chat session to ensure the AI has the most up-to-date version of your codebase.

### 4.2 Ask Groq ❓ <a name="42-ask-groq"></a>

This feature allows users to ask questions about the generated codebase using Groq's Llama 3 AI models. 

**How to use:**

1. Upload the generated codebase file (in Markdown format) using the file uploader.
2. Type your question about the codebase in the text area provided.
3. Click the "Ask Groq" button.
4. The application will send the codebase content and your question to the selected Groq Llama 3 model.
5. The AI's response will be displayed in the output area.

### 4.3 Help Section ❓ <a name="43-help-section"></a>

The Help section provides detailed information on how to use the application, including:
- Step-by-step instructions for each feature 👣
- Tips for achieving better results 💡
- FAQ addressing common questions and concerns ❓

## 5. Settings and Configuration ⚙️ <a name="5-settings-and-configuration"></a>

The sidebar contains important settings and configuration options:

- API Key Input: Enter your Groq API key (required for functionality) 🔑
- Model Selection: Choose between different Groq Llama 3 model versions based on your needs. 🤖
- System Prompt Input: (Optional) Enter a custom system prompt to guide the AI's behavior and responses.

## 6. Advanced Features 🚀 <a name="6-advanced-features"></a> (Future Development)

The following are potential advanced features that could be added to CodeAggregatorAI in future versions:

### 6.1 Enhanced Code Analysis 🧠 <a name="61-enhanced-code-analysis"></a>

- Provide more detailed code analysis, such as function call graphs, variable usage analysis, and code complexity metrics.
- Identify potential code smells and suggest improvements.

### 6.2 Integration with Code Editors 💻 <a name="62-integration-with-code-editors"></a>

- Allow users to directly import codebases from popular code editors like VS Code and Atom.
- Enable seamless synchronization between the generated codebase and the user's code editor.

### 6.3 Collaborative Features 🤝 <a name="63-collaborative-features"></a>

- Implement user accounts and project management features to enable teams to collaborate on codebase analysis and AI interactions.
- Allow users to share generated codebases and AI insights with colleagues.

### 6.4 Custom Model Fine-Tuning ⚙️ <a name="64-custom-model-fine-tuning"></a>

- Provide options for users to fine-tune Groq's Llama 3 models on their own codebases to improve the AI's understanding of their specific code and domain.

## 7. Troubleshooting 🧰 <a name="7-troubleshooting"></a>

### 7.1 API Key Issues

If you encounter problems related to the Groq API key:
1. Ensure the API key is entered correctly in the sidebar. 🔑
2. Check that your API key has the necessary permissions and quota. 🔒
3. Verify your internet connection to ensure the API can be reached. 🌐

### 7.2 Model Performance Issues

If the AI-generated insights are not meeting expectations:
1. Try rephrasing your question to be more specific and clear.
2. Ensure that the uploaded codebase file is relevant to your question.
3. Experiment with different Groq Llama 3 model versions to find the best fit for your use case. 🤖

### 7.3 Codebase Generation Errors

If you encounter errors during codebase generation:
1. Double-check the GitHub repository URL for accuracy.
2. Verify that you have the necessary permissions to access the repository (if it's private).
3. Check the console logs for specific error messages that can help pinpoint the issue.

## 8. Best Practices 👍 <a name="8-best-practices"></a>

### 8.1 Codebase Generation

- Use the default ignore patterns to exclude unnecessary files and reduce the size of the generated codebase.
- Add custom ignore patterns to further refine the codebase and focus on the most relevant code.
- Choose the appropriate output format (Markdown or JSONL) based on your intended use case.

### 8.2 Asking Groq

- Be clear and specific in your questions about the codebase.
- Provide context and background information to help the AI understand your query.
- Experiment with different Groq Llama 3 models to find the one that best suits your needs.

## 9. FAQ 🤔 <a name="9-faq"></a>

### Q1: What is CodeAggregatorAI?

A1: CodeAggregatorAI is a tool that helps you prepare your codebase for use with AI. It takes your entire GitHub repository and turns it into a single, organized file that AI models can easily understand.

### Q2: Why should I use CodeAggregatorAI?

A2: Using CodeAggregatorAI has several benefits:

- **AI-Ready Code:**  It transforms your code into a format that AI models can easily process.
- **Organization:** It structures your codebase in a clear and logical way.
- **Efficiency:** It saves you time and effort by automating the process of code aggregation.
- **Insights:** It allows you to ask questions about your codebase using powerful AI models.

### Q3: How do I use CodeAggregatorAI?

A3: Using CodeAggregatorAI is simple:

1. **Provide the GitHub URL:** Enter the URL of your GitHub repository.
2. **Customize (Optional):** Add custom ignore patterns to exclude specific files or folders.
3. **Generate:** Click "Generate Codebase" to create your AI-ready file.
4. **Upload & Ask:** Upload the generated file and ask your coding questions to Groq's AI.

### Q4: What types of questions can I ask Groq about my codebase?

A4: You can ask a variety of questions, including:

- "Summarize the main functionality of this code."
- "What are the key classes and methods in this project?"
- "How does the authentication system work?"
- "Find any potential security vulnerabilities in the code."
- "Generate unit tests for this function."

### Q5: Can I use CodeAggregatorAI with private GitHub repositories?

A5: Yes, you can use CodeAggregatorAI with private repositories. However, you'll need to ensure that the application has the necessary permissions to access your repository.

### Q6: What are some best practices for using CodeAggregatorAI?

A6: Here are some tips for getting the most out of CodeAggregatorAI:

- **Use default and custom ignore patterns:**  Exclude unnecessary files to improve efficiency and focus on relevant code.
- **Choose the right output format:** Select Markdown for readability or JSONL for easier AI processing.
- **Be clear and specific in your questions:** Provide context and background information to help the AI understand your query.
- **Experiment with different Groq models:** Find the model that best suits your needs.

## 10. Version History <a name="10-version-history"></a>

### v1.0.0 (Current Version)
- Initial release of CodeAggregatorAI
- Features code aggregation, file analysis, and Groq AI integration

## Conclusion

CodeAggregatorAI is a valuable tool for developers looking to leverage the power of AI in their workflow. It simplifies the process of preparing your codebase for AI interaction, enabling you to gain insights, automate tasks, and build better software.

We encourage you to explore the capabilities of CodeAggregatorAI, experiment with different features, and provide feedback to help us improve the application. As AI continues to advance, tools like CodeAggregatorAI will become increasingly essential for developers who want to stay ahead of the curve.
