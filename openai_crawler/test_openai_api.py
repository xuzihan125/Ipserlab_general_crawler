from openai_crawler import OpenAI
import json

example = """
<body>
  <a href="/company">
   COMPANY
  </a>
  <div>
    <div>Jhon Wick</div>
    <div>this is an example person</div>
  </div>
  <div>
    <div>Test product</div>
    <div>this is a test product</div>
  </div>
</body>
"""

example_respond = """
{'company_name': '',
 'company_intro': '',
 'employees':[[name:'Jhon Wick', desc:'this is an example person']],
 'products':[['name':'Test product', desc:'this is a test product']],
 'patents':[]
 'relevant_links': ['/company']}
"""

payload = """
<body>
 <ul>
  <a href="/">
   Home
  </a>
  <a href="/company">
   COMPANY
  </a>
  <div>
   Technology
   <ul>
    <a href="/seh-pathway-1">
     sEH Pathway
    </a>
    <a href="/publications">
     Publications
    </a>
    <a href="/pipeline-1">
     Pipeline
    </a>
    <a href="/intellectual-property">
     Intellectual Property
    </a>
   </ul>
  </div>
  <a href="/media">
   Media
  </a>
  <a href="/invest">
   Investors
  </a>
  <a href="/contact">
   Contact
  </a>
 </ul>
 <div>
  <div>
   <a href="/">
   </a>
   <ul>
    <a href="/">
     Home
    </a>
    <a href="/company">
     COMPANY
    </a>
    <div>
     Technology
     <ul>
      <a href="/seh-pathway-1">
       sEH Pathway
      </a>
      <a href="/publications">
       Publications
      </a>
      <a href="/pipeline-1">
       Pipeline
      </a>
      <a href="/intellectual-property">
       Intellectual Property
      </a>
     </ul>
    </div>
    <a href="/media">
     Media
    </a>
    <a href="/invest">
     Investors
    </a>
    <a href="/contact">
     Contact
    </a>
   </ul>
  </div>
  <section>
   <nav>
    <a href="#intro">
     Intro
    </a>
    <a href="#story">
     Story
    </a>
    <a href="#ride">
     Ride
    </a>
   </nav>
   <div>
    <div>
     <div>
      Intro
      <div>
       Research and Development of
       Novel,Â First-In-Class Medications
       for Human Health
       <p>
        <a href="/seh-pathway-1">
         Explor
        </a>
        <a href="/seh-pathway-1">
         e Technology
        </a>
       </p>
      </div>
     </div>
     SCROLL DOWN
    </div>
    <div>
     <div>
      Intro
      <div>
       Research and Development of
       Novel,Â First-In-Class Medications
       for Human Health
       <p>
        <a href="/seh-pathway-1">
         Explor
        </a>
        <a href="/seh-pathway-1">
         e Technology
        </a>
       </p>
      </div>
     </div>
     <div>
      AccenGen Therapeutics, Inc. is an early-stage pharmaceutical company focused on developing products using soluble epoxide hydrolase (sEH) inhibitors (sEHI) and dual sEH/COX inhibitors for indications with fibrotic etiologies and highest unmet needs. Our highest priority indication is treating pulmonary fibrosis, a disease worse than many cancers.
      sEH studies have resulted in over 800 publications in top-tier peer-reviewed journals.
     </div>
    </div>
   </div>
   <div>
    <div>
     Story
     For something that touches us all.
    </div>
    <div>
     Story
     For something that touches us all.
    </div>
   </div>
   <div>
    <div>
     Ride
     <p>
      sEH core technology platform allows multiple product opportunities and diversified risk
      .
     </p>
    </div>
    <div>
     Ride
     <p>
      sEH core technology platform allows multiple product opportunities and diversified risk
      .
     </p>
    </div>
   </div>
  </section>
  <footer>
   <a href="#top">
    Top
   </a>
   <ul>
    <a href="/contact">
     Contact
    </a>
    <a href="/legal">
     Legal
    </a>
   </ul>
  </footer>
 </div>
</body>
"""

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system",
         "content": "You are a systematic assistant skilled in understanding the tree structure of HTML language. "
                    "Your task involves analyzing simplified HTML pages extracted from the original website. Your "
                    "role is to identify and list information related to the company in json format. Relevant "
                    "information includes the company's name(company_name), introduction(company_intro), employee "
                    "details(employee_detail), current products(current_product, include name and description), "
                    "patents (including names, descriptions, and patent numbers). Additionally, please provide any "
                    "links that may contain relevant information(relevant_links) at the end of your response. Please "
                    "return everything in a json "
                    "format."},
        {"role": "user", "content": "here is an example:\n" + example},
        {"role": "assistant", "content": example_respond},
        {"role": "user", "content": "please analysis this one. Discard anything from the example.\n" + payload}
    ]
)

content = completion.choices[0].message.content
result = json.loads(content)
print(result)
{'company_name': 'AccenGen Therapeutics, Inc.',
 'company_intro': 'AccenGen Therapeutics, Inc. is an early-stage pharmaceutical company focused on developing products using soluble epoxide hydrolase (sEH) inhibitors (sEHI) and dual sEH/COX inhibitors for indications with fibrotic etiologies and highest unmet needs. Our highest priority indication is treating pulmonary fibrosis, a disease worse than many cancers. sEH studies have resulted in over 800 publications in top-tier peer-reviewed journals.',
 'relevant_links': ['/company', '/seh-pathway-1', '/publications', '/pipeline-1', '/intellectual-property'],
 'current_products': [{'name': 'sEH Pathway', 'desc': ''}], 'patents': []}

{'company_name': 'AccenGen Therapeutics, Inc.',
 'company_intro': 'AccenGen Therapeutics, Inc. is an early-stage pharmaceutical company focused on developing products using soluble epoxide hydrolase (sEH) inhibitors (sEHI) and dual sEH/COX inhibitors for indications with fibrotic etiologies and highest unmet needs. Our highest priority indication is treating pulmonary fibrosis, a disease worse than many cancers. sEH studies have resulted in over 800 publications in top-tier peer-reviewed journals.',
 'relevant_links': ['/', '/company', '/seh-pathway-1', '/publications', '/pipeline-1', '/intellectual-property',
                    '/media', '/invest', '/contact', '/legal']}

# {'company_name': 'AccenGen Therapeutics, Inc.',
#  'company_intro': 'AccenGen Therapeutics, Inc. is an early-stage pharmaceutical company focused on developing products using soluble epoxide hydrolase (sEH) inhibitors (sEHI) and dual sEH/COX inhibitors for indications with fibrotic etiologies and highest unmet needs. Our highest priority indication is treating pulmonary fibrosis, a disease worse than many cancers. sEH studies have resulted in over 800 publications in top-tier peer-reviewed journals.',
#  'relevant_links': ['/', '/company', '/seh-pathway-1', '/intellectual-property']}
