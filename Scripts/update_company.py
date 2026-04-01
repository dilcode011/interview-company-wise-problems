#!/usr/bin/env python3

import requests
import csv
import sys
import os
from datetime import datetime

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"


def fetch_company_problems(company):
    slug = company.lower().replace(" ", "-").replace(".", "")

    query = """
    query companyTag($slug: String!) {
      companyTag(tagSlug: $slug) {
        questions {
          titleSlug
          title
          difficulty
          frequency
          acRate
          topicTags {
            name
          }
        }
      }
    }
    """

    response = requests.post(
        LEETCODE_GRAPHQL,
        json={"query": query, "variables": {"slug": slug}},
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    data = response.json()
    return data.get("data", {}).get("companyTag", {}).get("questions", [])


def save_to_csv(company, questions):
    if not questions:
        print(f"No data for {company}")
        return

    # ✅ Folder = Company Name (IMPORTANT)
    os.makedirs(company, exist_ok=True)

    file_path = f"{company}/problems.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Title", "Slug", "Difficulty",
            "Frequency", "AcceptanceRate",
            "Topics", "FetchedAt"
        ])

        for q in questions:
            topics = ", ".join([t["name"] for t in q.get("topicTags", [])])

            writer.writerow([
                q.get("title"),
                q.get("titleSlug"),
                q.get("difficulty"),
                q.get("frequency"),
                q.get("acRate"),
                topics,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    print(f"Saved: {file_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_company.py 'Amazon'")
        return

    company = sys.argv[1]
    print(f"Updating {company}...")

    questions = fetch_company_problems(company)
    save_to_csv(company, questions)


if __name__ == "__main__":
    main()
