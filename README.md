# XRPL NFT Rich List Generator

This tool generates a rich list of NFT holders for a specific issuer on the XRP Ledger.

## Features

- Fetches all NFTs for a specified issuer address
- Counts NFTs per holder address
- Ranks holders by the number of NFTs they own
- Calculates percentage of total NFTs owned
- Provides detailed distribution statistics
- Filters out burned NFTs
- Displays a formatted table of the top holders
- Exports complete rich list to CSV and statistics to JSON

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Edit the `nft_richlist.py` file to set your issuer address if needed.

## Usage

Run the script with:
```
python nft_richlist.py
```

The script will:
1. Fetch all NFTs for the specified issuer
2. Generate a rich list sorted by NFT holdings
3. Display detailed distribution statistics
4. Display the top 20 holders in the console
5. Save the complete rich list to CSV and statistics to JSON in the `output` directory

## Output Files

The script generates two output files in the `output` directory:
- `xrpl_nfts_richlist_TIMESTAMP.csv`: The complete rich list with owner addresses, NFT counts, and percentages
- `xrpl_nfts_stats_TIMESTAMP.json`: Detailed statistics about the NFT distribution

## Example Output

### Console Output
```
=== NFT Distribution Statistics ===
Total active NFTs: 2098
Total unique holders: 144
Average NFTs per holder: 14.57
Burned NFTs: 0

Top holder owns 47.66% of all NFTs

Holder distribution:
  Holders with 1 NFT: 59 (40.97%)
  Holders with 2-5 NFTs: 53 (36.81%)
  Holders with 6-10 NFTs: 20 (13.89%)
  Holders with 11-50 NFTs: 4 (2.78%)
  Holders with 51-100 NFTs: 5 (3.47%)
  Holders with >100 NFTs: 3 (2.08%)

Top 20 NFT holders:
   Owner Address                        NFT Count  Percentage
1  raBUcZ6CCfPbfQupUnBPXf7h9XWzK6PkiF   1000       47.66%
2  rJA5p2Lu412vvUYeNNSJyF7eFqzrhHQa7L   167        7.96%
...
```

### Statistics JSON
```json
{
  "total_nfts": 2098,
  "total_holders": 144,
  "avg_per_holder": 14.57,
  "holders_with_1": 59,
  "holders_with_2_to_5": 53,
  "holders_with_6_to_10": 20,
  "holders_with_11_to_50": 4,
  "holders_with_51_to_100": 5,
  "holders_with_over_100": 3,
  "top_holder_percentage": 47.66,
  "burned_nfts": 0
}
```

## Coreum Staking APY Fetcher

This script fetches the current APY (Annual Percentage Yield) for staking Coreum from the staking-explorer.com website.

### Usage

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python coreum_staking_apy.py
   ```

3. The script will:
   - Fetch the current APY, APR, and other staking information
   - Display the information in the console
   - Save the data to JSON files in the `output` directory:
     - A timestamped file for historical records
     - A `coreum_staking_latest.json` file that is overwritten with each run

This can be useful for tracking changes in staking rewards over time or automating investment decisions based on yield rates. 