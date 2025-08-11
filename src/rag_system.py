"""RAG (Retrieval-Augmented Generation) system for ADGM regulations"""

import os
import requests
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging
from bs4 import BeautifulSoup
from .config import ADGM_DOCUMENT_SOURCES, VECTOR_DB_PATH, OPENAI_API_KEY, GEMINI_API_KEY

# LLM integration - Try Gemini first, then OpenAI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = bool(GEMINI_API_KEY)
    if GEMINI_AVAILABLE:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        gemini_model = None
except ImportError:
    GEMINI_AVAILABLE = False
    gemini_model = None
    logging.warning("Gemini not available. Install with: pip install google-generativeai")

# OpenAI fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = bool(OPENAI_API_KEY)
    if OPENAI_AVAILABLE:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        openai_client = None
except ImportError:
    OPENAI_AVAILABLE = False
    openai_client = None
    logging.warning("OpenAI not available. Install with: pip install openai")

# Determine which LLM to use
LLM_AVAILABLE = GEMINI_AVAILABLE or OPENAI_AVAILABLE
PRIMARY_LLM = "gemini" if GEMINI_AVAILABLE else ("openai" if OPENAI_AVAILABLE else None)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ADGMRAGSystem:
    """RAG system for ADGM legal documents and regulations"""

    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collection_name = "adgm_regulations"
        self.collection = None
        self.llm_available = LLM_AVAILABLE
        self.primary_llm = PRIMARY_LLM
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the ChromaDB collection"""
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "ADGM regulations and legal documents"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
            self._populate_knowledge_base()
    
    def _populate_knowledge_base(self):
        """Populate the knowledge base with ADGM regulations"""
        logger.info("Populating knowledge base with ADGM regulations...")
        
        documents = []
        metadatas = []
        ids = []
        
        # Add static ADGM legal knowledge
        static_knowledge = self._get_static_adgm_knowledge()
        
        for i, (doc_id, content, metadata) in enumerate(static_knowledge):
            documents.append(content)
            metadatas.append(metadata)
            ids.append(f"static_{i}_{doc_id}")
        
        # Add comprehensive official document sources information from PDF
        for i, source in enumerate(ADGM_DOCUMENT_SOURCES):
            # Create detailed content for each source
            content = f"""
            ADGM Official Document Source:
            
            Category: {source.category}
            Document Type: {source.document_type}
            Official Link: {source.official_link}
            
            Compliance Information:
            - This is an official ADGM document template/guideline from the ADGM website
            - Must be used for ADGM compliance and regulatory requirements
            - All documents of this type should follow these official templates and guidelines
            - Deviations from official ADGM templates may result in non-compliance
            
            Usage Context:
            {self._get_document_usage_context(source.category, source.document_type)}
            
            Regulatory Requirements:
            {self._get_regulatory_requirements(source.category)}
            """
            
            metadata = {
                "category": source.category,
                "document_type": source.document_type,
                "source": "official_adgm",
                "link": source.official_link,
                "compliance_level": "mandatory"
            }
            
            documents.append(content)
            metadatas.append(metadata)
            ids.append(f"official_{i}")
        
        # Add to vector database
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to knowledge base")
    
    def _get_static_adgm_knowledge(self) -> List[tuple]:
        """Get static ADGM legal knowledge"""
        knowledge = [
            (
                "jurisdiction_requirement",
                """
                ADGM Jurisdiction Requirements:
                All ADGM registered entities must specify ADGM Courts as the jurisdiction for dispute resolution.
                References to UAE Federal Courts, Dubai Courts, or other emirate courts are not compliant.
                The correct jurisdiction clause should read: "The ADGM Courts shall have exclusive jurisdiction over any disputes arising from this document."
                """,
                {"type": "jurisdiction", "severity": "high", "compliance_area": "legal"}
            ),
            (
                "governing_law",
                """
                ADGM Governing Law Requirements:
                All ADGM company documents must be governed by ADGM law and regulations.
                References to UAE Federal Law, Dubai Law, or other emirate laws are non-compliant.
                The correct governing law clause should state: "This document shall be governed by and construed in accordance with the laws of Abu Dhabi Global Market."
                """,
                {"type": "governing_law", "severity": "high", "compliance_area": "legal"}
            ),
            (
                "registration_authority",
                """
                ADGM Registration Authority Requirements:
                All ADGM entities must be registered with the ADGM Registration Authority.
                References to Department of Economic Development (DED), UAE Ministry, or other registration authorities are incorrect.
                All registration-related matters must reference the "ADGM Registration Authority" as the competent authority.
                """,
                {"type": "registration", "severity": "high", "compliance_area": "regulatory"}
            ),
            (
                "company_formation_documents",
                """
                Required Documents for ADGM Company Formation:
                1. Memorandum of Association (MoA)
                2. Articles of Association (AoA)
                3. Incorporation Application Form
                4. UBO Declaration Form
                5. Register of Members and Directors
                6. Board Resolution for Incorporation (if applicable)
                
                All documents must comply with ADGM templates and regulations.
                """,
                {"type": "checklist", "severity": "medium", "compliance_area": "formation"}
            ),
            (
                "signature_requirements",
                """
                ADGM Document Signature Requirements:
                All legal documents must include proper signature blocks for authorized signatories.
                Documents must be signed by directors, company secretary, or other authorized persons as applicable.
                Electronic signatures are acceptable if they comply with ADGM Electronic Transactions Regulations.
                Unsigned documents or documents without proper signature blocks may be rejected.
                """,
                {"type": "signatures", "severity": "medium", "compliance_area": "formal"}
            ),
            (
                "articles_of_association_requirements",
                """
                ADGM Articles of Association Requirements:
                Must include: Company name, registered office address, objects and powers, share capital structure,
                directors' powers and responsibilities, shareholder rights, dividend distribution rules,
                meeting procedures, and dissolution procedures.
                Must specify ADGM Courts jurisdiction and ADGM law as governing law.
                Must comply with ADGM Companies Regulations format and content requirements.
                """,
                {"type": "articles", "severity": "high", "compliance_area": "formation"}
            ),
            (
                "ubo_declaration_requirements",
                """
                ADGM Ultimate Beneficial Owner (UBO) Declaration Requirements:
                Must identify all persons who own or control 25% or more of the company.
                Must include full personal details, nationality, address, and nature of control.
                Must be updated within 14 days of any changes.
                Required for all ADGM company types except publicly listed companies.
                """,
                {"type": "ubo", "severity": "high", "compliance_area": "compliance"}
            ),
            (
                "employment_contract_requirements",
                """
                ADGM Employment Contract Requirements:
                Must comply with ADGM Employment Regulations 2019.
                Must include: employee details, job description, salary and benefits, working hours,
                notice periods, termination clauses, and dispute resolution (ADGM Employment Tribunal).
                Must specify ADGM law as governing law.
                Data protection clauses must comply with ADGM Data Protection Regulation.
                """,
                {"type": "employment", "severity": "medium", "compliance_area": "employment"}
            )
        ]
        return knowledge
    
    def query_regulations(self, query: str, n_results: int = 5) -> List[Dict]:
        """Query the ADGM regulations knowledge base"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error querying regulations: {str(e)}")
            return []
    
    def get_compliance_guidance(self, document_type: str, issue_type: str) -> Optional[str]:
        """Get specific compliance guidance for document type and issue using RAG + LLM"""
        query = f"{document_type} {issue_type} ADGM compliance requirements"
        results = self.query_regulations(query, n_results=3)

        if results:
            # Use LLM to generate contextual guidance if available
            if self.llm_available:
                return self._generate_llm_guidance(document_type, issue_type, results)
            else:
                # Fallback to simple concatenation
                guidance_parts = []
                for result in results:
                    if result['metadata'].get('type') == issue_type or issue_type in result['content'].lower():
                        guidance_parts.append(result['content'])

                if guidance_parts:
                    return "\n\n".join(guidance_parts)

        return None

    def _generate_llm_guidance(self, document_type: str, issue_type: str, rag_results: List[Dict]) -> str:
        """Generate contextual guidance using LLM with RAG context"""
        try:
            # Prepare context from RAG results
            context = "\n\n".join([result['content'] for result in rag_results[:3]])

            prompt = f"""You are an ADGM legal compliance expert. Based on the following official ADGM regulations and guidelines, provide specific guidance for a {document_type} document regarding {issue_type}.

ADGM Regulations Context:
{context}

Please provide:
1. Specific requirements for {document_type} regarding {issue_type}
2. Exact compliance steps needed
3. Reference to relevant ADGM regulations
4. Suggested corrective actions

Keep the response focused, professional, and cite specific ADGM requirements."""

            # Try Gemini first
            if self.primary_llm == "gemini" and gemini_model:
                response = gemini_model.generate_content(prompt)
                return response.text.strip()

            # Fallback to OpenAI
            elif self.primary_llm == "openai" and openai_client:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert ADGM legal compliance advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()

            else:
                # No LLM available, use fallback
                return "\n\n".join([result['content'] for result in rag_results[:2]])

        except Exception as e:
            logger.error(f"Error generating LLM guidance: {str(e)}")
            # Fallback to simple concatenation
            return "\n\n".join([result['content'] for result in rag_results[:2]])

    def generate_enhanced_analysis(self, document_text: str, document_type: str, detected_issues: List[Dict]) -> Dict:
        """Generate enhanced document analysis using LLM with RAG context"""
        if not self.llm_available:
            return {"enhanced_analysis": "LLM analysis not available", "llm_available": False}

        try:
            # Get relevant ADGM context
            query = f"{document_type} ADGM compliance requirements legal review"
            rag_results = self.query_regulations(query, n_results=5)
            context = "\n\n".join([result['content'] for result in rag_results[:3]])

            # Prepare issues summary
            issues_summary = "\n".join([
                f"- {issue.get('issue', 'Unknown issue')} (Severity: {issue.get('severity', 'Unknown')})"
                for issue in detected_issues[:5]
            ])

            prompt = f"""You are an expert ADGM legal compliance reviewer. Analyze this {document_type} document for ADGM compliance.

ADGM Regulations Context:
{context}

Document Type: {document_type}

Detected Issues:
{issues_summary}

Document Excerpt (first 1000 chars):
{document_text[:1000]}...

Please provide:
1. Overall compliance assessment (0-100% score)
2. Priority ranking of issues (Critical/High/Medium/Low)
3. Specific ADGM regulation references for each issue
4. Step-by-step remediation plan
5. Additional compliance considerations not yet detected

Format as JSON with keys: compliance_score, priority_issues, adgm_references, remediation_plan, additional_considerations"""

            # Try Gemini first
            if self.primary_llm == "gemini" and gemini_model:
                response = gemini_model.generate_content(prompt)
                response_text = response.text.strip()

                # Parse JSON response
                import json
                try:
                    analysis = json.loads(response_text)
                    analysis["llm_available"] = True
                    analysis["llm_used"] = "gemini"
                    return analysis
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    return {
                        "enhanced_analysis": response_text,
                        "compliance_score": 0,
                        "llm_available": True,
                        "llm_used": "gemini"
                    }

            # Fallback to OpenAI
            elif self.primary_llm == "openai" and openai_client:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert ADGM legal compliance advisor. Respond in JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.2
                )

                # Parse JSON response
                import json
                try:
                    analysis = json.loads(response.choices[0].message.content.strip())
                    analysis["llm_available"] = True
                    analysis["llm_used"] = "openai"
                    return analysis
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    return {
                        "enhanced_analysis": response.choices[0].message.content.strip(),
                        "compliance_score": 0,
                        "llm_available": True,
                        "llm_used": "openai"
                    }

            else:
                return {"enhanced_analysis": "No LLM available", "llm_available": False}

        except Exception as e:
            logger.error(f"Error generating enhanced analysis: {str(e)}")
            return {"enhanced_analysis": f"LLM analysis error: {str(e)}", "llm_available": False}
    
    def get_official_template_link(self, document_type: str) -> Optional[str]:
        """Get official ADGM template link for document type"""
        for source in ADGM_DOCUMENT_SOURCES:
            if document_type.lower() in source.document_type.lower():
                return source.official_link
        return None
    
    def validate_jurisdiction_clause(self, text: str) -> Dict:
        """Validate jurisdiction clauses in document text"""
        issues = []
        suggestions = []
        
        text_lower = text.lower()
        
        # Check for incorrect jurisdiction references
        incorrect_jurisdictions = [
            "uae federal court", "dubai court", "sharjah court", "abu dhabi court",
            "federal court", "local court"
        ]
        
        for incorrect in incorrect_jurisdictions:
            if incorrect in text_lower:
                issues.append(f"References incorrect jurisdiction: {incorrect}")
                suggestions.append("Update to specify ADGM Courts as the exclusive jurisdiction")
        
        # Check for missing ADGM jurisdiction
        adgm_patterns = ["adgm court", "abu dhabi global market court"]
        has_adgm_jurisdiction = any(pattern in text_lower for pattern in adgm_patterns)
        
        if not has_adgm_jurisdiction and ("jurisdiction" in text_lower or "court" in text_lower):
            issues.append("Missing ADGM Courts jurisdiction specification")
            suggestions.append("Add clause: 'The ADGM Courts shall have exclusive jurisdiction'")
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "compliant": len(issues) == 0
        }
    
    def validate_governing_law(self, text: str) -> Dict:
        """Validate governing law clauses in document text"""
        issues = []
        suggestions = []
        
        text_lower = text.lower()
        
        # Check for incorrect governing law references
        incorrect_laws = ["uae law", "dubai law", "federal law", "sharjah law"]
        
        for incorrect in incorrect_laws:
            if incorrect in text_lower:
                issues.append(f"References incorrect governing law: {incorrect}")
                suggestions.append("Update to specify ADGM law as governing law")
        
        # Check for missing ADGM governing law
        adgm_patterns = ["adgm law", "abu dhabi global market law", "laws of adgm"]
        has_adgm_law = any(pattern in text_lower for pattern in adgm_patterns)
        
        if not has_adgm_law and ("governing law" in text_lower or "governed by" in text_lower):
            issues.append("Missing ADGM law as governing law")
            suggestions.append("Add clause: 'governed by the laws of Abu Dhabi Global Market'")
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "compliant": len(issues) == 0
        }
    
    def _get_document_usage_context(self, category: str, document_type: str) -> str:
        """Get usage context for document types"""
        context_map = {
            "Company Formation & Governance": "Used for establishing legal structure and governance framework of ADGM companies",
            "Company Formation": "Required for company incorporation process in ADGM",
            "Company Formation & Compliance": "Essential for company setup and ongoing regulatory compliance",
            "Policy & Guidance": "Provides official guidance on ADGM legal framework and compliance requirements",
            "ADGM Company Set-up": "Mandatory checklists to ensure complete document submission for company registration",
            "Employment & HR": "Required for employment relationships and HR compliance in ADGM",
            "Data Protection": "Mandatory for companies handling personal data under ADGM Data Protection Regulation",
            "Compliance & Filings": "Required for ongoing regulatory compliance and annual obligations",
            "Letters/Permits": "Used for obtaining official letters and permits from ADGM authorities",
            "Regulatory Guidance": "Official guidance on ADGM regulations and compliance procedures",
            "Regulatory Template": "Official templates for regulatory documents and filings"
        }
        return context_map.get(category, "Official ADGM document for regulatory compliance")
    
    def _get_regulatory_requirements(self, category: str) -> str:
        """Get regulatory requirements for document categories"""
        requirements_map = {
            "Company Formation & Governance": """
            - Must comply with ADGM Companies Regulations
            - Requires ADGM Courts jurisdiction clauses
            - Must specify ADGM law as governing law
            - Requires proper signature by authorized persons
            """,
            "Company Formation": """
            - Must be filed with ADGM Registration Authority
            - Requires board approval and proper execution
            - Must include all required shareholder details
            - Subject to ADGM incorporation procedures
            """,
            "Employment & HR": """
            - Must comply with ADGM Employment Regulations 2019
            - Requires ADGM Employment Tribunal jurisdiction
            - Must include data protection compliance clauses
            - Subject to ADGM employment law requirements
            """,
            "Data Protection": """
            - Must comply with ADGM Data Protection Regulation 2021
            - Requires appointment of Data Protection Officer if applicable
            - Must include lawful basis for processing personal data
            - Subject to ADGM Office of Data Protection oversight
            """,
            "Compliance & Filings": """
            - Must be filed within statutory deadlines
            - Requires proper auditor certification where applicable
            - Must comply with ADGM accounting standards
            - Subject to ADGM Registration Authority review
            """
        }
        return requirements_map.get(category, "Must comply with applicable ADGM regulations and requirements")
