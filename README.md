# Gengar-Academic-Paper-Analysis-o1

### Here is the distribution of the sample set papers

- Medicine: 6%
- Biology: 14%
- Physics: 8%
- Engineering: 12%
- Computer Science: 28%
- Environmental Science: 24%
- Social Sciences: 8%

### Bulk Analysis Comprehensive results

### Folder Structure

- app (entry point, flask app, and blueprints)
- analysis (script to call process pdfs, run gpt completions, and parse data objs)
- api (api endpoints)
- constants (constants for the app)
- data (data models)

### Blueprint Endpoints

http://18.138.195.151/pdf/upload

- /pdf/upload (upload pdfs for json return result)
- - PDF is file attachement in body
- - Returns json with id of the pdf
```
# return data scructure
{
  "pdf_name": "A Balance for Fairness: Fair Distribution Utilising Physics in Games of Characteristic Function Form.pdf",
  "timestamp": "2025-01-09 12:00:00",
   "summary":{
      "title":"A Balance for Fairness: Fair Distribution Utilising Physics in Games of Characteristic Function Form",
      "authors":"Song-Ju Kimyz, Taiki Takahashix, and Kazuo Sanoy",
      "published":"February 8, 2021",
      "errorCount":"13",
      "logicalErrorCount":"2",
      "methodicalErrorCount":"2",
      "calculationErrorCount":"3",
      "dataInconsistencyCount":"1",
      "citationErrorCount":"2",
      "formattingErrorCount":"3",
      "ethicalErrorCount":"0"
   },
   "logical":{
      "errors":[
         {
            "errorCategory":"Logical/Conceptual Errors",
            "issue":"Oversimplification in applying physical systems to solve linear programming problems for fairness.",
            "implications":"May lead to incorrect assumptions about the scalability and applicability of the proposed method to more complex scenarios.",
            "recommendation":"Provide a more detailed theoretical justification and explore the limitations of using physical systems for complex computational problems."
         },
         {
            "errorCategory":"Logical/Conceptual Errors",
            "issue":"Anthropomorphism in linking Themis' balance to the physical distribution system.",
            "implications":"Potential confusion regarding the analogy between mythological symbolism and the actual computational model.",
            "recommendation":"Clarify the metaphorical connections and ensure that symbolic representations do not obscure the technical explanations."
         }
      ]
   },
   "methodical":{
      "errors":[
         {
            "errorCategory":"Methodological Errors",
            "issue":"Lack of validation against standard computational methods.",
            "implications":"The effectiveness and efficiency claims of the physical method remain unsubstantiated without comparative analysis.",
            "recommendation":"Conduct comparative studies using traditional computational methods to validate and benchmark the proposed physical approach."
         },
         {
            "errorCategory":"Methodological Errors",
            "issue":"Unclear explanation of the experimental setup involving interlocked cylinders.",
            "implications":"Readers may find it difficult to replicate the experiment or understand how the physical system accurately models the linear programming problem.",
            "recommendation":"Provide a more detailed and clear description of the experimental apparatus and the underlying principles that ensure accurate modeling of the computational problem."
         }
      ]
   },
   "calculation":{
      "errors":[
         {
            "errorCategory":"Calculation Errors",
            "issue":"Incorrect formatting and potential logical errors in equations, such as eq. (23).",
            "implications":"Misinterpretation of the mathematical formulations could lead to incorrect implementation and results.",
            "recommendation":"Review and correct the formatting of all equations to ensure clarity and accuracy in mathematical expressions."
         },
         {
            "errorCategory":"Calculation Errors",
            "issue":"Presence of encoding errors and strange characters in mathematical notation.",
            "implications":"Creates confusion and hinders the readability and understanding of the mathematical content.",
            "recommendation":"Ensure that all mathematical symbols and equations are properly formatted and free from encoding issues."
         },
         {
            "errorCategory":"Calculation Errors",
            "issue":"Incomplete or misformatted equations that do not clearly convey the intended calculations.",
            "implications":"Leads to ambiguity in understanding the computational steps and results.",
            "recommendation":"Complete and correctly format all equations, providing necessary explanations to maintain clarity."
         }
      ]
   },
   "data_inconsistencies":{
      "errors":[
         {
            "errorCategory":"Data Inconsistencies",
            "issue":"Inconsistencies in the representation of participant counts and data examples.",
            "implications":"May undermine the reliability of the study by presenting conflicting or unclear data information.",
            "recommendation":"Ensure consistency in data representation across all examples and sections, and reconcile any discrepancies found."
         }
      ]
   },
   "citation":{
      "errors":[
         {
            "errorCategory":"Citation/Reference Issues",
            "issue":"Missing citations for certain theoretical claims and concepts.",
            "implications":"Weakens the credibility of the arguments by not adequately supporting them with existing literature.",
            "recommendation":"Add appropriate citations from peer-reviewed sources to support all theoretical claims and enhance the studyâs credibility."
         },
         {
            "errorCategory":"Citation/Reference Issues",
            "issue":"Inconsistent numbering and formatting of references.",
            "implications":"Creates confusion and makes it difficult for readers to locate and verify sources.",
            "recommendation":"Review and standardize the citation format to align with the chosen citation style guidelines."
         }
      ]
   },
   "formatting":{
      "errors":[
         {
            "errorCategory":"Formatting Errors",
            "issue":"Presence of encoding issues and strange characters throughout the document.",
            "implications":"Distracts readers and can obscure the intended meaning of the text.",
            "recommendation":"Proofread the document to remove encoding errors and ensure proper display of all characters."
         },
         {
            "errorCategory":"Formatting Errors",
            "issue":"Improper integration and referencing of figures and tables.",
            "implications":"Leads to confusion regarding the association between text and visual aids, hindering comprehension.",
            "recommendation":"Ensure all figures and tables are properly formatted, labeled, and referenced in the text according to journal guidelines."
         },
         {
            "errorCategory":"Formatting Errors",
            "issue":"Overall layout inconsistencies not adhering to standard journal submission guidelines.",
            "implications":"May result in rejection or delays in the publication process due to non-compliance with formatting requirements.",
            "recommendation":"Align the paperâs formatting with the specific guidelines provided by the target journal, including sections, headings, and style consistency."
         }
      ]
   },
   "ethical":{
      "errors":[
         
      ]
   }
}
```

