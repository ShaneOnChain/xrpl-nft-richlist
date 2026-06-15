from xrpl.models.requests import NFTsByIssuer
from xrpl.clients import JsonRpcClient
from collections import Counter
import pandas as pd
import datetime
import json
import os

# File: nft_richlist.py
# Purpose: Generate a rich list of NFT holders sorted by number of NFTs owned

# Account configuration
issuer = "rwPBKTM6XcWtXYjCvFhCyzgFR8xem477KR"

# Server configuration
clio_server = "http://23.88.78.185:51234"

# Initialize the client
client = JsonRpcClient(clio_server)

def get_all_nfts(issuer_address):
    """Fetch all NFTs for a specific issuer address"""
    all_nfts = []
    marker = None
    page_limit = 100  # Fetch this many NFTs per request
    
    print(f"Fetching NFTs issued by {issuer_address}...")
    
    try:
        while True:
            # Create request with marker if we have one
            request = NFTsByIssuer(
                issuer=issuer_address,
                limit=page_limit,
                marker=marker
            )
            
            # Send the request
            response = client.request(request)
            result = response.result
            
            # Add NFTs from this page to our collection
            if "nfts" in result:
                all_nfts.extend(result["nfts"])
                print(f"Fetched {len(result['nfts'])} NFTs... (Total so far: {len(all_nfts)})")
            
            # Check if we have a marker for next page
            if "marker" in result:
                marker = result["marker"]
            else:
                # No more pages
                break
    except Exception as e:
        print(f"Error fetching NFTs: {e}")
        
    return all_nfts

def create_nft_richlist(nfts):
    """Create a rich list of NFT holders sorted by number of NFTs owned"""
    # Filter out burned NFTs
    active_nfts = [nft for nft in nfts if not nft.get("is_burned", False)]
    
    # Extract owner addresses from NFTs
    owners = [nft["owner"] for nft in active_nfts]
    
    # Count the number of NFTs per owner
    owner_counts = Counter(owners)
    
    # Create a sorted list of (owner, count) tuples
    richlist = owner_counts.most_common()
    
    # Calculate some statistics
    total_nfts = len(active_nfts)
    total_holders = len(owner_counts)
    
    # Calculate distribution statistics
    if total_holders > 0:
        avg_per_holder = total_nfts / total_holders
        # Calculate how many holders have 1, 2-5, 6-10, 11-50, 51-100, 100+ NFTs
        holders_with_1 = sum(1 for _, count in owner_counts.items() if count == 1)
        holders_with_2_to_5 = sum(1 for _, count in owner_counts.items() if 2 <= count <= 5)
        holders_with_6_to_10 = sum(1 for _, count in owner_counts.items() if 6 <= count <= 10)
        holders_with_11_to_50 = sum(1 for _, count in owner_counts.items() if 11 <= count <= 50)
        holders_with_51_to_100 = sum(1 for _, count in owner_counts.items() if 51 <= count <= 100)
        holders_with_over_100 = sum(1 for _, count in owner_counts.items() if count > 100)
    else:
        avg_per_holder = 0
        holders_with_1 = 0
        holders_with_2_to_5 = 0
        holders_with_6_to_10 = 0
        holders_with_11_to_50 = 0
        holders_with_51_to_100 = 0
        holders_with_over_100 = 0
        
    # Get top holder percentage
    if total_nfts > 0 and len(richlist) > 0:
        top_holder_percentage = (richlist[0][1] / total_nfts) * 100
    else:
        top_holder_percentage = 0
        
    stats = {
        "total_nfts": total_nfts,
        "total_holders": total_holders,
        "avg_per_holder": avg_per_holder,
        "holders_with_1": holders_with_1,
        "holders_with_2_to_5": holders_with_2_to_5,
        "holders_with_6_to_10": holders_with_6_to_10,
        "holders_with_11_to_50": holders_with_11_to_50,
        "holders_with_51_to_100": holders_with_51_to_100, 
        "holders_with_over_100": holders_with_over_100,
        "top_holder_percentage": top_holder_percentage,
        "burned_nfts": len(nfts) - len(active_nfts)
    }
    
    return richlist, stats

