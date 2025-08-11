# 🏛️ ADGM Compliant Corporate Agent

An intelligent AI assistant that reviews and validates legal documents for business incorporation and compliance under **Abu Dhabi Global Market (ADGM)** rules.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![ADGM](https://img.shields.io/badge/ADGM-Compliant-gold.svg)

## 🎯 Overview

This system helps users ensure they have all required documents, highlights compliance issues, and produces reviewed versions of documents with detailed comments and suggestions. It's not just a text-checker — it's a **compliance-focused document reviewer** that uses real ADGM regulations.

### Key Features

- 📄 **Multi-Document Upload** - Accept multiple .docx files simultaneously
- 🔍 **Document Type Classification** - Automatically identify document types (AoA, MoA, resolutions, forms)
- ✅ **Completeness Checking** - Verify against ADGM's official checklists
- 🚨 **Red Flag Detection** - Spot legal issues, wrong jurisdiction, missing clauses
- 💬 **Inline Commenting** - Insert comments directly in documents with ADGM law references
- 📊 **Compliance Scoring** - Generate compliance scores and status reports
- 🔧 **JSON Output** - Machine-readable summary of findings
- 🌐 **Web Interface** - Both Streamlit and Gradio interfaces available

## 🏗️ Architecture

### Core Components

1. **Document Classifier** (`src/document_classifier.py`)
   - Classifies uploaded documents by type
   - Detects business process type
   - Generates document completeness reports

2. **RAG System** (`src/rag_system.py`)
   - **Retrieval-Augmented Generation** using ADGM regulations + **Google Gemini LLM**
   - ChromaDB vector database for regulation storage
   - **Gemini-1.5-Flash** for contextual legal guidance generation (FREE)
   - Fallback to OpenAI or local models when needed

3. **Red Flag Detector** (`src/red_flag_detector.py`)
   - Detects compliance issues and legal red flags
   - Validates jurisdiction and governing law clauses
   - Checks document-specific requirements

4. **Document Processor** (`src/document_processor.py`)
   - Main orchestration component
   - Creates reviewed documents with inline comments
   - Generates comprehensive reports

5. **Web Interfaces**
   - **Streamlit** (`app.py`) - Full-featured interface
   - **Gradio** (`gradio_app.py`) - Alternative simple interface

## 📋 Supported Documents

### Company Formation & Governance
- Articles of Association (AoA)
- Memorandum of Association (MoA)
- Board Resolution Templates
- Shareholder Resolution Templates
- Incorporation Application Forms
- UBO Declaration Forms
- Register of Members and Directors

### Employment & HR
- Employment Contracts (2024 & 2019 templates)
- HR Policy Documents

### Compliance & Regulatory
- Data Protection Policies
- Annual Accounts & Filings
- Regulatory Templates

### Process Types Detected
- **Company Incorporation**
- **Private Company Limited**
- **Employment Setup**
- **Annual Compliance**

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API Key (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/adgm-compliant-corporate-agent.git
   cd adgm-compliant-corporate-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional - LLM features)**
   ```bash
   # Create .env file with your API keys (optional)
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
   ```

   **Note:** The system includes a **working Gemini API key** and will use **Google Gemini-1.5-Flash (FREE)** by default. You can optionally add your own API keys for enhanced usage limits.

### Quick Test

Run the basic functionality test to verify installation:
```bash
python test_basic_functionality.py
```

Expected output:
```
🚀 ADGM Compliance System - Basic Functionality Test
✅ Sample document created
✅ Document analysis completed
✅ 5 compliance issues detected
✅ Reviewed document generated
✅ JSON report saved
```

### Running the Application

#### Option 1: Streamlit Interface (Recommended)
```bash
streamlit run app.py
```
Navigate to `http://localhost:8501`

#### Option 2: Gradio Interface
```bash
python gradio_app.py
```
Navigate to `http://localhost:7860`

## 📖 Usage Guide

### 1. Upload Documents
- Click "Browse files" or drag & drop .docx files
- Upload multiple documents for comprehensive analysis
- Supported: Articles of Association, Memorandums, Contracts, etc.

### 2. Document Analysis
The system will automatically:
- Classify each document type
- Detect the business process (e.g., "Company Incorporation")
- Check completeness against ADGM requirements
- Identify red flags and compliance issues

### 3. Review Results
- **Overview Tab**: Compliance scores and summary
- **Process Analysis**: Document completeness check
- **Document Details**: Individual document analysis
- **Downloads**: Reviewed documents with comments
- **JSON Output**: Machine-readable results

### 4. Download Reviewed Documents
- Each document is returned with inline comments
- Comments include specific ADGM regulation references
- Suggestions for corrections provided

## 🔍 Red Flag Detection

The system automatically detects:

### High Severity Issues
- ❌ Wrong jurisdiction (UAE federal courts instead of ADGM)
- ❌ Incorrect governing law (UAE law instead of ADGM law)
- ❌ Wrong registration authority references
- ❌ Missing required document sections

### Medium Severity Issues
- ⚠️ Missing signature blocks
- ⚠️ Incomplete document sections
- ⚠️ Formatting issues

### Low Severity Issues
- ℹ️ Minor formatting inconsistencies
- ℹ️ Suggestions for improvement

## 📊 Compliance Scoring

| Score Range | Status | Description |
|-------------|---------|-------------|
| 90-100 | ✅ Compliant | Ready for submission |
| 70-89 | ⚠️ Minor Issues | Few corrections needed |
| 50-69 | ❌ Major Issues | Significant revisions required |
| 0-49 | 🚫 Non-Compliant | Major compliance failures |

## 🔧 Example JSON Output

```json
{
  "process": "Company Incorporation",
  "documents_uploaded": 4,
  "required_documents": 5,
  "missing_documents": ["Register of Members and Directors"],
  "issues_found": [
    {
      "document": "Articles of Association",
      "section": "Clause 3.1",
      "issue": "Jurisdiction clause does not specify ADGM",
      "severity": "High",
      "suggestion": "Update jurisdiction to ADGM Courts."
    }
  ]
}
```

## 🗂️ Project Structure

```
ADGM-compliant-corporate-agent/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration and ADGM sources
│   ├── document_classifier.py # Document type classification
│   ├── rag_system.py         # RAG system for ADGM regulations
│   ├── red_flag_detector.py  # Compliance issue detection
│   └── document_processor.py # Main document processing
├── examples/
│   ├── README.md
│   └── sample_*.docx         # Example documents
├── data/
│   └── vector_db/            # ChromaDB storage
├── temp/                     # Temporary uploads
├── output/                   # Generated reports
├── app.py                    # Streamlit interface
├── gradio_app.py            # Gradio interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔒 Environment Variables

Create a `.env` file in the root directory:

```bash
# OpenAI API Key (optional, for enhanced AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Vector Database Path
VECTOR_DB_PATH=./data/vector_db

# Temporary Upload Path
TEMP_UPLOAD_PATH=./temp

# Output Path for Reports
OUTPUT_PATH=./output
```

## 🛠️ Development

### Adding New Document Types

1. Update `DOCUMENT_TYPE_MAPPINGS` in `src/config.py`
2. Add classification logic in `src/document_classifier.py`
3. Add specific validation rules in `src/red_flag_detector.py`

### Adding New Red Flags

1. Update `RED_FLAGS` dictionary in `src/config.py`
2. Implement detection logic in `src/red_flag_detector.py`
3. Add corresponding ADGM regulation references

### Extending RAG Knowledge Base

1. Add new regulations to `_get_static_adgm_knowledge()` in `src/rag_system.py`
2. Update `ADGM_DOCUMENT_SOURCES` in `src/config.py`

## 📚 Official ADGM Sources

All compliance rules are based on official ADGM sources:

- [ADGM Registration Authority](https://www.adgm.com/registration-authority/registration-and-incorporation)
- [ADGM Legal Framework](https://www.adgm.com/legal-framework/guidance-and-policy-statements)
- [ADGM Company Setup](https://www.adgm.com/setting-up)
- [ADGM Employment Regulations](https://www.adgm.com/operating-in-adgm)

## ⚠️ Important Disclaimers

- **This tool provides guidance only** - Always consult with qualified legal professionals
- **Not a substitute for legal advice** - Use for preliminary document review
- **Regulations may change** - Always verify with current ADGM requirements
- **Document templates** - Use official ADGM templates when available

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/adgm-compliant-corporate-agent/issues)
- **Documentation**: [Wiki](https://github.com/your-repo/adgm-compliant-corporate-agent/wiki)
- **ADGM Official**: [ADGM Website](https://www.adgm.com)

## 🏆 Acknowledgments

- Abu Dhabi Global Market for providing comprehensive documentation
- ADGM Registration Authority for official templates and guidelines
- The open-source community for excellent tools and libraries

---

<div align="center">
<strong>Built with ❤️ for ADGM compliance</strong>
</div>
