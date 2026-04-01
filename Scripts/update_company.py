#!/usr/bin/env python3
"""
LeetCode Company-Wise Problems Updater
Usage: python update_company.py "Amazon"

This script fetches company-tagged problems from LeetCode using GraphQL
and saves them to a CSV file inside a company-specific folder.
"""

import requests
import csv
import sys
import os
from datetime import datetime

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

def fetch_company_problems(company: str):
    """Fetch problems for a given company using LeetCode GraphQL."""
  
    slug = company.lower().replace(" ", "-").replace(".", "")

    query = """
    query companyTag($slug: String!) {
      companyTag(tagSlug: $slug) {
        company {
          name
        }
        questions {
          titleSlug
          title
          difficulty
          frequency
          acceptanceRate: acRate
          topicTags {
            name
          }
        }
      }
    }
    """

    variables = {"slug": slug}

    try:
        response = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        questions = data.get("data", {}).get("companyTag", {}).get("questions", [])
        
        if not questions:
            print(f" No problems found for company: {company} (slug: {slug})")
            return []

        print(f" Successfully fetched {len(questions)} problems for {company}")
        return questions

    except requests.exceptions.RequestException as e:
        print(f" Network error while fetching {company}: {e}")
        return []
    except Exception as e:
        print(f" Unexpected error while fetching {company}: {e}")
        return []


def save_to_csv(company: str, questions: list):
    """Save fetched problems to CSV file."""
    if not questions:
        return


    output_dir = os.path.join("data", company.lower().replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{company.lower()}_problems.csv")
    
    
    headers = [
        "title", "titleSlug", "difficulty", "frequency", 
        "acceptanceRate", "topics", "fetched_at"
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for q in questions:
            topics = ", ".join([tag.get("name", "") for tag in q.get("topicTags", [])])
            
            writer.writerow({
                "title": q.get("title", ""),
                "titleSlug": q.get("titleSlug", ""),
                "difficulty": q.get("difficulty", ""),
                "frequency": q.get("frequency", 0),
                "acceptanceRate": q.get("acceptanceRate", 0),
                "topics": topics,
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    print(f" Saved {len(questions)} problems to {filename}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_company.py \"Company Name\"")
        print("Example: python update_company.py \"Amazon\"")
        sys.exit(1)

    company = sys.argv[1].strip()
    print(f" Starting update for company: {company}")

    questions = fetch_company_problems(company)
    save_to_csv(company, questions)

    print(f" Update completed for {company}!")


if __name__ == "__main__":
    main()
