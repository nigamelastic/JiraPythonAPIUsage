#!/usr/bin/env python
from jira import JIRA

import sys
import os
import configparser
import lxml.html


config = configparser.ConfigParser()
config.read("happy.config")
serverName = config.get('JIRA', 'serverName')
password = config.get('JIRA', 'password')
username = config.get('JIRA', 'username')
projectName = <ProjectName>

options = {
   'server': serverName,
   'verify': False,
   }
jira = JIRA(options, basic_auth=(username,password))
files = []

for file in os.listdir(sys.argv[1]):
   if '.html' in file:
       files.append(sys.argv[1]+'\\'+file)

for f in files:
    tree =lxml.html.parse(f)
    scanName = tree.xpath('//td[contains(text(),"Task:")]/following-sibling::td/text()')[0]
    summaryValue="Security Scan using OpenVAS for " + scanName 
    startTime = tree.xpath('//td[contains(text(),"Scan started:")]/following-sibling::td/b/text()')[0];
    endTime = tree.xpath('//td[contains(text(),"Scan ended:")]/following-sibling::td/text()')[0];
    descriptionText = summaryValue + " which started on " + startTime +  " and ended at " + endTime + ".\nThe systems include the following IPs :\n"
    allIPs= tree.xpath('//tr[contains(@class,"table_head")]/following-sibling::tr/td/a/text()')
    count =1
    midText =""
    for ip in allIPs:
        descriptionText=descriptionText+"\n"+ip
        xpathValue= '//h3[contains(text(),"Security")]['+str(count)+']'
        midText=midText+'\n\n'+tree.xpath(xpathValue+'/text()')[0]+'\n Severity :'+tree.xpath(xpathValue+'/following-sibling::div/b/text()')[0]+tree.xpath(xpathValue+'/following-sibling::div/div[2]/text()')[0]+'\nSummary : '+tree.xpath(xpathValue+'/following-sibling::div/b[contains(text(),"Summary")]/following-sibling::p/text()')[0]+'\nImpact : '+tree.xpath(xpathValue+'/following-sibling::div/b[contains(text(),"Impact")]//following-sibling::p/text()')[0]+'\n\n\n'

    descriptionText=descriptionText + "\n\n\nTop Issues for each IP Address :\n\n" +midText+ "Please check the attached scan report for more details. "

    new_issue = jira.create_issue(project=projectName, summary=summaryValue,description=descriptionText , assignee={'name': username}, issuetype={'name': 'Task'},  priority={'name': 'Medium'}, security={'name': 'private (Team)'})
    jira.resolution("Done",new_issue)
    jira.add_attachment(issue=new_issue, attachment=f)
    jira.transition_issue(issue, transition='Done',resolution={'name': 'Done'})
    print(new_issue.fields.status)
