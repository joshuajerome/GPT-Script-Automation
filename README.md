# GPT-Script-Automation
[![](https://img.shields.io/badge/Dell-blue?style=for-the-badge)](https://www.dell.com/en-us)
[![](https://img.shields.io/badge/iDRAC-red?style=for-the-badge)](https://www.dell.com/en-us/dt/solutions/openmanage/idrac.htm)
[![](https://img.shields.io/badge/iDRAC_Redfish_Scripting-yellow?style=for-the-badge)](https://github.com/dell/iDRAC-Redfish-Scripting)

### Table of Contents
- **[project details](https://github.com/joshuajerome/GPT-Script-Automation#project-details)**
  - _[project goals](https://github.com/joshuajerome/GPT-Script-Automation#-project-goals-)_
  - _[project non-goals](https://github.com/joshuajerome/GPT-Script-Automation#project-non-goals)_
  - _[Artifcats OK to be fed into LLMs](https://github.com/joshuajerome/GPT-Script-Automation#artifacts-ok-to-be-fed-into-llm-ie-gpt)_
  - _[Artifacts NOT to be fed into LLMs](https://github.com/joshuajerome/GPT-Script-Automation#artifacts-not-to-be-fed-into-llm-ie-gpt)_

## Project Details

### Project Goals

  - pass in login credentials
  - choose a python script (example.py) from Dell's public github
  - choose flags that are valid only for example.py
    
### **_In respone, the code will:_**

 1. **Read & store: any ip, username, password, and any other flags that can-not & should-not be automated**

 2. **Fetch and generate output for desired REDFISH script**
    1. Fetch the file from Idrac Redfish Scripting repo using github API
    2. Stores the file as a temporary .py locally
    3. Executes "run.sh" on example.py
    4. Stores the output in example.out

 3. **Fetch the appropriate LLM (GPT) instructions**
    1. Access GPT api and feed GPT the instructions
    2. Store GPT generated script/code locally (gpt_example.py)
    3. Executres "gpt.sh" on gpt_example.py
    4. Stores the output in gpt_example.out

  - Original python script, expected output, GPT instructions, GPT Python Script, and GPT output should be available for viewing & comparing differences.
  - Create a Wiki page with project, progress, problems faced, problems addressed, solutions

### Project Non-Goals

  - Explore public APIs for github & desired LLM
  - Learn how to increase automation while preserving security

### Artifacts OK to be fed into LLM (i.e. GPT)

  - script specific LLM instructions

### Artifacts NOT to be fed into LLM (i.e. GPT)

  - login credentials (including ip of iDRAC server)
  - expected/generated outputs of python scripts

