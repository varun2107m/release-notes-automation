from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_release_notes(parsed_data, section_name):
    """
    Generates clean, professional SaaS-style release notes (NO markdown)
    """

    prompt = f"""
You are a senior product manager writing release notes for a mature SaaS product.

IMPORTANT:
- Do NOT use markdown symbols like **, *, #, _
- Output must be plain text only
- Follow the EXACT structure below

STRICT FORMAT:

Module Name
• <clear outcome> for <user group>
• <clear outcome>
• <clear outcome>

RULES:
- Each module MUST have bullets (no plain lines)
- Every bullet must start with "•"
- Merge similar updates into one bullet
- Avoid repetition
- Mention users at least once per module
- Max 3 bullets per module
- Use outcome-driven language (Track, View, Manage, Export)
- Keep each bullet under 12 words

BAD EXAMPLE (DO NOT DO):
Streamline user management ❌

GOOD EXAMPLE:
User Management
• Manage users more efficiently for admins
• Navigate user flows faster with improved layout

INPUT:
{json.dumps(parsed_data, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior product manager writing professional release notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ AI generation failed: {e}")
        return None
    