from xrpl.models.requests import NFTsByIssuer
from xrpl.clients import JsonRpcClient

# Account configuration
issuer = "rwPBKTM6XcWtXYjCvFhCyzgFR8xem477KR"
minter = "rXMART8usFd5kABXCayoP6ZfB35b4v43t"

# Server configuration
clio_server = "http://23.88.78.185:51234"

# Initialize the client
client = JsonRpcClient(clio_server)

# Function to fetch all NFTs for an issuer
def get_all_nfts(issuer_address):
    all_nfts = []
    marker = None
    page_limit = 100  # Fetch this many NFTs per request
    
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
    
    return all_nfts

# Fetch all NFTs and print the count
nfts = get_all_nfts(issuer)
print(f"\nTotal NFTs found: {len(nfts)}")





