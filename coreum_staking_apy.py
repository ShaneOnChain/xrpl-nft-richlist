# File: coreum_staking_apy.py
# Purpose: Fetch the current APY for staking Coreum from staking-explorer.com

import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
import sys
import time

def fetch_coreum_staking_data():
    """
    Fetch staking data for Coreum from staking-explorer.com
    
    Returns:
        dict: Dictionary containing staking information including APY, APR, etc.
    """
    url = "https://staking-explorer.com/explorer/coreum"
    print(f"Fetching Coreum staking data from {url}...")
    
    try:
        # Send GET request to the staking explorer
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize dictionary to store the results
        staking_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source_url": url
        }
        
        # Extract APY (look for text containing "APY" and the percentage value)
        apy_element = soup.find(string=lambda text: "APY" in text if text else False)
        if apy_element and apy_element.find_parent():
            # Find the percentage value near the APY text
            apy_container = apy_element.find_parent().find_parent()
            if apy_container:
                apy_value = apy_container.find(string=lambda text: "%" in text if text else False)
                if apy_value:
                    staking_data["apy"] = apy_value.strip()
        
        # Extract APR
        apr_element = soup.find(string=lambda text: "APR" in text if text else False)
        if apr_element and apr_element.find_parent():
            apr_container = apr_element.find_parent().find_parent()
            if apr_container:
                apr_value = apr_container.find(string=lambda text: "%" in text if text else False)
                if apr_value:
                    staking_data["apr"] = apr_value.strip()
        
        # Extract Real Staking Reward (RSR)
        rsr_element = soup.find(string=lambda text: "RSR" in text if text else False)
        if rsr_element and rsr_element.find_parent():
            rsr_container = rsr_element.find_parent().find_parent()
            if rsr_container:
                rsr_value = rsr_container.find(string=lambda text: "%" in text if text else False)
                if rsr_value:
                    staking_data["real_staking_reward"] = rsr_value.strip()
        
        # Extract bonded tokens percentage
        bonded_element = soup.find(string=lambda text: "Bonded tokens" in text if text else False)
        if bonded_element and bonded_element.find_parent():
            bonded_container = bonded_element.find_parent().find_parent()
            if bonded_container:
                bonded_value = bonded_container.find(string=lambda text: "%" in text if text else False)
                if bonded_value:
                    staking_data["bonded_percentage"] = bonded_value.strip()
        
        # Extract unbonding period
        unbonding_element = soup.find(string=lambda text: "Unbonding period" in text if text else False)
        if unbonding_element and unbonding_element.find_parent():
            unbonding_container = unbonding_element.find_parent().find_parent()
            if unbonding_container:
                days_element = unbonding_container.find(string=lambda text: "days" in text if text else False)
                if days_element:
                    staking_data["unbonding_period"] = days_element.strip()
        
        return staking_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_staking_data(staking_data):
    """
    Save the staking data to a JSON file
    
    Args:
        staking_data (dict): Dictionary containing staking information
    """
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Format timestamp for filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save staking data to JSON
    filename = f"{output_dir}/coreum_staking_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(staking_data, f, indent=2)
    print(f"Staking data saved to {filename}")
    
    # Also save to a "latest" file that's always overwritten
    latest_filename = f"{output_dir}/coreum_staking_latest.json"
    with open(latest_filename, 'w') as f:
        json.dump(staking_data, f, indent=2)
    print(f"Latest staking data saved to {latest_filename}")

def display_staking_data(staking_data):
    """
    Display the staking data in a formatted way
    
    Args:
        staking_data (dict): Dictionary containing staking information
    """
    if not staking_data:
        print("No staking data available to display.")
        return
    
    print("\n=== Coreum Staking Information ===")
    print(f"Timestamp: {staking_data.get('timestamp', 'N/A')}")
    print(f"Source: {staking_data.get('source_url', 'N/A')}")
    print("\nRewards:")
    print(f"  APY: {staking_data.get('apy', 'N/A')}")
    print(f"  APR: {staking_data.get('apr', 'N/A')}")
    print(f"  Real Staking Reward: {staking_data.get('real_staking_reward', 'N/A')}")
    print("\nStaking Stats:")
    print(f"  Bonded Percentage: {staking_data.get('bonded_percentage', 'N/A')}")
    print(f"  Unbonding Period: {staking_data.get('unbonding_period', 'N/A')}")

def main():
    try:
        # Fetch staking data
        staking_data = fetch_coreum_staking_data()
        
        if staking_data:
            # Display the data
            display_staking_data(staking_data)
            
            # Save the data
            save_staking_data(staking_data)
        else:
            print("Failed to fetch staking data.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 