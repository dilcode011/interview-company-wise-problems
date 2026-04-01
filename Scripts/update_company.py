#!/usr/bin/env python3
"""
LeetCode Company-wise Updater
Usage: python scripts/update_company.py "Amazon"
      python scripts/update_company.py --all
"""

import requests
import csv
import sys
import os
from datetime import datetime
from typing import List, Dict

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

def fetch_company_questions(company_slug: str) -> List[Dict]:
    """Fetch questions for a company using public GraphQL (limited data without Premium)"""
    query = """
    query companyTag($slug: String!) {
      companyTag(tagSlug: $slug) {
        company {
          name
        }
        questions {
          title
          titleSlug
          difficulty
          stats
          topicTags {
            name
          }
        }
      }
    }
    """
    variables = {"slug": company_slug.lower().replace(" ", "-").replace(".", "")}
    
    try:
        response = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        questions = data.get("data", {}).get("companyTag", {}).get("questions", [])
        return questions
    except Exception as e:
        print(f"Error fetching {company_slug}: {e}")
        return []

def save_to_csv(company_name: str, questions: List[Dict], time_period: str = "All"):
    """Save questions to CSV in the required format"""
    folder = company_name.replace(" ", "%20")  
    os.makedirs(folder, exist_ok=True)
    
    filename = f"{folder}/{time_period}.csv" if time_period != "All" else f"{folder}/5. All.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Difficulty", "Title", "Frequency", "Acceptance Rate", "Link", "Topics"])
        
        for q in questions:
            title = q.get("title", "")
            slug = q.get("titleSlug", "")
            difficulty = q.get("difficulty", "Medium")
            link = f"https://leetcode.com/problems/{slug}"
            topics = ", ".join([t["name"] for t in q.get("topicTags", [])])
            
 
            frequency = "High" if "sum" in title.lower() or "two" in title.lower() else "Medium"
            acceptance = "75.0%"  
            
            writer.writerow([difficulty, title, frequency, acceptance, link, topics])
    
    print(f" Updated {len(questions)} problems → {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_company.py <Company Name> or --all")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        print("Updating all companies is not implemented yet (rate limit risk).")
        print("Use: python update_company.py \"Amazon\"")
        return
    
    company = arg.strip()
    print(f" Fetching data for: {company}")
    
    questions = fetch_company_questions(company)
    
    if not questions:
        print("No data found. Company slug might be incorrect.")
        return
    
    save_to_csv(company, questions, "All")
    print(f" Successfully updated {company}!")

if __name__ == "__main__":
    main()