def display_richlist(richlist, stats, top_n=None):
    """Display the rich list in a formatted way"""
    if top_n:
        display_list = richlist[:top_n]
    else:
        display_list = richlist
    
    # Create a DataFrame for nicer display
    df = pd.DataFrame(display_list, columns=["Owner Address", "NFT Count"])
    df.index = range(1, len(df) + 1)  # 1-based indexing for rank
    
    # Calculate percentage of total
    total_nfts = stats["total_nfts"]
    if total_nfts > 0:
        df["Percentage"] = (df["NFT Count"] / total_nfts * 100).round(2)
        df["Percentage"] = df["Percentage"].astype(str) + '%'
    else:
        df["Percentage"] = "0%"
    
    return df

def print_stats(stats):
    """Print statistics about the NFT distribution"""
    print("\n=== NFT Distribution Statistics ===")
    print(f"Total active NFTs: {stats['total_nfts']}")
    print(f"Total unique holders: {stats['total_holders']}")
    print(f"Average NFTs per holder: {stats['avg_per_holder']:.2f}")
    print(f"Burned NFTs: {stats['burned_nfts']}")
    
    # Top holder info
    print(f"\nTop holder owns {stats['top_holder_percentage']:.2f}% of all NFTs")
    
    # Distribution breakdown
    print("\nHolder distribution:")
    print(f"  Holders with 1 NFT: {stats['holders_with_1']} ({stats['holders_with_1']/stats['total_holders']*100:.2f}%)")
    print(f"  Holders with 2-5 NFTs: {stats['holders_with_2_to_5']} ({stats['holders_with_2_to_5']/stats['total_holders']*100:.2f}%)")
    print(f"  Holders with 6-10 NFTs: {stats['holders_with_6_to_10']} ({stats['holders_with_6_to_10']/stats['total_holders']*100:.2f}%)")
    print(f"  Holders with 11-50 NFTs: {stats['holders_with_11_to_50']} ({stats['holders_with_11_to_50']/stats['total_holders']*100:.2f}%)")
    print(f"  Holders with 51-100 NFTs: {stats['holders_with_51_to_100']} ({stats['holders_with_51_to_100']/stats['total_holders']*100:.2f}%)")
    print(f"  Holders with >100 NFTs: {stats['holders_with_over_100']} ({stats['holders_with_over_100']/stats['total_holders']*100:.2f}%)")

def save_results(richlist, stats, collection_name=""):
    """Save the rich list and stats to files"""
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Format timestamp for filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Base filename
    base_filename = f"{collection_name}_" if collection_name else ""
    
    # Save rich list to CSV
    csv_filename = f"{output_dir}/{base_filename}richlist_{timestamp}.csv"
    df_full = display_richlist(richlist, stats)
    df_full.to_csv(csv_filename)
    print(f"\nComplete rich list saved to {csv_filename}")
    
    # Save stats to JSON
    stats_filename = f"{output_dir}/{base_filename}stats_{timestamp}.json"
    with open(stats_filename, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Statistics saved to {stats_filename}")

def main():
    try:
        # Fetch all NFTs
        nfts = get_all_nfts(issuer)
        print(f"\nTotal NFTs found: {len(nfts)}")
        
        # Create rich list
        print("\nGenerating rich list...")
        richlist, stats = create_nft_richlist(nfts)
        
        # Display stats
        print_stats(stats)
        
        # Display top holders
        top_n = 20  # Show top 20 holders
        print(f"\nTop {top_n} NFT holders:")
        df = display_richlist(richlist, stats, top_n)
        print(df)
        
        # Save results
        collection_name = "xrpl_nfts"  # Optional name for the collection
        save_results(richlist, stats, collection_name)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 