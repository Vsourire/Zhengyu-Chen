import requests
import pandas as pd
from datetime import datetime

# DAO list
dao_list = [
    "arbitrumfoundation.eth", "bitdao.eth", "ens.eth", "opcollective.eth",
    "cow.eth", "balancer.eth", "origingov.eth", "1inch.eth",
    "aavedao.eth", "lido-snapshot.eth", "gmx.eth", "synthetix-stakers-poll.eth",
    "radiantcapital.eth", "dydxgov.eth", "gitcoindao.eth", "klimadao.eth", "kernelgov.eth", "paragonsdao.eth", "stakedao.eth", "zora.eth"
]

# Snapshot GraphQL endpoint
url = "https://hub.snapshot.org/graphql"

# Request proposals
def fetch_proposals(dao, limit=1000):
    query = f"""
    query {{
      proposals(
        first: {limit}
        where: {{ space_in: ["{dao}"] }}
        orderBy: "created"
        orderDirection: asc
      ) {{
        id
        created
        votes
        space {{
          id
        }}
      }}
    }}
    """
    response = requests.post(url, json={"query": query})
    data = response.json()
    return data['data']['proposals']

# Result
results = []

# loop DAO
for dao in dao_list:
    proposals = fetch_proposals(dao, limit=1000)
    
    if len(proposals) < 2:
        continue

    # To DataFrame
    df = pd.DataFrame(proposals)
    df['created'] = pd.to_datetime(df['created'], unit='s')
    df = df.sort_values('created')

    # 1. Average weekly proposals
    total_weeks = (df['created'].iloc[-1] - df['created'].iloc[0]).days / 7
    avg_weekly_proposals = len(df) / total_weeks if total_weeks > 0 else 0

    # 2. Last 10 proposals average votes
    recent_votes = df.tail(10)['votes'].mean()

    results.append({
        "DAO": dao,
        "Total Proposals": len(df),
        "Avg Weekly Proposals": round(avg_weekly_proposals, 2),
        "Avg Voters (Last 10 Proposals)": round(recent_votes, 2)
    })

# Print summary DataFrame
summary_df = pd.DataFrame(results)
print(summary_df)
