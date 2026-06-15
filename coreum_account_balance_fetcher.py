# File: coreum_account_balance_fetcher.py
# Purpose: Fetch the total Coreum balance for a given wallet address

import requests
import sys
from decimal import Decimal

def fetch_coreum_balance(wallet_address):
    """
    Fetch Coreum wallet balance and return a dictionary with the results
    
    Args:
        wallet_address (str): The Coreum wallet address to check
    
    Returns:
        dict: Dictionary containing the wallet balance information or None if failed
    """
    api_endpoints = [
        "https://coreum-rest.publicnode.com",
        "https://rest.coreum.net",
        "https://rest.mainnet-1.coreum.dev"
    ]
    
    # Initialize dictionary to store the results
    wallet_data = {
        "address": wallet_address,
        "available": Decimal('0'),
        "delegated": Decimal('0'),
        "unbonding": Decimal('0'),
        "reward": Decimal('0'),
        "total": Decimal('0')
    }
    
    # Try each endpoint until one works
    for api_url in api_endpoints:
        try:
            # 1. Get available balance
            balance_response = requests.get(
                f"{api_url}/cosmos/bank/v1beta1/balances/{wallet_address}",
                timeout=15, verify=True
            )
            balance_response.raise_for_status()
            balance_data = balance_response.json()
            
            # Extract COREUM balance from the response
            for balance in balance_data.get('balances', []):
                if balance.get('denom') == 'ucore':  # Coreum uses 'ucore' as the base denomination
                    wallet_data["available"] = Decimal(balance.get('amount', '0')) / Decimal('1000000')  # Convert from ucore to COREUM
                    break
            
            # 2. Get delegated amount (staked)
            delegations_response = requests.get(
                f"{api_url}/cosmos/staking/v1beta1/delegations/{wallet_address}",
                timeout=15, verify=True
            )
            delegations_response.raise_for_status()
            delegations_data = delegations_response.json()
            
            # Sum up all delegations
            for delegation in delegations_data.get('delegation_responses', []):
                balance = delegation.get('balance', {})
                if balance.get('denom') == 'ucore':
                    wallet_data["delegated"] += Decimal(balance.get('amount', '0')) / Decimal('1000000')
            
            # 3. Get unbonding delegations
            unbonding_response = requests.get(
                f"{api_url}/cosmos/staking/v1beta1/delegators/{wallet_address}/unbonding_delegations",
                timeout=15, verify=True
            )
            unbonding_response.raise_for_status()
            unbonding_data = unbonding_response.json()
            
            # Sum up all unbonding amounts
            for unbonding in unbonding_data.get('unbonding_responses', []):
                for entry in unbonding.get('entries', []):
                    wallet_data["unbonding"] += Decimal(entry.get('balance', '0')) / Decimal('1000000')
            
            # 4. Get rewards
            rewards_response = requests.get(
                f"{api_url}/cosmos/distribution/v1beta1/delegators/{wallet_address}/rewards",
                timeout=15, verify=True
            )
            rewards_response.raise_for_status()
            rewards_data = rewards_response.json()
            
            # Extract total rewards
            for reward in rewards_data.get('total', []):
                if reward.get('denom') == 'ucore':
                    wallet_data["reward"] = Decimal(reward.get('amount', '0')) / Decimal('1000000')
                    break
            
            # Calculate total balance
            wallet_data["total"] = wallet_data["available"] + wallet_data["delegated"] + wallet_data["unbonding"] + wallet_data["reward"]
            
            # Convert Decimal objects to float for better compatibility
            for key in wallet_data:
                if isinstance(wallet_data[key], Decimal):
                    wallet_data[key] = float(wallet_data[key])
            
            return wallet_data
            
        except Exception:
            # Just continue trying the next endpoint on any error
            continue
    
    # All endpoints failed
    return None

def format_balance_output(wallet_data):
    """
    Format wallet data into a readable string
    """
    if not wallet_data:
        return "Failed to fetch wallet data."
    
    output = f"=== Coreum Wallet Information ===\n"
    output += f"Address: {wallet_data['address']}\n\n"
    output += f"Balances:\n"
    output += f"  Available: {wallet_data['available']:,.6f} COREUM\n"
    output += f"  Delegated: {wallet_data['delegated']:,.6f} COREUM\n"
    output += f"  Unbonding: {wallet_data['unbonding']:,.6f} COREUM\n"
    output += f"  Reward:    {wallet_data['reward']:,.6f} COREUM\n\n"
    output += f"Total Balance: {wallet_data['total']:,.6f} COREUM"
    
    return output

def main():
    # Use the provided address or default if none is given
    if len(sys.argv) > 1:
        wallet_address = sys.argv[1]
    else:
        # Default to the example wallet address
        wallet_address = "core17hpellnwn69excm6sf0njcyk6tg8ufqtzlflc7"
    
    # Fetch the wallet data
    wallet_data = fetch_coreum_balance(wallet_address)
    
    if wallet_data:
        # Display the formatted output
        print(format_balance_output(wallet_data))
    else:
        print("Failed to fetch wallet data from all available endpoints.")

if __name__ == "__main__":
    main()