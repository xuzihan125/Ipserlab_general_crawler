Example = """
        <body>
          <a href="/company">
           COMPANY
          </a>
          <div>
            <div>Jhon Wick</div>
            <div>this is an example person. He is the C.E.O. of the company</div>
          </div>
          <div>
            <div href="http://test_product.com">Test product</div>
            <div>this is a test product</div>
          </div>
          <div>
            <div href="http://test_publication.com">Test publication</div>
          </div>
        </body>
        """

Example_Respond = """
        {"company_name": "",
         "company_intro": "",
         "employee_details":[[name:"Jhon Wick", position:"C.E.O.", desc:"this is an example person"]],
         "products":[["name":"Test product", desc:"this is a test product", link:"http://test_product.com"]],
         "publications":[["name":"Test publication", link:"http://test_publication.com"]],
         "patents":[]
         "relevant_links": ["/company"]}
        """

Description = """
    You are a systematic assistant skilled in understanding the tree structure of HTML language. 
    Your task involves analyzing simplified HTML pages extracted from the original website. 
    Your role is to identify and list information related to the company in json format. 
    Relevant information includes:
        the company's name(must use "company_name" as key word in respond), 
        introduction(must use "company_intro" as key word in respond), 
        employee details(must use "employee_details" as key word in respond), 
        products(must use "products" as key word in respond, contains name, description and link to the product), 
        publications(must use "publications" as key word in respond, include name(please include the full name of the publication), link to the publication)
        patents (must use "patents" as key word in respond, include names, descriptions, patent numbers and link to the patent). 
    Sometime current products, publications and patents may not have a link. You can just leave the link part as empty.
    if the company's name is already provided, consider things with different name as the product.
    Additionally, please provide any links that may contain relevant information(relevant_links) at the end of your response. Those link do not include those that could be pointing to a pdf file, CSS file or images. 
    Please return everything in a json format.
"""