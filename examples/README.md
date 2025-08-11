# Example Documents

This folder contains example documents for testing the ADGM Compliant Corporate Agent.

## Sample Documents Included

1. **sample_articles_of_association.docx** - Example Articles of Association document
2. **sample_memorandum_of_association.docx** - Example Memorandum of Association document  
3. **sample_employment_contract.docx** - Example Employment Contract
4. **sample_ubo_declaration.docx** - Example UBO Declaration Form
5. **sample_board_resolution.docx** - Example Board Resolution

## Expected JSON Output

```json
{
  "process": "Company Incorporation",
  "documents_uploaded": 4,
  "required_documents": 5,
  "missing_documents": ["Register of Members and Directors"],
  "issues_found": [
    {
      "document": "sample_articles_of_association.docx",
      "section": "Clause 3.1",
      "issue": "Jurisdiction clause does not specify ADGM",
      "severity": "High",
      "suggestion": "Update jurisdiction to ADGM Courts."
    },
    {
      "document": "sample_employment_contract.docx",
      "section": "Clause 12",
      "issue": "Governing law references UAE federal law instead of ADGM law",
      "severity": "High", 
      "suggestion": "Replace with: governed by the laws of Abu Dhabi Global Market"
    }
  ]
}
```

## How to Test

1. Upload these sample documents through the web interface
2. Review the generated compliance analysis
3. Download the reviewed documents with inline comments
4. Check the JSON output matches the expected format

## Notes

- These are example documents for demonstration purposes
- Real documents should be prepared by qualified legal professionals
- Always verify compliance with current ADGM regulations
