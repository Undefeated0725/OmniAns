# Powerful AI agent for essay question answering and R&D automation

![Uploading Screenshot 2024-07-30 at 12.29.49 AM.png…]()

This is the first AI agent designed to assist in the brainstorming, structuring, and drafting of research thesis essays. It leverages advanced language models to generate sub-questions, outline essays, extract relevant information from PDFs, and refine the overall structure to produce a coherent and compelling thesis.

## Features

1. **Insight Analyst**:
   - Generates a list of sub-questions related to the research topic to help build a comprehensive thesis.

2. **Structural Outlining**:
   - Structures the essay based on the research question and sub-questions.
   - Provides a detailed outline, specifying the purpose of each paragraph, the evidence needed, and the development of the argument.

3. **PDF Text Extraction**:
   - Extracts text from PDF documents to gather relevant information and insights.
   - Summarizes the core ideas and essential information from the PDFs.

4. **Essay Restructuring**:
   - Revises the initial essay structure based on the extracted and summarized information.
   - Ensures that the final structure integrates all relevant contexts and insights.

5. **Paragraph Writing**:
   - Generates detailed and well-cited paragraphs based on the provided structure and extracted information.
   - Includes in-text citations and references for each paragraph.

6. **Final Essay Compilation**:
   - Compiles all the generated paragraphs into a coherent essay.
   - Adds smooth transitions and ensures a professional, compelling, and consistent tone throughout the essay.

## Workflow

### 1. Insight Analyst

```yaml
insight_analyst:
  action: prompt
  prompt: 
    - text: |
        You are an expert in brainstorming, analyzing, and researching. You are given a research question: 
        
        {{ message }}
        
        Your task is to generate a list of sub-questions that are related to this and will help in building a professional research thesis.
```

### 2. Structural Outlining

```yaml
structural_outlining:
  action: prompt
  prompt: 
    - text: |
        You are professional. You are in charge of structuring an essay that answers this question:
      
        {{ message }}

        Your colleague has brainstormed a list of sub-questions related to this essay. Take advantage of these and structure your argument. Your output should be a list of paragraphs that include 1) what the paragraph is for 2) what evidence is needed 3) how is the argument developed. Do not generate anything else except the list.

        List of sub-questions to explore

        {{ insight_analyst.result }}
```

### 3. PDF Text Extraction

```yaml
extract_pdf_texts:
  for: filepath
  in:
    var: pdf_filepaths
  flow:
    extractor:
      action: extract_pdf_text
      file:
        var: filepath
    summarize:
      action: prompt
      prompt:
        - text: |
            Summarize the core idea and essential information of the pdf structurally. 
            {{ extractor.full_text }}
```

### 4. Essay Restructuring

```yaml
restructurer:
  action: prompt
  prompt:
    - text: |
        You are professor from Oxford. You are in charge of revising the first draft of a structure of an essay written by a bright student. The student has not read anything before, so you will pay attention to combining the context into the structure to update a better one. 

        Make sure that nothing other than the new structure is outputted. 

        The question to answer is 

        {{message}}

        Your student has provided you with 

        {{structural_outlining.result}}

        The context you will use to revise & upgrade the structure:

        {% for pdf_result in extract_pdf_texts %}
          {{pdf_result.summarize.result}}
        {% endfor %}
```

### 5. Paragraph Writing

```yaml
essay_writer: 
  for: para_struct
  in: 
    link: get_json_string.json_object
  flow:
    key_gen:
      action: prompt
      prompt:
      - text: |
          The paragraph below is a part of a bigger essay, to answer the question {{message}}

          Paragraph:

          {{para_struct}}

          For the paragraph, generate a list of keywords that could be used to search up to paragraphs in the PDFs & knowledge base that are relevant to this paragraph. Focus on the evidence needed and how they will be incorporated for a better response.  
    extract_query:
      action: extract_xml_tag
      tag: query
      text:
          link: key_gen.result     
    retrieval:
      action: retrieve
      k: 10
      documents:
          lambda: |
              [{"title": page.title, "page_num": page.page_number, "text": paragraph}
              for flow in extract_pdf_texts
              for page in flow.extractor.pages
              for paragraph in page.text.split('\n')]                
      texts:
          lambda: |
              [paragraph
              for flow in extract_pdf_texts
              for page in flow.extractor.pages
              for paragraph in page.text.split('\n')]     
      query:
          link: extract_query.result         
    reranking:
      action: rerank
      k: 5
      documents:
          link: retrieval.result
      texts:
          lambda: |
              [paragraph
              for paragraph in retrieval.result['text']]
      query:
          link: extract_query.result
    para_writer:
      action: prompt
      prompt:
        - text: |
            You are in charge of writing a paragraph as part of a larger essay, focusing on {{message}}. Make Sure the paragraph you write is detailed and compelling. Write at least 200 words if not more. 

            You are given the paragraph's structure and several paragraphs in PDFs as important context. Use the context to fill in the structure to write a professional paragraph, including in-text citations to cite important facts or arguments from the sources. Make sure it is detailed and well-written to beat the Oxford standard.

            For each in-text citation, use the provided page number, article name, and author's name. Additionally, generate references corresponding to the in-text citations.

            Paragraph: {{para_struct}}
            
            Below are provided in order for each paragraph of context:
            
            titles: 
            {{retriveal.result['title']}}

            page numbers:
            {{retriveal.result['page_num']}}

            texts:
            {{retriveal.result['text']}}
```

### 6. Final Essay Compilation

```yaml
essayfinaliser:
  action: prompt
  prompt:
    - text: |
          You are an Oxford Professor. Your proud student has read a lot of reading to answer the question {{message}}. You have received his writing on each paragraph and the citations.

          You will organize the writing by connecting the paragraphs together and put the references in the end as appendixes. You will take the third-party perspective to check any inconsistencies between the paragraphs and add smooth transitions. Make sure that the overall tone is professional, compelling, and consistent. 
          
          {{essay1stdraft.string}}
```

## Installation and Usage

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-repository-url.git
   cd your-repository
   ```

2. **Install Dependencies**:
   Ensure you have the required Python packages installed.
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure YAML File**:
   Edit the `flow.yaml` file to customize the AI agent's workflow and configurations.

4. **Run the AI Agent**:
   Execute the main script to start the AI agent.
   ```sh
   python main.py
   ```

## Contributing

We welcome contributions from the community. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to the branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This README provides a comprehensive overview of the AI agent, its features, workflow, installation instructions, and contribution guidelines.