### Setting up pythong project and Flask app

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the app

Run with
```
python -m app.entry
```

### Running in AWS with Guinicorn

```
python app.py --host=0.0.0.0 --port=5000
gunicorn -b 0.0.0.0:8000 app.entry:app
```

### Setting up Gunicorn server for constant use

Create/Edit the systemd service file:
```
sudo nano /etc/systemd/system/gunicorn.service
```
Add this configuration (using your verified working paths):
```
[Unit]
Description=Gunicorn instance for Gengar Paper Analysis
After=network.target

[Service]
User=devai
WorkingDirectory=/home/devai/Gengar-Academic-Paper-Analysis-o1
Environment="PATH=/home/devai/Gengar-Academic-Paper-Analysis-o1/venv/bin"
ExecStart=/home/devai/Gengar-Academic-Paper-Analysis-o1/venv/bin/gunicorn -b 0.0.0.0:8000 app.entry:app --workers 3 --timeout 120

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable gunicorn

# Start the service
sudo systemctl start gunicorn

# Check status
sudo systemctl status gunicorn
```

### Setting up Apache to serve the proxy

Here's how to install and set up Apache2 on Amazon Linux:
First, update your system:
```
sudo yum update
```

Install Apache (on Amazon Linux, it's called httpd):
```
sudo yum install httpd
```

Start the Apache service:
```
sudo systemctl start httpd
```

Enable Apache to start on boot:
```
sudo systemctl enable httpd
```

Check the status:
```
sudo systemctl status httpd
```

Allow HTTP traffic through the firewall:
```
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

### To view logs within your server
```
# View Gunicorn service logs
sudo journalctl -u gunicorn.service

# View last 100 lines
sudo journalctl -u gunicorn.service -n 100

# Follow logs in real-time (good for debugging)
sudo journalctl -u gunicorn.service -f
```
