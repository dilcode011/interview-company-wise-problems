#!/usr/bin/env python3
"""
LeetCode Company-Wise Updater
Usage: python update_company.py "Amazon"
"""

import requests
import csv
import sys
from datetime import datetime

# Public LeetCode GraphQL endpoint (works without login for basic tags)
LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

def fetch_company_problems(company: str):
    query = """
    query companyTag {
      companyTag(tagSlug: $slug) {
        company { name }
        questions {
          titleSlug title difficulty frequency acceptanceRate topicTags { name }
        }
      }
    }
    """
    variables = {"slug": company.lower().replace(" ", "-")}
    response = requests.post(LEETCODE_GRAPHQL, json={"query": query, "variables": variables})
    data = response.json()
    return data.get("data", {}).get("companyTag", {}).get("questions", [])

